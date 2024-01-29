import clsx from "clsx";
import { IBM_Plex_Mono } from "next/font/google";

import "../globals.css";

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-ibm-plex-mono",
  weight: ["400", "500"],
});

type RootLayoutProps = {
  locale: Locale;
  children: React.ReactNode;
};

export function RootLayout({ locale, children }: RootLayoutProps) {
  return (
    <html lang={locale} className={clsx(plexMono.variable, "font-sans")}>
      {children}
    </html>
  );
}
