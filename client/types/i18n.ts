import { locales } from "@/i18n";

export type Locale = (typeof locales)[number];

export type LocaleParams<T = object, U = object> = {
  params: { locale: Locale } & T;
} & U;
