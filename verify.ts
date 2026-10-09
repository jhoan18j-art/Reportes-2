export type CheckTerm = { label: string; value: number; sign: 1 | -1 };
export type Operation = {
  label: string;
  operator: "sum" | "product";
  terms: CheckTerm[];
  written_result: number;
};
export type CheckResult = Operation & { expected: number; ok: boolean; difference: number };

const round2 = (n: number) => Math.round(n * 100) / 100;

/** Recalcula cada operación escrita en el ticket y marca diferencias mayores a 1 centavo. */
export function verifyOperations(ops: Operation[]): CheckResult[] {
  return ops
    .filter((o) => o.terms.length > 0)
    .map((o) => {
      const expected = round2(
        o.operator === "product"
          ? o.terms.reduce((acc, t) => acc * t.value, 1)
          : o.terms.reduce((acc, t) => acc + t.sign * t.value, 0),
      );
      const difference = round2(o.written_result - expected);
      return { ...o, expected, difference, ok: Math.abs(difference) <= 0.01 };
    });
}
