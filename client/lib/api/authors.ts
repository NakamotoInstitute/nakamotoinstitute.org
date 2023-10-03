import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import {
  authorIndexResponseSchema,
  authorDetailResponseSchema,
  slugParamsResponseSchema,
} from "./schemas";

export async function getAuthors(locale: Locale) {
  const res = await fetchAPI(`/authors?locale=${locale}`);
  return authorIndexResponseSchema.parse(await res.json());
}

export async function getAuthor(slug: string, locale: Locale) {
  const res = await fetchAPI(`/authors/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return authorDetailResponseSchema.parse(await res.json());
}

export async function getAuthorParams() {
  const res = await fetchAPI("/authors/params");
  return slugParamsResponseSchema.parse(await res.json());
}
