import { notFound } from "next/navigation";

import fetchAPI from "./fetchAPI";
import {
  zMempoolIndex,
  zMempoolPost,
  zMempoolSeriesDetail,
  zMempoolSeriesIndex,
} from "./schemas/mempool";
import { zSlugParamsResponse } from "./schemas/shared";

export async function getMempoolPosts(locale: Locale) {
  const res = await fetchAPI(`/mempool?locale=${locale}`);
  return zMempoolIndex.parse(await res.json());
}

export async function getMempoolPost(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zMempoolPost.parse(await res.json());
}

export async function getLatestMempoolPosts(locale: Locale) {
  const res = await fetchAPI(`/mempool/latest?locale=${locale}`);
  if (res.status === 404) {
    return [];
  }
  return zMempoolIndex.parse(await res.json());
}

export async function getMempoolParams() {
  const res = await fetchAPI("/mempool/params");
  return zSlugParamsResponse.parse(await res.json());
}

export async function getAllMempoolSeries(locale: Locale) {
  const res = await fetchAPI(`/mempool/series?locale=${locale}`);
  return zMempoolSeriesIndex.parse(await res.json());
}

export async function getMempoolSeries(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/series/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zMempoolSeriesDetail.parse(await res.json());
}

export async function getMempoolSeriesParams() {
  const res = await fetchAPI("/mempool/series/params");
  return zSlugParamsResponse.parse(await res.json());
}

export async function getMempoolFeed(
  locale: Locale,
  format: "rss" | "atom" = "rss",
) {
  const res = await fetchAPI(`/mempool/feed?locale=${locale}&format=${format}`);
  return await res.text();
}
