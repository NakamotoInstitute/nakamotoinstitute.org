import { defaultLocale } from "@/i18n";
import fs from "fs/promises";
import path from "path";

type ContentDirectory = "pages";

export const getDirectoryFile = async (
  directory: ContentDirectory,
  slug: string,
  locale: Locale = defaultLocale,
) => {
  try {
    const dir = path.join("@/../content", directory);
    const filePath = path.join(dir, `${slug}.${locale}.md`);
    return await fs.readFile(filePath, "utf-8");
  } catch {
    return null;
  }
};

export const getPage = async (slug: string, locale: Locale) => {
  let page = await getDirectoryFile("pages", slug, locale);
  if (!page && locale !== defaultLocale) {
    page = await getDirectoryFile("pages", slug);
  }
  return page ?? "";
};
