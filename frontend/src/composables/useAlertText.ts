import { useI18n } from "vue-i18n";

const PROCESSED_MESSAGE = "File processed successfully";
const FAILED_MESSAGE = "File processing failed";
const ATTENTION_PREFIX = "File requires attention: ";

export function translateScanDetail(
  detail: string,
  t: (key: string, params?: Record<string, string>) => string,
): string {
  const suspicious = detail.match(/^suspicious extension (.+)$/);
  if (suspicious) {
    return t("alerts.reasons.suspiciousExtension", { ext: suspicious[1] });
  }

  const oversized = detail.match(/^file is larger than (.+)$/);
  if (oversized) {
    return t("alerts.reasons.oversized", { limit: oversized[1] });
  }

  if (detail === "pdf extension does not match mime type") {
    return t("alerts.reasons.pdfMimeMismatch");
  }

  const magic = detail.match(/^file content looks like \.(.+), not \.(.+)$/);
  if (magic) {
    return t("alerts.reasons.magicMismatch", { detected: magic[1], declared: magic[2] });
  }

  if (detail === "stored file not found during metadata extraction") {
    return t("alerts.reasons.fileNotFound");
  }

  return detail;
}

export function translateAlertMessage(
  message: string,
  locale: string,
  t: (key: string, params?: Record<string, string>) => string,
): string {
  if (locale === "en") {
    return message;
  }

  if (message === PROCESSED_MESSAGE) {
    return t("alerts.messages.processed");
  }
  if (message === FAILED_MESSAGE) {
    return t("alerts.messages.failed");
  }
  if (message.startsWith(ATTENTION_PREFIX)) {
    const details = message.slice(ATTENTION_PREFIX.length);
    const translated = details
      .split(", ")
      .map((part) => translateScanDetail(part, t))
      .join(", ");
    return t("alerts.messages.requiresAttention", { details: translated });
  }

  return message;
}

export function alertLevelLabel(
  level: string,
  t: (key: string) => string,
): string {
  if (level === "info" || level === "warning" || level === "critical") {
    return t(`alerts.levels.${level}`);
  }
  return level;
}

export function formatAlertDate(value: string, locale: string): string {
  const dateLocale = locale === "ru" ? "ru-RU" : "en-US";
  return new Date(value).toLocaleString(dateLocale, {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function useAlertText() {
  const { t, locale } = useI18n();

  return {
    levelLabel: (level: string) => alertLevelLabel(level, t),
    alertMessage: (message: string) => translateAlertMessage(message, locale.value, t),
    formatAlertDate: (value: string) => formatAlertDate(value, locale.value),
  };
}
