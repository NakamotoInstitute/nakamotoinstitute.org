import Link from "next/link";

import { IndexLink } from "./IndexNavigation";

type ThreadPageHeaderProps = {
  title: string;
  sourceTitle: string;
  satoshiOnly: boolean;
  allLink: IndexLink;
  externalLink: string;
  children?: React.ReactNode;
};

export const ThreadPageHeader = ({
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
            <Link href={allLink.href}>View all {allLink.label}</Link>
          ) : (
            <Link href={{ query: { view: "satoshi" } }}>View Satoshi only</Link>
          )}
          <Link href={externalLink}>External link</Link>
        </div>
      </div>
    </>
  );
};
