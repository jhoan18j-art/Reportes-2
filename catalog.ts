export const USERS = {
  "Víctor": { role: "usuario" },
  "Jesús": { role: "usuario" },
  auditor: { role: "auditor" },
} as const;
export type UserName = keyof typeof USERS;
export const USER_NAMES = Object.keys(USERS) as UserName[];

export const CATALOG: Record<string, string[]> = {
  "Pampas Insurgentes": ["Jesús"],
  Rama: ["Jesús"],
  Sushito: ["Jesús"],
  Barranca: ["Jesús"],
  Carajillo: ["Jesús"],
  Pennygans: ["Jesús"],
  "Clínica": ["Jesús"],
  "Zumo Santa Mónica": ["Víctor"],
  "Zumo Chegaray": ["Víctor"],
  "Ryoshi Polanco": ["Víctor"],
  "Encanto Polanco": ["Víctor"],
  "Churrasquería": ["Víctor"],
  "Salón Romance": ["Jesús", "Víctor"],
  "Jungla Tlalpan": ["Jesús", "Víctor"],
  "Jungla División": ["Jesús", "Víctor"],
  "Jungla Picacho": ["Jesús", "Víctor"],
  "Jungla Empresas": ["Jesús", "Víctor"],
  "Cipirilí": ["Jesús", "Víctor"],
  "Marometa Satélite": ["Jesús", "Víctor"],
  "Marometa Marina": ["Jesús", "Víctor"],
  Veterinaria: ["Jesús", "Víctor"],
};
export const SITES = Object.keys(CATALOG);

/** Sitios ordenados: primero los asignados a la persona, luego el resto. */
export function sitesFor(name: string | null) {
  const mine = SITES.filter((s) => name && CATALOG[s]?.includes(name));
  return { mine, others: SITES.filter((s) => !mine.includes(s)) };
}

export const FIELDS = [
  ["fecha", "Fecha (AAAA-MM-DD)"], ["sitio", "Sitio"], ["costo_unitario", "Costo unitario"],
  ["folio_inicial", "Folio inicial utilizado"], ["folio_final", "Folio final utilizado"],
  ["folio_inicio_block", "Folio de inicio sin desprender en block"],
  ["total_boletos", "Total de boletos"], ["boletos_pagados", "Boletos pagados"],
  ["boletos_cancelados", "Boletos cancelados"], ["boletos_perdidos", "Boletos perdidos"],
  ["boletos_entregados", "Total de boletos entregados"],
  ["gastos_operacion", "Gastos de operación"], ["lider_unidad", "Líder de unidad"],
  ["sueldo", "Sueldo"], ["operador", "Operador"],
  ["gastos_especiales", "Gastos especiales"],
  ["total_nominas_gastos", "Total de nóminas y gastos"],
  ["elabora_flujo", "Quién elabora el reporte de flujo"],
  ["elabora_reporte", "Quién elabora el reporte"],
  ["recibe_dinero", "Quién recibe la cantidad de dinero"],
  ["recibe_reporte", "Quién recibe el reporte"],
] as const;
export type FieldKey = (typeof FIELDS)[number][0];
export type Report = Record<FieldKey, string>;
export const emptyReport = (): Report => Object.fromEntries(FIELDS.map(([k]) => [k, ""])) as Report;

export const accountEmail = (name: string) =>
  `${name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "")}@snapincome.app`;

/** Fecha de hoy en Ciudad de México (AAAA-MM-DD). */
export const todayMx = () => new Date().toLocaleDateString("en-CA", { timeZone: "America/Mexico_City" });
