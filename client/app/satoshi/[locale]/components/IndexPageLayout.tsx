import { PageLayout, PageLayoutProps } from "@/app/components/PageLayout";

import { IndexHeader } from "./IndexHeader";
import { IndexNavigationProps } from "./IndexNavigation";

type IndexPageLayoutProps = PageLayoutProps & IndexNavigationProps;

export const IndexPageLayout = async ({
  t,
  type,
  sourceLinks,
  toggleLinks,
  children,
  ...rest
}: IndexPageLayoutProps) => {
  return (
    <PageLayout t={t} {...rest}>
      <IndexHeader
        t={t}
        type={type}
        sourceLinks={sourceLinks}
        toggleLinks={toggleLinks}
      />
      {children}
    </PageLayout>
  );
};
