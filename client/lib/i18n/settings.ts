import { defaultLocale, i18nLocales } from "@/i18n";

export const fallbackLng = "en";
export const defaultNS = "common";

type KeySeparator = string | false | undefined;

export function getOptions(
  lng = fallbackLng,
  ns: string | string[] = defaultNS,
) {
  return {
    // debug: true,
    supportedLngs: i18nLocales,
    keySeparator: false as KeySeparator,
    fallbackLng: defaultLocale,
    lng,
    fallbackNS: defaultNS,
    returnEmptyString: false,
    defaultNS,
    ns,
  };
}
