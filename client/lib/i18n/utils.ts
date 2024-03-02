import { locales } from "@/i18n";

type LocaleParam = { locale: Locale; [key: string]: unknown };
type CallbackResponse = (locale: Locale) => LocaleParam[];
type AsyncCallbackResponse = (locale: Locale) => Promise<LocaleParam[]>;

export const getLocaleParams = async (
  callback?: CallbackResponse | AsyncCallbackResponse,
): Promise<LocaleParam[]> => {
  return (
    await Promise.all(
      locales.map(async (locale) => {
        const result = callback ? callback(locale) : { locale };
        return result instanceof Promise ? await result : result;
      }),
    )
  ).flat();
};

export const getDir = (locale: Locale) => {
  return ["ar", "fa", "he"].includes(locale) ? "rtl" : "ltr";
};

export const generateHrefLangs = (
  _locales: Locale[],
  generateHref: (_locale: Locale) => string,
) => {
  return _locales.reduce(
    (acc, locale) => {
      acc[locale] = generateHref(locale);
      return acc;
    },
    {} as Record<Locale, string>,
  );
};
