import { z } from "zod";
import { zAuthorIndexResponse } from "./authors";
import { zTranslations } from "./shared";

export const zFormat = z.enum(["pdf", "epub", "mobi", "txt"]);
export type LibraryFormat = z.infer<typeof zFormat>;

export const zGranularity = z.enum(["DAY", "MONTH", "YEAR"]);
export type Granularity = z.infer<typeof zGranularity>;

const zLibraryBaseData = z.object({
  slug: z.string(),
  title: z.string(),
  authors: zAuthorIndexResponse,
  date: z.coerce.date(),
  granularity: zGranularity,
  external: z.string().nullable(),
  formats: z.array(zFormat),
  translations: zTranslations,
});

export const zLibraryIndexDocData = zLibraryBaseData.extend({
  hasContent: z.boolean(),
});
export type LibraryIndexDoc = z.infer<typeof zLibraryIndexDocData>;

export const zLibraryData = zLibraryBaseData.extend({
  content: z.string(),
  subtitle: z.string().nullable(),
  displayTitle: z.string().nullable(),
  image: z.string().nullable(),
  imageAlt: z.string().nullable(),
});
export type LibraryDoc = z.infer<typeof zLibraryData>;

export const zLibraryIndexResponse = z.array(zLibraryIndexDocData);
