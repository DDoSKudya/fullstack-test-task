import { describe, expect, it } from "vitest";
import { formatBytes } from "./format";

describe("formatBytes", () => {
  it.each([
    { bytes: 0, expected: "0 B" },
    { bytes: 512, expected: "512 B" },
    { bytes: 1023, expected: "1023 B" },
    { bytes: 1024, expected: "1.0 KB" },
    { bytes: 1536, expected: "1.5 KB" },
    { bytes: 1024 * 1024 - 1, expected: "1024.0 KB" },
    { bytes: 1024 * 1024, expected: "1.0 MB" },
    { bytes: 5 * 1024 * 1024, expected: "5.0 MB" },
  ])("formats $bytes bytes as $expected", ({ bytes, expected }) => {
    expect(formatBytes(bytes)).toBe(expected);
  });
});
