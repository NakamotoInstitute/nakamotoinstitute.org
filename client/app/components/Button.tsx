import clsx from "clsx";
import Link, { LinkProps } from "next/link";

type ButtonLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  keyof LinkProps
> &
  LinkProps & {
    className?: string;
    variant?: "primary" | "secondary";
  };

export const ButtonLink = ({
  className,
  variant = "primary",
  href,
  children,
}: ButtonLinkProps) => {
  return (
    <Link
      href={href}
      className={clsx(
        "ring-offset-background focus-visible:ring-ring inline-flex h-10 items-center justify-center whitespace-nowrap px-4 py-3 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
        {
          "bg-cardinal text-white hover:bg-crimson hover:text-white":
            variant === "primary",
          "bg-white text-cardinal hover:text-dark": variant === "secondary",
        },
        className,
      )}
    >
      {children}
    </Link>
  );
};
