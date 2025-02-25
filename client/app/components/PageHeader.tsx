import clsx from "clsx";

type PageHeaderProps = {
  title: string;
  superTitle?: string;
  subtitle?: string;
  children?: React.ReactNode;
};

export function PageHeader({
  title,
  superTitle,
  subtitle,
  children,
}: PageHeaderProps) {
  return (
    <header className="mb-4">
      {superTitle ? (
        <h2 className="small-caps mb-1 text-lg">{superTitle}</h2>
      ) : null}
      <h1
        className={clsx(
          "text-3xl font-semibold md:text-4xl",
          !subtitle && "mb-4",
        )}
      >
        {title}
      </h1>
      {subtitle ? (
        <h2 className="mb-4 text-lg font-medium md:text-xl">{subtitle}</h2>
      ) : null}
      {children}
    </header>
  );
}
