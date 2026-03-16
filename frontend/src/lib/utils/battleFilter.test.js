import { describe, it, expect } from "vitest";
import { filterBattlesByDate } from "./battleFilter.js";

describe("filterBattlesByDate", () => {
  const battles = [
    { Battle: "A", start_date: "1861-04-12", end_date: "1861-04-12" },
    { Battle: "B", start_date: "1863-07-01", end_date: "1863-07-03" }
  ];

  it("includes single-day battle on exact day", () => {
    const result = filterBattlesByDate(battles, "1861-04-12");
    expect(result.map((b) => b.Battle)).toContain("A");
  });

  it("includes multi-day battle during range", () => {
    const result = filterBattlesByDate(battles, "1863-07-02");
    expect(result.map((b) => b.Battle)).toContain("B");
  });

  it("excludes battle outside range", () => {
    const result = filterBattlesByDate(battles, "1862-01-01");
    expect(result).toHaveLength(0);
  });
});