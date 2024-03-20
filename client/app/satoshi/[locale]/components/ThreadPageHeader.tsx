import Link from "next/link";

import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

type ThreadPageHeaderProps = {
  locale: Locale;
  title: string;
  sourceTitle: string;
  satoshiOnly: boolean;
  allLink: AnchorProps;
  externalLink: string;
  children?: React.ReactNode;
};

export const ThreadPageHeader = async ({
  locale,
  sourceTitle,
  title,
  satoshiOnly,
  allLink,
  externalLink,
  children,
}: ThreadPageHeaderProps) => {
  const { t } = await i18nTranslation(locale);

  return (
    <>
      {children}
      <div className="mb-4 text-center">
        <p className="text-xl">{sourceTitle}</p>
        <h1 className="text-4xl">{title}</h1>
        <div className="flex flex-col gap-2">
          {satoshiOnly ? (
            <Link href={allLink.href}>{allLink.text}</Link>
          ) : (
            <Link href={{ query: { view: "satoshi" } }}>
              {t("View Satoshi only")}
            </Link>
          )}
          <Link href={externalLink}>{t("External link")}</Link>
        </div>
      </div>
    </>
  );
};
