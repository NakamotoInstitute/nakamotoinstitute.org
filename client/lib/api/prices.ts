import Big from "big.js";
import { z } from "zod";

const zPriceDatum = z
  .object({
    PriceUSD: z.string(),
    time: z.coerce.date(),
  })
  .transform(({ PriceUSD, time }) => ({
    price: Big(PriceUSD),
    date: time,
  }));

export type Price = z.infer<typeof zPriceDatum>;

const zPriceData = z.array(zPriceDatum);

const PRICE_API_URL =
  "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=PriceUSD&frequency=1d&page_size=10000";

export const fetchPriceHistory = async (revalidate: number) => {
  try {
    const res = await fetch(PRICE_API_URL, { next: { revalidate } });
    if (!res.ok) {
      throw new Error(`API response status: ${res.status}`);
    }
    const data = await res.json();
    return zPriceData.parseAsync(data.data);
  } catch (err) {
    console.error("Error fetching price history:", err);
    throw err;
  }
};
