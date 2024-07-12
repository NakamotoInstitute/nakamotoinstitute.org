import { PageLayout, PageLayoutProps } from "@/app/components/PageLayout";

import { IndexHeader, IndexHeaderProps } from "./IndexHeader";

type IndexPageLayoutProps = PageLayoutProps & IndexHeaderProps;

export const IndexPageLayout = async ({
  t,
  title,
  sourceLinks,
  toggleLinks,
  children,
  ...rest
}: IndexPageLayoutProps) => {
  return (
    <PageLayout t={t} {...rest}>
      <IndexHeader
        t={t}
        title={title}
        sourceLinks={sourceLinks}
        toggleLinks={toggleLinks}
      />
      {children}
    </PageLayout>
  );
};
