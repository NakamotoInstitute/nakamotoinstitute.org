import { z } from "zod";

export const FORUM_POST_SOURCES = ["p2pfoundation", "bitcointalk"] as const;
export const zForumPostSource = z.enum(FORUM_POST_SOURCES);
export type ForumPostSource = z.infer<typeof zForumPostSource>;

const zForumPost = z.object({
  date: z.coerce.date(),
  subject: z.string(),
  text: z.string(),
  source: zForumPostSource,
  sourceId: z.string(),
  url: z.string(),
  threadId: z.number().int().min(1),
  satoshiId: z.number().int().min(1).nullable(),
  nestedLevel: z.number().int().min(0),
  posterName: z.string(),
  posterUrl: z.string().nullable(),
});
export type ForumPost = z.infer<typeof zForumPost>;

export const zSatoshiForumPost = zForumPost.extend({
  satoshiId: z.number().int().min(1),
});
export type SatoshiForumPost = z.infer<typeof zSatoshiForumPost>;

export const zForumPostIndex = z.array(zSatoshiForumPost);

export const zForumPostDetail = z.object({
  post: zSatoshiForumPost,
  previous: zSatoshiForumPost.nullable(),
  next: zSatoshiForumPost.nullable(),
});
export type ForumPostDetail = z.infer<typeof zForumPostDetail>;

export const zForumThread = z.object({
  id: z.number().int().min(1),
  title: z.string(),
  source: zForumPostSource,
  date: z.coerce.date(),
  url: z.string(),
});
export type ForumThread = z.infer<typeof zForumThread>;

export const zForumThreadIndex = z.array(zForumThread);

export const zForumThreadDetail = z.object({
  thread: zForumThread,
  posts: z.array(zForumPost),
  previous: zForumThread.nullable(),
  next: zForumThread.nullable(),
});
