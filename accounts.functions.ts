import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { requireSupabaseAuth } from "@/integrations/supabase/auth-middleware";
import { USERS, USER_NAMES, accountEmail } from "./catalog";

function randomPassword() {
  const chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const bytes = crypto.getRandomValues(new Uint8Array(10));
  return Array.from(bytes, (b) => chars[b % chars.length]).join("");
}

/** Devuelve el correo interno de la cuenta; crea la cuenta con contraseña aleatoria la primera vez. */
export const getLoginEmail = createServerFn({ method: "POST" })
  .inputValidator((d) => z.object({ name: z.enum(USER_NAMES as [string, ...string[]]) }).parse(d))
  .handler(async ({ data }) => {
    const { supabaseAdmin } = await import("@/integrations/supabase/client.server");
    // Crea todas las cuentas la primera vez, para que el auditor pueda ver sus contraseñas.
    for (const name of USER_NAMES) await ensureAccount(supabaseAdmin, name);
    return { email: accountEmail(data.name) };
  });

async function ensureAccount(admin: any, name: (typeof USER_NAMES)[number]) {
  const { data: row } = await admin.from("app_accounts").select("email").eq("name", name).maybeSingle();
  if (row) return;
  const email = accountEmail(name);
  const password = randomPassword();
  const role = USERS[name].role;
  let userId: string;
  const created = await admin.auth.admin.createUser({ email, password, email_confirm: true, user_metadata: { name } });
  if (created.error) {
    const list = await admin.auth.admin.listUsers({ perPage: 1000 });
    const existing = list.data.users.find((u: any) => u.email === email);
    if (!existing) throw new Error("No se pudo crear la cuenta");
    userId = existing.id;
    await admin.auth.admin.updateUserById(userId, { password });
  } else userId = created.data.user.id;
  await admin.from("user_roles").upsert({ user_id: userId, role }, { onConflict: "user_id,role" });
  await admin.from("app_accounts").insert({ name, role, email, password, user_id: userId });
}

async function assertAuditor(supabase: any, userId: string) {
  const { data } = await supabase.rpc("has_role", { _user_id: userId, _role: "auditor" });
  if (!data) throw new Error("Solo el auditor puede hacer esto");
}

export const listAccounts = createServerFn({ method: "GET" })
  .middleware([requireSupabaseAuth])
  .handler(async ({ context }) => {
    await assertAuditor(context.supabase, context.userId);
    const { supabaseAdmin } = await import("@/integrations/supabase/client.server");
    const { data } = await supabaseAdmin.from("app_accounts").select("name, role, password, updated_at");
    const rows = data ?? [];
    return USER_NAMES.map((n) => {
      const r = rows.find((x) => x.name === n);
      return { name: n, role: USERS[n].role, password: r?.password ?? null };
    });
  });

export const setAccountPassword = createServerFn({ method: "POST" })
  .middleware([requireSupabaseAuth])
  .inputValidator((d) =>
    z.object({ name: z.enum(USER_NAMES as [string, ...string[]]), password: z.string().min(6).max(72) }).parse(d),
  )
  .handler(async ({ data, context }) => {
    await assertAuditor(context.supabase, context.userId);
    const { supabaseAdmin } = await import("@/integrations/supabase/client.server");
    const { data: row } = await supabaseAdmin.from("app_accounts").select("user_id").eq("name", data.name).maybeSingle();
    if (!row) return { ok: false as const, error: "Esa persona aún no ha entrado por primera vez." };
    const { error } = await supabaseAdmin.auth.admin.updateUserById(row.user_id, { password: data.password });
    if (error) return { ok: false as const, error: "No se pudo cambiar la contraseña." };
    await supabaseAdmin.from("app_accounts").update({ password: data.password, updated_at: new Date().toISOString() }).eq("name", data.name);
    return { ok: true as const };
  });
