import { z } from "zod";

export const zForumPostSource = z.enum(["p2pfoundation", "bitcointalk"]);
export type ForumPostSource = z.infer<typeof zForumPostSource>;

const zForumPostBase = z.object({
  date: z.coerce.date(),
  subject: z.string(),
  text: z.string(),
  source: zForumPostSource,
  sourceId: z.string(),
  url: z.string(),
  threadId: z.number().int().min(1),
  satoshiId: z.number().int().min(1).optional(),
  nestedLevel: z.number().int().min(0),
  posterName: z.string(),
  posterUrl: z.string().nullable(),
});
export type ThreadPost = z.infer<typeof zForumPostBase>;

export const zSatoshiForumPost = zForumPostBase.extend({
  satoshiId: z.number().int().min(1),
});
export type ForumPost = z.infer<typeof zSatoshiForumPost>;

export const zForumPostIndexResponse = z.array(zSatoshiForumPost);

export const zForumPostResponse = z.object({
  post: zSatoshiForumPost,
  previous: zSatoshiForumPost.nullable(),
  next: zSatoshiForumPost.nullable(),
});

export const zForumThreadBase = z.object({
  id: z.number().int().min(1),
  title: z.string(),
  source: zForumPostSource,
  date: z.coerce.date(),
});
export type ForumThreadBase = z.infer<typeof zForumThreadBase>;

export const zForumThreadIndexResponse = z.array(zForumThreadBase);

export const zForumThread = z.object({
  thread: zForumThreadBase,
  posts: z.array(zForumPostBase),
  previous: zForumThreadBase.nullable(),
  next: zForumThreadBase.nullable(),
});
