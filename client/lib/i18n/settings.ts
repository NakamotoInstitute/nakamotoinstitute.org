import { defaultLocale, locales } from "@/i18n";

export const fallbackLng = "en";
export const languages = locales;
export const defaultNS = "common";

type KeySeparator = string | false | undefined;

export function getOptions(
  lng = fallbackLng,
  ns: string | string[] = defaultNS,
) {
  return {
    // debug: true,
    supportedLngs: languages,
    keySeparator: false as KeySeparator,
    fallbackLng: defaultLocale,
    lng,
    fallbackNS: defaultNS,
    returnEmptyString: false,
    defaultNS,
    ns,
  };
}
