import { OpenGraph } from "next/dist/lib/metadata/types/opengraph-types";

import { cdnUrl } from "@/lib/urls";

export const openGraphImages: OpenGraph["images"] = [
  {
    url: cdnUrl("/img/sni_opengraph_1200.jpg"),
    width: 1200,
    height: 675,
  },
];
