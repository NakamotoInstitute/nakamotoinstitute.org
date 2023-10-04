import { z } from "zod";

export const zAuthorData = z.object({
  name: z.string(),
  sortName: z.string(),
  slug: z.string(),
  content: z.string(),
});
export type Author = z.infer<typeof zAuthorData>;

export const zAuthorIndexResponse = z.array(zAuthorData);

export const zAuthorDetailResponse = z.object({ author: zAuthorData });
