import fs from "fs/promises";
import path from "path";

import { defaultLocale } from "@/i18n";
import { CapitalizedLocale } from "@/types/i18n";
import { formatLocale } from "@/utils/strings";

type ContentDirectory = "pages";

export const getDirectoryFile = async (
  directory: ContentDirectory,
  slug: string,
  locale: CapitalizedLocale = defaultLocale,
) => {
  try {
    const dir = path.join("@/../content", directory);
    const filePath = path.join(dir, locale, `${slug}.md`);
    return await fs.readFile(filePath, "utf-8");
  } catch {
    return null;
  }
};

export const getPage = async (slug: string, locale: Locale) => {
  const formattedLocale = formatLocale(locale);
  let page = await getDirectoryFile("pages", slug, formattedLocale);
  if (!page && locale !== defaultLocale) {
    page = await getDirectoryFile("pages", slug);
  }
  return page ?? "";
};
