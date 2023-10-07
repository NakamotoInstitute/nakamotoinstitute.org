import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import {
  zMempoolIndexResponse,
  zMempoolPostData,
  zMempoolSeriesIndexData,
  zMempoolSeriesFullModel,
  zSlugParamsResponse,
} from "./schemas";

export async function getMempoolPosts(locale: Locale) {
  const res = await fetchAPI(`/mempool?locale=${locale}`);
  return zMempoolIndexResponse.parse(await res.json());
}

export async function getMempoolPost(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zMempoolPostData.parse(await res.json());
}

export async function getMempoolParams() {
  const res = await fetchAPI("/mempool/params");
  return zSlugParamsResponse.parse(await res.json());
}

export async function getAllMempoolSeries(locale: Locale) {
  const res = await fetchAPI(`/mempool/series?locale=${locale}`);
  return zMempoolSeriesIndexData.parse(await res.json());
}

export async function getMempoolSeries(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/series/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zMempoolSeriesFullModel.parse(await res.json());
}

export async function getMempoolSeriesParams() {
  const res = await fetchAPI("/mempool/series/params");
  return zSlugParamsResponse.parse(await res.json());
}
