export const languages = {
  ar: "العربية",
  de: "Deutsch",
  en: "English",
  es: "Español",
  fa: "فارسی",
  fi: "Suomi",
  fr: "Français",
  he: "עברית",
  it: "Italiano",
  ko: "한국어",
  "pt-br": "Português Brasil",
  ru: "Русский",
  tr: "Türkçe",
  vi: "Tiếng Việt",
  "zh-cn": "简体中文",
} as const;

export const locales = [
  "ar",
  "de",
  "en",
  "es",
  "fa",
  "fi",
  "fr",
  "he",
  "it",
  "ko",
  "pt-br",
  "ru",
  "tr",
  "vi",
  "zh-cn",
] as const;

export const canonicalLocales = locales.map(
  (l) => Intl.getCanonicalLocales(l)[0],
);

export const defaultLocale = "en";

export function isLocale(value: string): value is (typeof locales)[number] {
  return (locales as readonly string[]).includes(value);
}

const rtlLocales = new Set(["ar", "fa", "he"]);

export function isRtl(locale: string): boolean {
  return rtlLocales.has(locale);
}
