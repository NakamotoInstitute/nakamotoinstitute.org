import { TFunction } from "i18next";

import { ToggleLink } from "@/app/components/ToggleLink";

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
  children,
}: ThreadPageHeaderProps) => {
  return (
    <>
      <div className="mb-4">
        <p className="small-caps mb-1 text-lg">{sourceTitle}</p>
        <h1 className="mb-4 text-3xl font-semibold md:text-4xl">{title}</h1>
        <div className="flex items-center justify-between">
          {children}
          <ToggleLink
            label={t("satoshi_only")}
            href={satoshiOnly ? allLink.href : { query: { view: "satoshi" } }}
            active={satoshiOnly}
          />
        </div>
      </div>
    </>
  );
};
