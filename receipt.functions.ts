import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { requireSupabaseAuth } from "@/integrations/supabase/auth-middleware";
import { FIELDS, SITES, type FieldKey } from "./catalog";
import type { Operation } from "./verify";

export type ExtractedReceipt = {
  amount: number | null;
  report: Record<FieldKey, string | null>;
  operations: Operation[];
};

const schema = {
  type: "object",
  additionalProperties: false,
  required: ["amount", "report", "operations"],
  properties: {
    amount: { type: ["number", "null"], description: "Cantidad a entregar (ingreso neto en efectivo)" },
    report: {
      type: "object",
      additionalProperties: false,
      required: FIELDS.map(([k]) => k),
      properties: Object.fromEntries(FIELDS.map(([k, label]) => [k, { type: ["string", "null"], description: label }])),
    },
    operations: {
      type: "array",
      description: "Cada cuenta escrita en el papel (sumas, restas, cantidad x precio, totales y subtotales), copiando los números tal como están escritos, sin corregirlos.",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["label", "operator", "terms", "written_result"],
        properties: {
          label: { type: "string" },
          operator: { type: "string", enum: ["sum", "product"] },
          terms: {
            type: "array",
            items: {
              type: "object",
              additionalProperties: false,
              required: ["label", "value", "sign"],
              properties: {
                label: { type: "string" },
                value: { type: "number" },
                sign: { type: "integer", enum: [1, -1] },
              },
            },
          },
          written_result: { type: "number" },
        },
      },
    },
  },
};

const SYSTEM = `Lees fotos de reportes de operación de valet/estacionamiento (Club Park). Llena cada campo de "report" con lo escrito en el papel, como texto; usa null si está vacío o no se ve. fecha en formato AAAA-MM-DD. sitio: elige el nombre más parecido de esta lista: ${SITES.join(", ")}; si no se parece a ninguno, copia lo escrito. Números sin signo de pesos. amount es la cantidad a entregar en efectivo. En operations transcribe TODAS las cuentas del papel (boletos x costo, suma de nómina y gastos, ingreso bruto menos gastos) con los números exactamente como están escritos, aunque estén mal; no las corrijas. Si no hay cuentas, devuelve [].`;

export const extractReceipt = createServerFn({ method: "POST" })
  .middleware([requireSupabaseAuth])
  .inputValidator((d) => z.object({ image: z.string().startsWith("data:image/").max(9_000_000) }).parse(d))
  .handler(async ({ data }): Promise<{ ok: true; data: ExtractedReceipt } | { ok: false; error: string }> => {
    const key = process.env["LOVABLE_API_KEY"];
    if (!key) return { ok: false, error: "La lectura de fotos no está configurada." };

    const res = await fetch("https://ai.gateway.lovable.dev/v1/responses", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Lovable-API-Key": key, "X-Lovable-AIG-SDK": "fetch" },
      body: JSON.stringify({
        model: "openai/gpt-6-astra",
        stream: true,
        store: false,
        reasoning: { effort: "low", summary: "auto" },
        include: ["reasoning.encrypted_content"],
        input: [
          {
            role: "system",
            content: SYSTEM,
          },
          {
            role: "user",
            content: [
              { type: "input_text", text: "Lee este reporte." },
              { type: "input_image", image_url: data.image },
            ],
          },
        ],
        text: { format: { type: "json_schema", name: "receipt", strict: true, schema } },
      }),
    });

    if (!res.ok || !res.body) {
      const body = await res.text().catch(() => "");
      console.error("AI gateway error", res.status, body);
      if (res.status === 429) return { ok: false, error: "Demasiadas solicitudes. Intenta en un momento." };
      if (res.status === 402) return { ok: false, error: "Se agotaron los créditos de IA del espacio de trabajo." };
      return { ok: false, error: "No pudimos leer la foto. Llena los datos manualmente." };
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    let text = "";
    let failed = false;
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split("\n");
      buf = lines.pop() ?? "";
      for (const line of lines) {
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (!payload || payload === "[DONE]") continue;
        try {
          const ev = JSON.parse(payload);
          if (ev.type === "response.output_text.delta") text += ev.delta;
          if (ev.type === "response.failed" || ev.type === "error") failed = true;
        } catch {
          /* ignore partial */
        }
      }
    }
    if (failed || !text.trim()) return { ok: false, error: "No pudimos leer la foto. Llena los datos manualmente." };
    try {
      return { ok: true, data: JSON.parse(text) as ExtractedReceipt };
    } catch {
      return { ok: false, error: "La respuesta no fue válida. Llena los datos manualmente." };
    }
  });
