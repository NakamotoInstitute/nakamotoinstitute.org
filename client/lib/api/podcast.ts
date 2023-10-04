import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import { zEpisodeData, zEpisodeIndex } from "./schemas";

export async function getEpisodes() {
  const res = await fetchAPI(`/podcast`);
  return zEpisodeIndex.parse(await res.json());
}

export async function getEpisode(slug: string) {
  const res = await fetchAPI(`/podcast/${slug}`);
  if (res.status === 404) {
    notFound();
  }
  return zEpisodeData.parse(await res.json());
}
