import { z } from "zod";

import { locales } from "@/i18n";

export const zLocale = z.string().refine(
  (val): val is Locale => {
    return locales.includes(val as Locale);
  },
  { message: "Invalid locale" },
);

const zSlugParam = z.object({
  locale: zLocale,
  slug: z.string(),
});
export type SlugParam = z.infer<typeof zSlugParam>;

export const zSlugParamsResponse = z.array(zSlugParam);

export const zTranslationData = z.object({
  locale: zLocale,
  title: z.string(),
  slug: z.string(),
});
export type TranslationData = z.infer<typeof zTranslationData>;

export const zTranslations = z.array(zTranslationData);

export const zTranslator = z.object({
  name: z.string(),
  url: z.string().nullable(),
  slug: z.string(),
});
export type Translator = z.infer<typeof zTranslator>;

export const zTranslators = z.array(zTranslator);
