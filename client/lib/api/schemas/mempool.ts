import { z } from "zod";
import { zAuthorIndex } from "./authors";
import { zTranslationData } from "./shared";

export const zMempoolSeries = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
  chapterTitle: z.boolean().default(false),
});
export type MempoolSeries = z.infer<typeof zMempoolSeries>;

export const zMempoolSeriesIndex = z.array(zMempoolSeries);

export const zMempoolPost = z.object({
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
  authors: zAuthorIndex,
  translations: z.array(zTranslationData),
  seriesIndex: z.number().int().min(1).nullable(),
  series: zMempoolSeries.nullable(),
  content: z.string(),
});
export type MempoolPost = z.infer<typeof zMempoolPost>;

export const zMempoolIndex = z.array(zMempoolPost);

export const zMempoolSeriesDetail = z.object({
  series: zMempoolSeries.extend({
    translations: z.array(zTranslationData),
  }),
  posts: zMempoolIndex,
});
