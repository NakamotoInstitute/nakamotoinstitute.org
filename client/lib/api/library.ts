import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import {
  zLibraryData,
  zLibraryIndexResponse,
  zSlugParamsResponse,
} from "./schemas";

export async function getLibraryDocs(locale: Locale) {
  const res = await fetchAPI(`/library?locale=${locale}`);
  return zLibraryIndexResponse.parse(await res.json());
}

export async function getLibraryDoc(slug: string, locale: Locale) {
  const res = await fetchAPI(`/library/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zLibraryData.parse(await res.json());
}

export async function getLibraryParams() {
  const res = await fetchAPI("/library/params");
  return zSlugParamsResponse.parse(await res.json());
}
