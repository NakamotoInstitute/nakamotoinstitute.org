import NotFoundLayout from "@/app/components/NotFoundLayout";
import { urls } from "@/lib/urls";

const generateHref = (loc: Locale) => urls(loc).satoshi.index;

export default function NotFound() {
  const locale: Locale = "en";

  return <NotFoundLayout locale={locale} generateHref={generateHref} />;
}
