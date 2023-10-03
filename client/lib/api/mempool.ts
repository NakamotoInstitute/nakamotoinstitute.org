import fetchAPI from "./fetchAPI";
import {
  mempoolIndexResponseSchema,
  mempoolPostDataSchema,
  slugParamsResponseSchema,
} from "./schemas";

export async function getMempoolPosts(locale: Locale) {
  const res = await fetchAPI(`/mempool?locale=${locale}`);
  return mempoolIndexResponseSchema.parse(await res.json());
}

export async function getMempoolPost(slug: string, locale: Locale) {
  const res = await fetchAPI(`/mempool/${slug}?locale=${locale}`);
  return mempoolPostDataSchema.parse(await res.json());
}

export async function getMempoolParams() {
  const res = await fetchAPI(`/mempool/params`);
  return slugParamsResponseSchema.parse(await res.json());
}
