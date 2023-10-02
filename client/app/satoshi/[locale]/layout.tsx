import { RootLayout } from "@/app/components";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const siteTitle = "Satoshi Nakamoto Institute";
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: `The Complete Satoshi | ${siteTitle}`,
    },
    description: "Bitcoin scholarship",
  };
}

export default function SatoshiLayout({
  params: { locale },
  children,
}: LocaleParams & {
  children: React.ReactNode;
}) {
  return <RootLayout locale={locale}>{children}</RootLayout>;
}
