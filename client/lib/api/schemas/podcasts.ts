import { z } from "zod";

export const zPodcastBase = z.object({
  slug: z.string(),
  name: z.string(),
  sortName: z.string(),
  description: z.string(),
  descriptionShort: z.string().nullable(),
  externalFeed: z.string().nullable(),
  defunct: z.boolean(),
});
export type PodcastBase = z.infer<typeof zPodcastBase>;

export const zEpisodeBase = z.object({
  slug: z.string(),
  title: z.string(),
  summary: z.string().nullable(),
  date: z.coerce.date(),
});
export type EpisodeBase = z.infer<typeof zEpisodeBase>;

export const zEpisodeIndex = z.array(zEpisodeBase);
export type EpisodeIndex = z.infer<typeof zEpisodeIndex>;

export const zPodcast = zPodcastBase.extend({
  spotifyUrl: z.string().nullable(),
  applePodcastsUrl: z.string().nullable(),
  fountainUrl: z.string().nullable(),
  onYoutube: z.boolean(),
  onRumble: z.boolean(),
});
export type Podcast = z.infer<typeof zPodcast>;

export const zEpisode = zEpisodeBase.extend({
  content: z.string(),
  duration: z.string().nullable(),
  notes: z.string().nullable(),
  youtubeId: z.string().nullable(),
  rumbleId: z.string().nullable(),
  mp3Url: z.string().nullable(),
  episodeNumber: z.number().nullable(),
  podcast: zPodcast,
});
export type Episode = z.infer<typeof zEpisode>;

export const zPodcastDetail = zPodcast.extend({
  episodes: zEpisodeIndex,
});
export type PodcastDetail = z.infer<typeof zPodcastDetail>;

export const zEpisodeParams = z.object({
  podcastSlug: z.string(),
  episodeSlug: z.string(),
});
export type EpisodeParams = z.infer<typeof zEpisodeParams>;

export const zEpisodeParamsIndex = z.array(zEpisodeParams);
export type EpisodeParamsIndex = z.infer<typeof zEpisodeParamsIndex>;

export const zPodcastIndex = z.array(zPodcastBase);
export type PodcastIndex = z.infer<typeof zPodcastIndex>;
