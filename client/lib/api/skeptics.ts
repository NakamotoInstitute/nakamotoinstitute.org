import fetchAPI from "./fetchAPI";
import { zPriceData, zSkepticsIndex } from "./schemas/skeptics";

export async function getSkeptics() {
  const res = await fetchAPI(`/skeptics`);
  return zSkepticsIndex.parse(await res.json());
}

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
