import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import { zAuthorIndex, zAuthorDetail, zSlugParamsResponse } from "./schemas";

export async function getAuthors(locale: Locale) {
  const res = await fetchAPI(`/authors?locale=${locale}`);
  return zAuthorIndex.parse(await res.json());
}

export async function getAuthor(slug: string, locale: Locale) {
  const res = await fetchAPI(`/authors/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zAuthorDetail.parse(await res.json());
}

export async function getAuthorParams() {
  const res = await fetchAPI("/authors/params");
  return zSlugParamsResponse.parse(await res.json());
}
