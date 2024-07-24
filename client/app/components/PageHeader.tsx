type PageHeaderProps = {
  title: string;
  superTitle?: string;
  children?: React.ReactNode;
};

export function PageHeader({ title, superTitle, children }: PageHeaderProps) {
  return (
    <header className="mb-4">
      {superTitle ? (
        <h2 className="mb-1 text-lg small-caps">{superTitle}</h2>
      ) : null}
      <h1 className="mb-4 text-3xl font-semibold md:text-4xl">{title}</h1>
      {children}
    </header>
  );
}
