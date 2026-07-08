import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

function mockStorage() {
  const store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] ?? null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
  };
}

describe("i18n", () => {
  beforeEach(() => {
    vi.stubGlobal("localStorage", mockStorage());
    document.documentElement.lang = "en";
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.resetModules();
  });

  it("setLocale updates i18n, storage and document lang", async () => {
    const { setLocale, i18n } = await import("./index");

    setLocale("ru");

    expect(i18n.global.locale.value).toBe("ru");
    expect(localStorage.getItem("locale")).toBe("ru");
    expect(document.documentElement.lang).toBe("ru");
  });

  it("resolveLocale prefers stored locale", async () => {
    localStorage.setItem("locale", "ru");
    vi.stubGlobal("navigator", { language: "en-US" });

    const { i18n } = await import("./index");

    expect(i18n.global.locale.value).toBe("ru");
  });

  it("resolveLocale falls back to browser language", async () => {
    vi.stubGlobal("navigator", { language: "ru-RU" });

    const { i18n } = await import("./index");

    expect(i18n.global.locale.value).toBe("ru");
  });

  it("resolveLocale defaults to en for empty browser language", async () => {
    vi.stubGlobal("navigator", { language: "" });

    const { i18n } = await import("./index");

    expect(i18n.global.locale.value).toBe("en");
  });
});
