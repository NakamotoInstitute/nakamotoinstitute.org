type PageHeaderProps = {
  title: string;
  superTitle?: string;
  children?: React.ReactNode;
};

export function PageHeader({ title, superTitle, children }: PageHeaderProps) {
  return (
    <header className="text-center">
      {superTitle ? <h2 className="text-xl">{superTitle}</h2> : null}
      <h1 className="mb-2 text-4xl font-semibold">{title}</h1>
      {children}
      <hr className="my-4" />
    </header>
  );
}
