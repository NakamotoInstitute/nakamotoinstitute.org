import { cache } from "react";

import { notFound } from "next/navigation";

import fetchAPI from "./fetchAPI";
import { zAuthorDetail, zAuthorIndex } from "./schemas/authors";
import { zSlugParamsResponse } from "./schemas/shared";

export async function getAuthors(locale: Locale) {
  const res = await fetchAPI(`/authors?locale=${locale}`);
  return zAuthorIndex.parse(await res.json());
}

export const getAuthor = cache(async (slug: string, locale: Locale) => {
  const res = await fetchAPI(`/authors/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zAuthorDetail.parse(await res.json());
});

export async function getAuthorParams() {
  const res = await fetchAPI("/authors/params");
  return zSlugParamsResponse.parse(await res.json());
}
