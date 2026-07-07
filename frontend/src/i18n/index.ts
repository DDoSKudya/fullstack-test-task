import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import ru from "./locales/ru.json";

export type AppLocale = "en" | "ru";

const STORAGE_KEY = "locale";

function normalizeLocale(value: string | null | undefined): AppLocale {
  if (!value) {
    return "en";
  }
  return value.toLowerCase().startsWith("ru") ? "ru" : "en";
}

function resolveLocale(): AppLocale {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === "en" || stored === "ru") {
    return stored;
  }
  return normalizeLocale(navigator.language);
}

export const i18n = createI18n({
  legacy: false,
  locale: resolveLocale(),
  fallbackLocale: "en",
  messages: { en, ru },
});

export function setLocale(locale: AppLocale): void {
  i18n.global.locale.value = locale;
  localStorage.setItem(STORAGE_KEY, locale);
  document.documentElement.lang = locale;
}

setLocale(i18n.global.locale.value as AppLocale);
