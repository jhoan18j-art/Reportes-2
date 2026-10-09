import { describe, expect, it } from "vitest";
import { monthlyTotals, totalsByCategory } from "./incomes";

describe("monthlyTotals", () => {
  it("sums incomes per month for the last 6 months", () => {
    const r = monthlyTotals(
      [
        { amount: 100.1, income_date: "2026-10-02" },
        { amount: 50.2, income_date: "2026-10-20" },
        { amount: 30, income_date: "2026-05-01" },
        { amount: 999, income_date: "2026-04-30" },
      ],
      new Date(2026, 9, 6),
    );
    expect(r.map((x) => x.key)).toEqual(["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]);
    expect(r[5]?.total).toBe(150.3);
    expect(r[0]?.total).toBe(30);
  });
});

describe("totalsByCategory", () => {
  it("groups and sorts by total", () => {
    expect(totalsByCategory([
      { amount: 10, category: "Ventas" },
      { amount: 40, category: "Renta" },
      { amount: 5, category: "Ventas" },
    ])).toEqual([{ category: "Renta", total: 40 }, { category: "Ventas", total: 15 }]);
  });
});
