import { z } from "zod";

export const authorDataSchema = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
});

export const authorIndexResponseSchema = z.array(authorDataSchema);

export const authorDetailResponseSchema = z.object({
  author: authorDataSchema,
});

export const authorParamsResponseSchema = z.array(
  z.object({
    locale: z.string(),
    slug: z.string(),
  }),
);
