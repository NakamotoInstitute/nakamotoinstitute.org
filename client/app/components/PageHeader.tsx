type PageHeaderProps = {
  title: string;
  superTitle?: string;
  children?: React.ReactNode;
};

export function PageHeader({ title, superTitle, children }: PageHeaderProps) {
  return (
    <header className="mb-8">
      {superTitle ? <h2 className="text-xl">{superTitle}</h2> : null}
      <h1 className="mb-5 text-4xl font-semibold">{title}</h1>
      {children}
    </header>
  );
}
