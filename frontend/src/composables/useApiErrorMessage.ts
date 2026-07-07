import { useI18n } from "vue-i18n";
import { ApiError } from "@/api/client";

export function translateApiError(
  message: string,
  t: (key: string, params?: Record<string, string>) => string,
): string {
  if (message === "File not found") {
    return t("errors.fileNotFound");
  }
  if (message === "Stored file not found") {
    return t("errors.storedFileNotFound");
  }
  if (message === "Filename is required") {
    return t("errors.filenameRequired");
  }
  if (message === "File is empty") {
    return t("errors.fileEmpty");
  }

  const tooLarge = message.match(/^file exceeds maximum upload size of (\d+) bytes$/);
  if (tooLarge) {
    return t("errors.fileTooLarge", { limit: tooLarge[1] });
  }

  return message;
}

export function formatApiError(
  error: unknown,
  fallback: string,
  locale: string,
  t: (key: string, params?: Record<string, string>) => string,
): string {
  if (!(error instanceof ApiError)) {
    return fallback;
  }
  if (locale === "en") {
    return error.message;
  }
  return translateApiError(error.message, t);
}

export function useApiErrorMessage() {
  const { t, locale } = useI18n();

  function apiError(error: unknown, fallback: string): string {
    return formatApiError(error, fallback, locale.value, t);
  }

  return { apiError };
}
