import clsx from "clsx";

export function ArrowLeft(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="1.25em"
      height="1.25em"
      fill="none"
      className={clsx(props.className, "stroke-current")}
      viewBox="0 0 20 20"
      {...props}
    >
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.8346 10.0003H4.16797M4.16797 10.0003L10.0013 15.8337M4.16797 10.0003L10.0013 4.16699"
      />
    </svg>
  );
}
