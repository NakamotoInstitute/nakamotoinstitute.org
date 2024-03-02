import { z } from "zod";

import { getLibraryIndex } from "./library";
import { getMempoolIndex } from "./mempool";
import { zLocale } from "./shared";

export const zAuthor = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
  content: z.string(),
});
export type Author = z.infer<typeof zAuthor>;

export const zAuthorIndex = z.array(zAuthor);

export function getAuthorIndex() {
  return zAuthorIndex;
}

export const zAuthorDetail = z.object({
  author: zAuthor,
  library: z.lazy(() => getLibraryIndex()),
  mempool: z.lazy(() => getMempoolIndex()),
  locales: z.array(zLocale),
});
