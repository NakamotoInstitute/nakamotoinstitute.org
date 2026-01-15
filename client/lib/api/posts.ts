import { cache } from "react";

import { notFound } from "next/navigation";

import { getNumericId } from "@/utils/strings";

import fetchAPI from "./fetchAPI";
import {
  ForumPostSource,
  zForumPostDetail,
  zForumPostIndex,
  zForumThreadDetail,
  zForumThreadIndex,
} from "./schemas/posts";

export async function getSatoshiPosts() {
  const res = await fetchAPI("/satoshi/posts");
  return zForumPostIndex.parse(await res.json());
}

export const getForumPost = cache(
  async (source: ForumPostSource, satoshiId: string | number) => {
    const satoshiIdNum = getNumericId(satoshiId);
    const res = await fetchAPI(`/satoshi/posts/${source}/${satoshiIdNum}`);
    if (res.status === 404 || res.status === 422) {
      notFound();
    }
    return zForumPostDetail.parse(await res.json());
  },
);

export async function getSatoshiPostsBySource(source: ForumPostSource) {
  const res = await fetchAPI(`/satoshi/posts/${source}`);
  return zForumPostIndex.parse(await res.json());
}

export async function getForumThreads() {
  const res = await fetchAPI("/satoshi/posts/threads");
  return zForumThreadIndex.parse(await res.json());
}

export const getForumThread = cache(
  async (
    source: ForumPostSource,
    threadId: string | number,
    satoshiOnly: boolean = false,
  ) => {
    const threadIdNum = getNumericId(threadId);
    const res = await fetchAPI(
      `/satoshi/posts/${source}/threads/${threadIdNum}?satoshi=${satoshiOnly}`,
    );
    if (res.status === 404 || res.status === 422) {
      notFound();
    }
    return zForumThreadDetail.parse(await res.json());
  },
);

export async function getForumThreadsBySource(source: ForumPostSource) {
  const res = await fetchAPI(`/satoshi/posts/${source}/threads`);
  if (res.status === 404) {
    notFound();
  }
  return zForumThreadIndex.parse(await res.json());
}
