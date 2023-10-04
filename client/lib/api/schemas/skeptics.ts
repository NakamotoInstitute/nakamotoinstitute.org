import Big from "big.js";
import { z } from "zod";

export const zSkepticData = z.object({
  name: z.string(),
  slug: z.string(),
  title: z.string(),
  article: z.string().nullable(),
  date: z.coerce.date(),
  source: z.string(),
  excerpt: z.string().nullable(),
  link: z.array(z.string()),
  mediaEmbed: z.string().nullable(),
  twitterScreenshot: z.boolean(),
  waybackLink: z.string().nullable(),
});
export type Skeptic = z.infer<typeof zSkepticData>;

export const zSkepticDataResponse = z.array(zSkepticData);

export const zPriceDatum = z
  .object({
    PriceUSD: z.string(),
    time: z.coerce.date(),
  })
  .transform(({ PriceUSD, time }) => ({
    price: Big(PriceUSD),
    date: time,
  }));
export type Price = z.infer<typeof zPriceDatum>;

export const zPriceData = z.array(zPriceDatum);
