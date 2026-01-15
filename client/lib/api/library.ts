import { cache } from "react";

import { notFound } from "next/navigation";

import fetchAPI from "./fetchAPI";
import {
  zDocNodeSlugParamsResponse,
  zDocument,
  zDocumentNode,
  zLibraryIndex,
} from "./schemas/library";
import { zSlugParamsResponse } from "./schemas/shared";

export async function getLibraryDocs(locale: Locale) {
  const res = await fetchAPI(`/library?locale=${locale}`);
  return zLibraryIndex.parse(await res.json());
}

export async function getHomeLibraryDocs(locale: Locale) {
  const res = await fetchAPI(`/library/home?locale=${locale}`);
  return zLibraryIndex.parse(await res.json());
}

export const getLibraryDoc = cache(async (slug: string, locale: Locale) => {
  const res = await fetchAPI(`/library/${slug}?locale=${locale}`);
  if (res.status === 404) {
    notFound();
  }
  return zDocument.parse(await res.json());
});

export const getLibraryDocNode = cache(
  async (slug: string, docSlug: string, locale: Locale) => {
    const res = await fetchAPI(`/library/${docSlug}/${slug}?locale=${locale}`);
    if (res.status === 404) {
      notFound();
    }
    return zDocumentNode.parse(await res.json());
  },
);

export async function getLibraryParams() {
  const res = await fetchAPI("/library/params");
  return zSlugParamsResponse.parse(await res.json());
}

export async function getLibraryNodeParams() {
  const res = await fetchAPI("/library/params/nodes");
  return zDocNodeSlugParamsResponse.parse(await res.json());
}
