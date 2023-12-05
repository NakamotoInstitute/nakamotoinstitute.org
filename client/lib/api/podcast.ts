import { notFound } from "next/navigation";
import fetchAPI from "./fetchAPI";
import { zEpisode, zPodcastIndex } from "./schemas/podcast";

export async function getEpisodes() {
  const res = await fetchAPI(`/podcast`);
  return zPodcastIndex.parse(await res.json());
}

export async function getEpisode(slug: string) {
  const res = await fetchAPI(`/podcast/${slug}`);
  if (res.status === 404) {
    notFound();
  }
  return zEpisode.parse(await res.json());
}
