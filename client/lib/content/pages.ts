import { defaultLocale } from "@/i18n";
import { getDirectoryFile } from "./shared";

export const getPage = async (slug: string, locale: Locale) => {
  let page = getDirectoryFile("pages", slug, locale);
  if (!page && locale !== defaultLocale) {
    page = getDirectoryFile("pages", slug, locale);
  }
  return page ?? null;
};
