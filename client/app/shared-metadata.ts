import { URL } from "url";

import { cdnUrl } from "@/lib/urls";

type OGImage = string | OGImageDescriptor | URL;
type OGImageDescriptor = {
  url: string | URL;
  secureUrl?: string | URL;
  alt?: string;
  type?: string;
  width?: string | number;
  height?: string | number;
};

export const openGraphImages: OGImage[] = [
  {
    url: cdnUrl("/img/sni_opengraph_1200.jpg"),
    width: 1200,
    height: 675,
  },
];
