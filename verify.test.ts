import { describe, it, expect } from "vitest";
import { verifyOperations } from "./verify";

describe("verifyOperations", () => {
  it("acepta una suma correcta", () => {
    const [r] = verifyOperations([{ label: "Neto", operator: "sum", written_result: 1700, terms: [
      { label: "Bruto", value: 2000, sign: 1 }, { label: "Gastos", value: 300, sign: -1 }] }]);
    expect(r!.ok).toBe(true);
  });
  it("detecta una suma mal hecha", () => {
    const [r] = verifyOperations([{ label: "Total", operator: "sum", written_result: 1750, terms: [
      { label: "A", value: 1000, sign: 1 }, { label: "B", value: 700, sign: 1 }] }]);
    expect(r!.ok).toBe(false);
    expect(r!.difference).toBe(50);
  });
  it("detecta cantidad por precio mal calculado", () => {
    const [r] = verifyOperations([{ label: "Boletos", operator: "product", written_result: 400, terms: [
      { label: "Cantidad", value: 12, sign: 1 }, { label: "Precio", value: 35, sign: 1 }] }]);
    expect(r!.expected).toBe(420);
    expect(r!.ok).toBe(false);
  });
});
