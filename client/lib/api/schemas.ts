import { z } from "zod";

export const authorDataSchema = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
  content: z.string(),
});

export type AuthorData = z.infer<typeof authorDataSchema>;

export const authorIndexResponseSchema = z.array(authorDataSchema);

export const authorDetailResponseSchema = z.object({
  author: authorDataSchema,
});

export const slugParamsResponseSchema = z.array(
  z.object({
    locale: z.string(),
    slug: z.string(),
  }),
);

export const mempoolTranslationDataSchema = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
});

export const mempoolSeriesDataSchema = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
  chapterTitle: z.boolean().default(false),
});

export type MempoolSeries = z.infer<typeof mempoolSeriesDataSchema>;

export const mempoolPostDataSchema = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
  excerpt: z.string(),
  image: z.string().nullable(),
  imageAlt: z.string().nullable(),
  originalUrl: z.string().nullable(),
  originalSite: z.string().nullable(),
  translationUrl: z.string().nullable(),
  translationSite: z.string().nullable(),
  translationSiteUrl: z.string().nullable(),
  date: z.coerce.date(),
  added: z.coerce.date(),
  authors: authorIndexResponseSchema,
  translations: z.array(mempoolTranslationDataSchema),
  seriesIndex: z.number().int().min(1).nullable(),
  series: mempoolSeriesDataSchema.nullable(),
  content: z.string(),
});

export type MempoolPost = z.infer<typeof mempoolPostDataSchema>;

export const mempoolIndexResponseSchema = z.array(mempoolPostDataSchema);
