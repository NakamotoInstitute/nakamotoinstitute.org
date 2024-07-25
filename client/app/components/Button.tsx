import clsx from "clsx";
import Link from "next/link";

type ButtonLinkProps = {
  href: string;
  children: React.ReactNode;
  className?: string;
  target?: string;
  rel?: string;
};

export const ButtonLink = ({ href, children, className }: ButtonLinkProps) => {
  return (
    <Link
      href={href}
      className={clsx(
        "ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        "hover:bg-crimson h-10 bg-cardinal px-4 py-3 text-white hover:text-white",
        className,
      )}
    >
      {children}
    </Link>
  );
};
