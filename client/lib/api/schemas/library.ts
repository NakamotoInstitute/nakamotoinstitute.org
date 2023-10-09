import { z } from "zod";
import { zAuthorIndex } from "./authors";
import { zTranslations } from "./shared";

export const zFormat = z.enum(["pdf", "epub", "mobi", "txt"]);
export type LibraryFormat = z.infer<typeof zFormat>;

export const zGranularity = z.enum(["DAY", "MONTH", "YEAR"]);
export type Granularity = z.infer<typeof zGranularity>;

const zDocumentBase = z.object({
  slug: z.string(),
  title: z.string(),
  authors: zAuthorIndex,
  date: z.coerce.date(),
  granularity: zGranularity,
  external: z.string().nullable(),
  formats: z.array(zFormat),
  translations: zTranslations,
});

export const zDocument = zDocumentBase.extend({
  content: z.string(),
  subtitle: z.string().nullable(),
  displayTitle: z.string().nullable(),
  image: z.string().nullable(),
  imageAlt: z.string().nullable(),
});
export type Document = z.infer<typeof zDocument>;

export const zDocumentIndex = zDocumentBase.extend({
  hasContent: z.boolean(),
});
export type DocumentIndex = z.infer<typeof zDocumentIndex>;

export const zLibraryIndex = z.array(zDocumentIndex);
