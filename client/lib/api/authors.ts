import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import {
  zAuthorIndexResponse,
  zAuthorDetailResponse,
  zSlugParamsResponse,
} from "./schemas";

export async function getAuthors(locale: Locale) {
  const res = await fetchAPI(`/authors?locale=${locale}`);
  return zAuthorIndexResponse.parse(await res.json());
}

export async function getAuthor(slug: string, locale: Locale) {
  const res = await fetchAPI(`/authors/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zAuthorDetailResponse.parse(await res.json());
}

export async function getAuthorParams() {
  const res = await fetchAPI("/authors/params");
  return zSlugParamsResponse.parse(await res.json());
}
