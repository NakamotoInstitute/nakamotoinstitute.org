import { cache } from "react";

import fetchAPI from "./fetchAPI";
import {
  zEpisode,
  zEpisodeParamsIndex,
  zPodcastDetail,
  zPodcastIndex,
} from "./schemas/podcasts";

export async function getPodcasts() {
  const res = await fetchAPI(`/podcasts`);
  return zPodcastIndex.parse(await res.json());
}

export async function getHomePodcasts() {
  const res = await fetchAPI(`/podcasts/home`);
  return zPodcastIndex.parse(await res.json());
}

export async function getEpisodes() {
  const res = await fetchAPI(`/podcasts/episodes`);
  return zEpisodeParamsIndex.parse(await res.json());
}

export const getPodcast = cache(async (slug: string) => {
  const res = await fetchAPI(`/podcasts/${slug}`);
  return zPodcastDetail.parse(await res.json());
});

export const getEpisode = cache(
  async (podcastSlug: string, episodeSlug: string) => {
    const res = await fetchAPI(`/podcasts/${podcastSlug}/${episodeSlug}`);
    return zEpisode.parse(await res.json());
  },
);

export async function getPodcastFeed(podcastSlug: string) {
  const res = await fetchAPI(`/podcasts/${podcastSlug}/feed`);
  return await res.text();
}
