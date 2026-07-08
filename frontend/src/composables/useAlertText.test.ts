import { createI18n } from "vue-i18n";
import { createApp, h } from "vue";
import { describe, expect, it } from "vitest";
import en from "@/i18n/locales/en.json";
import ru from "@/i18n/locales/ru.json";
import {
  alertLevelLabel,
  formatAlertDate,
  translateAlertMessage,
  translateScanDetail,
  useAlertText,
} from "@/composables/useAlertText";

function withI18n<T>(composable: () => T, locale: "en" | "ru" = "ru"): T {
  const i18n = createI18n({
    legacy: false,
    locale,
    messages: { en, ru },
  });
  let result!: T;
  const app = createApp({
    setup() {
      result = composable();
      return () => h("div");
    },
  });
  app.use(i18n);
  app.mount(document.createElement("div"));
  return result;
}

function ruTranslator(key: string, params?: Record<string, string>): string {
  switch (key) {
    case "alerts.reasons.suspiciousExtension":
      return `Подозрительное расширение ${params?.ext ?? ""}`;
    case "alerts.reasons.oversized":
      return `Размер файла превышает ${params?.limit ?? ""}`;
    case "alerts.reasons.pdfMimeMismatch":
      return "Расширение PDF не соответствует MIME-типу";
    case "alerts.reasons.magicMismatch":
      return `Содержимое похоже на .${params?.detected ?? ""}, а не на .${params?.declared ?? ""}`;
    case "alerts.reasons.fileNotFound":
      return "Файл не найден при извлечении метаданных";
    default:
      return key;
  }
}

describe("translateScanDetail", () => {
  const t = ruTranslator;

  it.each([
    {
      detail: "suspicious extension .exe",
      expected: "Подозрительное расширение .exe",
    },
    {
      detail: "file is larger than 10 MB",
      expected: "Размер файла превышает 10 MB",
    },
    {
      detail: "pdf extension does not match mime type",
      expected: "Расширение PDF не соответствует MIME-типу",
    },
    {
      detail: "file content looks like .png, not .txt",
      expected: "Содержимое похоже на .png, а не на .txt",
    },
    {
      detail: "stored file not found during metadata extraction",
      expected: "Файл не найден при извлечении метаданных",
    },
  ])("translates known scan detail: $detail", ({ detail, expected }) => {
    expect(translateScanDetail(detail, t)).toBe(expected);
  });

  it("returns unknown detail unchanged", () => {
    expect(translateScanDetail("custom backend message", t)).toBe("custom backend message");
  });
});

describe("translateAlertMessage", () => {
  const alertT = (key: string, params?: Record<string, string>) => {
    switch (key) {
      case "alerts.messages.processed":
        return "Файл успешно обработан";
      case "alerts.messages.failed":
        return "Ошибка обработки файла";
      case "alerts.messages.requiresAttention":
        return `Требует внимания: ${params?.details ?? ""}`;
      case "alerts.reasons.suspiciousExtension":
        return `Подозрительное расширение ${params?.ext ?? ""}`;
      default:
        return key;
    }
  };

  it("returns english message unchanged", () => {
    expect(translateAlertMessage("File processed successfully", "en", alertT)).toBe(
      "File processed successfully",
    );
  });

  it("translates processed message on ru locale", () => {
    expect(translateAlertMessage("File processed successfully", "ru", alertT)).toBe(
      "Файл успешно обработан",
    );
  });

  it("translates attention message with scan details", () => {
    const message = "File requires attention: suspicious extension .exe";
    expect(translateAlertMessage(message, "ru", alertT)).toBe(
      "Требует внимания: Подозрительное расширение .exe",
    );
  });

  it("translates failed message on ru locale", () => {
    expect(translateAlertMessage("File processing failed", "ru", alertT)).toBe(
      "Ошибка обработки файла",
    );
  });

  it("returns unknown message unchanged on ru locale", () => {
    expect(translateAlertMessage("custom message", "ru", alertT)).toBe("custom message");
  });
});

describe("alertLevelLabel", () => {
  const t = (key: string) => {
    switch (key) {
      case "alerts.levels.info":
        return "Инфо";
      case "alerts.levels.warning":
        return "Внимание";
      case "alerts.levels.critical":
        return "Критично";
      default:
        return key;
    }
  };

  it.each([
    ["info", "Инфо"],
    ["warning", "Внимание"],
    ["critical", "Критично"],
  ] as const)("translates %s level", (level, expected) => {
    expect(alertLevelLabel(level, t)).toBe(expected);
  });

  it("returns unknown level unchanged", () => {
    expect(alertLevelLabel("custom", t)).toBe("custom");
  });
});

describe("formatAlertDate", () => {
  it("formats date for ru locale", () => {
    const formatted = formatAlertDate("2026-07-07T12:00:00Z", "ru");
    expect(formatted).toMatch(/июл/i);
  });

  it("formats date for en locale", () => {
    const formatted = formatAlertDate("2026-07-07T12:00:00Z", "en");
    expect(formatted).toMatch(/Jul/i);
  });
});

describe("useAlertText", () => {
  it("exposes translated helpers", () => {
    const { levelLabel, alertMessage, formatAlertDate: formatDate } = withI18n(
      () => useAlertText(),
      "ru",
    );

    expect(levelLabel("warning")).toBe("Внимание");
    expect(alertMessage("File processed successfully")).toBe("Файл успешно обработан");
    expect(formatDate("2026-07-07T12:00:00Z")).toMatch(/июл/i);
  });
});
