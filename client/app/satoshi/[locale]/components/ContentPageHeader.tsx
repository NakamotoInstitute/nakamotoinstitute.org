type ContentPageHeaderProps = {
  title: string;
  source: string;
  children?: React.ReactNode;
};

export const ContentPageHeader = async ({
  source,
  title,
  children,
}: ContentPageHeaderProps) => {
  return (
    <div className="mb-4">
      <p className="mb-1 text-lg small-caps">{source}</p>
      <h1 className="mb-4 text-3xl font-semibold md:text-4xl">{title}</h1>
      {children}
    </div>
  );
};
