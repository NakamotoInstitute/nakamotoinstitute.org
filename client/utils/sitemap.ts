import { locales as allLocales } from "@/i18n";
import { CapitalizedLocale, Locale } from "@/types/i18n";
import { formatLocale } from "@/utils/strings";

export type LocalizedUrlObject = { [K in CapitalizedLocale]: string };

export function createLocalizedUrlObject(
  urlFunc: (locale: Locale) => string,
  locales: Locale[] = [...allLocales],
): LocalizedUrlObject {
  return locales.reduce((obj, locale) => {
    obj[formatLocale(locale)] = urlFunc(locale);
    return obj;
  }, {} as LocalizedUrlObject);
}
