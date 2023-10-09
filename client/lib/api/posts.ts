import { getNumericId } from "@/utils/strings";
import fetchAPI from "./fetchAPI";
import {
  ForumPostSource,
  zForumPostIndex,
  zForumThreadIndex,
  zForumThreadDetail,
  zForumPostDetail,
} from "./schemas/posts";

export async function getSatoshiPosts() {
  const res = await fetchAPI("/satoshi/posts");
  return zForumPostIndex.parse(await res.json());
}

export async function getForumPost(
  source: ForumPostSource,
  satoshiId: string | number,
) {
  const satoshiIdNum = getNumericId(satoshiId);
  const res = await fetchAPI(`/satoshi/posts/${source}/${satoshiIdNum}`);
  return zForumPostDetail.parse(await res.json());
}

export async function getSatoshiPostsBySource(source: ForumPostSource) {
  const res = await fetchAPI(`/satoshi/posts/${source}`);
  return zForumPostIndex.parse(await res.json());
}

export async function getForumThreads() {
  const res = await fetchAPI("/satoshi/posts/threads");
  return zForumThreadIndex.parse(await res.json());
}

export async function getForumThread(
  source: ForumPostSource,
  threadId: string | number,
  satoshiOnly: boolean = false,
) {
  const threadIdNum = getNumericId(threadId);
  const res = await fetchAPI(
    `/satoshi/posts/${source}/threads/${threadIdNum}?satoshi=${satoshiOnly}`,
  );
  return zForumThreadDetail.parse(await res.json());
}

export async function getForumThreadsBySource(source: ForumPostSource) {
  const res = await fetchAPI(`/satoshi/posts/${source}/threads`);
  return zForumThreadIndex.parse(await res.json());
}
