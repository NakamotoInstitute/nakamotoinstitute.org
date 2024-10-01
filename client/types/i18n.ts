import { locales } from "@/i18n";

declare global {
  type Locale = (typeof locales)[number];
  type LocaleParams<T = object, U = object> = {
    params: { locale: Locale } & T;
  } & U;
}

type CapitalizeRegion<T> = T extends `${infer Lang}-${infer Region}`
  ? `${Lang}-${Uppercase<Region>}`
  : T;

export type CapitalizedLocale = CapitalizeRegion<Locale>;
