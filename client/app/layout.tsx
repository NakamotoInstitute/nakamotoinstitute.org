import { Metadata } from "next";

import { RootLayout } from "@/app/components/RootLayout";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

export default function SatoshiLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
