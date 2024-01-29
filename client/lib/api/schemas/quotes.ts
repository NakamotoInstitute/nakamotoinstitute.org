import { z } from "zod";

import { zEmailSource } from "./emails";
import { zForumPostSource } from "./posts";

const zQuoteItem = z.object({
  satoshiId: z.number().int().min(0),
  subject: z.string(),
});

const zQuoteEmail = zQuoteItem.extend({
  source: zEmailSource,
});

const zQuoteForumPost = zQuoteItem.extend({
  source: zForumPostSource,
});

const zQuoteBase = z.object({
  whitepaper: z.boolean(),
  text: z.string(),
  post: zQuoteForumPost.nullable(),
  email: zQuoteEmail.nullable(),
  date: z.coerce.date(),
});

export const zQuoteCategory = z.object({
  name: z.string(),
  slug: z.string(),
});
export type QuoteCategory = z.infer<typeof zQuoteCategory>;

export const zQuoteCategoryIndex = z.array(zQuoteCategory);

export const zQuote = zQuoteBase.extend({
  categories: z.array(zQuoteCategory),
});
export type Quote = z.infer<typeof zQuote>;

export const zQuoteCategoryDetail = z.object({
  category: zQuoteCategory,
  quotes: z.array(zQuote),
});
