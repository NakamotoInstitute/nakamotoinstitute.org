import { z } from "zod";
import { zAuthorIndexResponse } from "./authors";
import { zTranslationData } from "./shared";

export const zMempoolSeriesData = z.object({
  locale: z.string(),
  title: z.string(),
  slug: z.string(),
  chapterTitle: z.boolean().default(false),
});
export type MempoolSeries = z.infer<typeof zMempoolSeriesData>;

export const zMempoolSeriesIndexData = z.array(zMempoolSeriesData);

export const zMempoolPostData = z.object({
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
  authors: zAuthorIndexResponse,
  translations: z.array(zTranslationData),
  seriesIndex: z.number().int().min(1).nullable(),
  series: zMempoolSeriesData.nullable(),
  content: z.string(),
});
export type MempoolPost = z.infer<typeof zMempoolPostData>;

export const zMempoolIndexResponse = z.array(zMempoolPostData);

export const zMempoolSeriesFullModel = z.object({
  series: zMempoolSeriesData.extend({
    translations: z.array(zTranslationData),
  }),
  posts: zMempoolIndexResponse,
});
