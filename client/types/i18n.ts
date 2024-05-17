import { locales } from "@/i18n";

export type Locale = (typeof locales)[number];

type CapitalizeRegion<T> = T extends `${infer Lang}-${infer Region}`
  ? `${Lang}-${Uppercase<Region>}`
  : T;

export type CapitalizedLocale = CapitalizeRegion<Locale>;

export type LocaleParams<T = object, U = object> = {
  params: { locale: Locale } & T;
} & U;
