import { z } from "zod";

const zSlugParam = z.object({
  locale: z.string(),
  slug: z.string(),
});
export type SlugParam = z.infer<typeof zSlugParam>;

export const zSlugParamsResponse = z.array(zSlugParam);

export const zTranslationData = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
});
export type TranslationData = z.infer<typeof zTranslationData>;

export const zTranslations = z.array(zTranslationData);
