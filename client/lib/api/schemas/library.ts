import { z } from "zod";

import { getAuthorIndex } from "./authors";
import { zTranslations, zTranslators } from "./shared";

export const zFormat = z.enum(["pdf", "epub", "mobi", "txt"]);
export type LibraryFormat = z.infer<typeof zFormat>;

export const zGranularity = z.enum(["DAY", "MONTH", "YEAR"]);
export type Granularity = z.infer<typeof zGranularity>;

export const zDocumentFormat = z.object({
  url: z.string(),
  type: zFormat,
});
export type DocumentFormat = z.infer<typeof zDocumentFormat>;

const zDocumentBase = z.object({
  slug: z.string(),
  title: z.string(),
  authors: z.lazy(() => getAuthorIndex()),
  date: z.coerce.date(),
  granularity: zGranularity,
  external: z.string().nullable(),
  formats: z.array(zDocumentFormat),
  translations: zTranslations,
});

export const zDocument = zDocumentBase.extend({
  content: z.string(),
  subtitle: z.string().nullable(),
  displayTitle: z.string().nullable(),
  displayDate: z.string().nullable(),
  image: z.string().nullable(),
  imageAlt: z.string().nullable(),
  hasMath: z.boolean(),
  translators: zTranslators,
});
export type Document = z.infer<typeof zDocument>;

export const zDocumentIndex = zDocumentBase.extend({
  hasContent: z.boolean(),
});
export type DocumentIndex = z.infer<typeof zDocumentIndex>;

export const zLibraryIndex = z.array(zDocumentIndex);

export function getLibraryIndex() {
  return zLibraryIndex;
}
