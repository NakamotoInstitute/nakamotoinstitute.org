import { TFunction } from "i18next";
import Link from "next/link";

type ThreadPageHeaderProps = {
  t: TFunction<string, string>;
  title: string;
  sourceTitle: string;
  satoshiOnly: boolean;
  allLink: AnchorProps;
  externalLink: string;
  children?: React.ReactNode;
};

export const ThreadPageHeader = async ({
  t,
  sourceTitle,
  title,
  satoshiOnly,
  allLink,
  externalLink,
  children,
}: ThreadPageHeaderProps) => {
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
              {t("view_satoshi_only")}
            </Link>
          )}
          <Link href={externalLink}>{t("external_link")}</Link>
        </div>
      </div>
    </>
  );
};
