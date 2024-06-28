import clsx from "clsx";
import { IBM_Plex_Mono, STIX_Two_Text } from "next/font/google";

import "../globals.css";

const stix = STIX_Two_Text({
  subsets: ["latin"],
  variable: "--font-stix",
  style: ["normal", "italic"],
});
const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-ibm-plex-mono",
  weight: ["400", "500", "600"],
});

type RootLayoutProps = {
  locale: Locale;
  children: React.ReactNode;
};

export function RootLayout({ locale, children }: RootLayoutProps) {
  return (
    <html
      lang={locale}
      className={clsx(
        stix.variable,
        plexMono.variable,
        "bg-cream font-serif text-dark",
      )}
    >
      {children}
    </html>
  );
}
