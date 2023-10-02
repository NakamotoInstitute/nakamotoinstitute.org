import { Metadata } from "next";
import { RootLayout } from "../components";

export async function generateMetadata(): Promise<Metadata> {
  const siteTitle = "Satoshi Nakamoto Institute";
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: siteTitle,
    },
    description: "Bitcoin scholarship",
  };
}

export default function MainLayout({
  params: { locale },
  children,
}: LocaleParams & {
  children: React.ReactNode;
}) {
  return <RootLayout locale={locale}>{children}</RootLayout>;
}
