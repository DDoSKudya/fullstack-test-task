import { describe, expect, it } from "vitest";
import { translateScanDetail, translateAlertMessage, alertLevelLabel, formatAlertDate } from "@/composables/useAlertText";

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
});

describe("alertLevelLabel", () => {
  const t = (key: string) => (key === "alerts.levels.warning" ? "Внимание" : key);

  it("translates known levels", () => {
    expect(alertLevelLabel("warning", t)).toBe("Внимание");
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
});
