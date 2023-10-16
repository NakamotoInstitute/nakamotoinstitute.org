import type {
  Locale as I18nLocale,
  LocaleParams as I18nLocaleParams,
} from "./i18n";

declare global {
  type Locale = I18nLocale;
  type LocaleParams<T = object, U = object> = I18nLocaleParams<T, U>;
}

type NonNullable<T> = T extends null ? never : T;
