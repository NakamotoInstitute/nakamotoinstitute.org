import { z } from "zod";

export const zForumPostSource = z.enum(["p2pfoundation", "bitcointalk"]);
export type ForumPostSource = z.infer<typeof zForumPostSource>;
