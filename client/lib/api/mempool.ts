import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import {
  mempoolIndexResponseSchema,
  mempoolPostDataSchema,
  mempoolSeriesIndexDataSchema,
  mempoolSeriesResponseSchema,
  slugParamsResponseSchema,
} from "./schemas";

export async function getMempoolPosts(locale: Locale) {
  const res = await fetchAPI(`/mempool?locale=${locale}`);
  return mempoolIndexResponseSchema.parse(await res.json());
}

export async function getMempoolPost(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return mempoolPostDataSchema.parse(await res.json());
}

export async function getMempoolParams() {
  const res = await fetchAPI("/mempool/params");
  return slugParamsResponseSchema.parse(await res.json());
}

export async function getAllMempoolSeries(locale: Locale) {
  const res = await fetchAPI(`/mempool/series?locale=${locale}`);
  return mempoolSeriesIndexDataSchema.parse(await res.json());
}

export async function getMempoolSeries(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/series/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return mempoolSeriesResponseSchema.parse(await res.json());
}

export async function getMempoolSeriesParams() {
  const res = await fetchAPI("/mempool/series/params");
  return slugParamsResponseSchema.parse(await res.json());
}
