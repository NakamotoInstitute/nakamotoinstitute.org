import { defaultLocale } from "@/i18n";
import fs from "fs/promises";
import path from "path";

type ContentDirectory = "pages";

export const getDirectoryFile = async (
  directory: ContentDirectory,
  slug: string,
  locale: Locale = defaultLocale,
) => {
  const dir = path.join("@/../content", directory);
  const filePath = path.join(dir, `${slug}.${locale}.md`);
  return fs.readFile(filePath, "utf-8");
};

export const getPage = async (slug: string, locale: Locale) => {
  let page = getDirectoryFile("pages", slug, locale);
  if (!page && locale !== defaultLocale) {
    page = getDirectoryFile("pages", slug, locale);
  }
  return page ?? null;
};
