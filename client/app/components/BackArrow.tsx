import clsx from "clsx";

export function BackArrow(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="1em"
      height="1em"
      fill="none"
      className={clsx(props.className, "stroke-current")}
      viewBox="0 0 24 24"
      {...props}
    >
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.5}
        d="M20.25 12H3.75M10.5 5.25 3.75 12l6.75 6.75"
      />
    </svg>
  );
}
