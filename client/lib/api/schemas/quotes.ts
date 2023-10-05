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

export const zQuoteCategoryBase = z.object({
  name: z.string(),
  slug: z.string(),
});
export type QuoteCategoryBase = z.infer<typeof zQuoteCategoryBase>;

export const zQuoteCategoryIndex = z.array(zQuoteCategoryBase);

export const zQuote = zQuoteBase.extend({
  categories: z.array(zQuoteCategoryBase),
});
export type Quote = z.infer<typeof zQuote>;

export const zQuoteCategory = z.object({
  category: zQuoteCategoryBase,
  quotes: z.array(zQuote),
});
export type QuoteCategory = z.infer<typeof zQuoteCategory>;
