export const CATEGORIES = ["Ventas", "Servicios", "Honorarios", "Renta", "Reembolso", "Otros"] as const;
export const PAYMENT_METHODS = ["Efectivo", "Tarjeta", "Transferencia", "Otro"] as const;

export type Income = {
  id: string;
  amount: number;
  currency: string;
  income_date: string;
  payer: string | null;
  concept: string | null;
  category: string;
  payment_method: string;
  photo_path: string | null;
  site: string | null;
  report: Record<string, string> | null;
  user_id: string;
  created_at: string;
};

const MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];

export function formatMoney(n: number, currency = "MXN") {
  return new Intl.NumberFormat("es-MX", { style: "currency", currency }).format(n);
}

export function formatDate(d: string) {
  const [y, m = 1, day] = d.split("-").map(Number);
  return `${day} ${MONTHS[m - 1]} ${y}`;
}

/** Totals for the last `count` months ending at `today`, oldest first. */
export function monthlyTotals(incomes: Pick<Income, "amount" | "income_date">[], today: Date, count = 6) {
  const out: { key: string; label: string; total: number }[] = [];
  for (let i = count - 1; i >= 0; i--) {
    const d = new Date(today.getFullYear(), today.getMonth() - i, 1);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
    out.push({ key, label: MONTHS[d.getMonth()] ?? "", total: 0 });
  }
  for (const inc of incomes) {
    const row = out.find((r) => r.key === inc.income_date.slice(0, 7));
    if (row) row.total = Math.round((row.total + Number(inc.amount)) * 100) / 100;
  }
  return out;
}

export function totalsByCategory(incomes: Pick<Income, "amount" | "category">[]) {
  const map = new Map<string, number>();
  for (const i of incomes) map.set(i.category, (map.get(i.category) ?? 0) + Number(i.amount));
  return [...map.entries()].map(([category, total]) => ({ category, total })).sort((a, b) => b.total - a.total);
}
