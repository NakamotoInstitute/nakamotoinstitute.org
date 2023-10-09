import { z } from "zod";

export const zEpisode = z.object({
  slug: z.string(),
  title: z.string(),
  date: z.coerce.date(),
  content: z.string(),
  duration: z.string(),
  summary: z.string(),
  notes: z.string(),
  youtubeId: z.string(),
});
export type Episode = z.infer<typeof zEpisode>;

export const zPodcastIndex = z.array(zEpisode);
