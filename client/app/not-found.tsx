import NotFoundLayout from "@/app/components/NotFoundLayout";
import { urls } from "@/lib/urls";

import { RootLayout } from "./components/RootLayout";

const generateHref = (loc: Locale) => urls(loc).home;

export default function NotFound() {
  const locale: Locale = "en";

  return (
    <RootLayout locale={locale}>
      <NotFoundLayout locale={locale} generateHref={generateHref} />
    </RootLayout>
  );
}
