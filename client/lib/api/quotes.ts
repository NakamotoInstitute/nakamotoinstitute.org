import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import { zQuoteCategoryDetail, zQuoteCategoryIndex } from "./schemas/quotes";

export async function getQuoteCategories() {
  const res = await fetchAPI(`/satoshi/quotes`);
  return zQuoteCategoryIndex.parse(await res.json());
}

export async function getQuoteCategory(slug: string) {
  const res = await fetchAPI(`/satoshi/quotes/${slug}`);
  if (res.status === 404) {
    notFound();
  }
  return zQuoteCategoryDetail.parse(await res.json());
}
