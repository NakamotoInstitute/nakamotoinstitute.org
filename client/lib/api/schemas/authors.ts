import { z } from "zod";
import { zLibraryIndex, zMempoolIndex } from ".";

export const zAuthor = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
  content: z.string(),
});
export type Author = z.infer<typeof zAuthor>;

export const zAuthorIndex = z.array(zAuthor);

export const zAuthorDetail = z.object({
  author: zAuthor,
  library: z.array(zLibraryIndex),
  mempool: z.array(zMempoolIndex),
});
