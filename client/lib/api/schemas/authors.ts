import { z } from "zod";

import { zLibraryIndex } from "./library";
import { zMempoolIndex } from "./mempool";
import { zLocale } from "./shared";

export const zAuthor = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
});
export type Author = z.infer<typeof zAuthor>;

export const zAuthorIndex = z.array(zAuthor);

export const zAuthorDetail = z.object({
  author: zAuthor,
  library: z.lazy(() => zLibraryIndex),
  mempool: z.lazy(() => zMempoolIndex),
  locales: z.array(zLocale),
});
