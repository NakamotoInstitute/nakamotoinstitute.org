import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout, PageLayoutProps } from "@/app/components/PageLayout";

import { IndexLinks, IndexNavigation } from "./IndexNavigation";

type IndexPageLayoutProps = PageLayoutProps & {
  title: string;
  navLinks: IndexLinks;
};

export const IndexPageLayout = ({
  title,
  navLinks,
  children,
  ...rest
}: IndexPageLayoutProps) => {
  return (
    <PageLayout {...rest}>
      <PageHeader title={title}>
        <IndexNavigation links={navLinks} />
      </PageHeader>
      {children}
      <hr className="my-4" />
      <IndexNavigation links={navLinks} reverse />
    </PageLayout>
  );
};
