import clsx from "clsx";

export type ArrowDirection = "left" | "right" | "back";

export type ArrowProps = React.SVGProps<SVGSVGElement> & {
  direction: ArrowDirection;
};

export function Arrow({ direction, ...props }: ArrowProps) {
  const isBack = direction === "back";

  const pathProps = {
    left: {
      d: "M15.8346 10.0003H4.16797M4.16797 10.0003L10.0013 15.8337M4.16797 10.0003L10.0013 4.16699",
    },
    right: {
      d: "M4.16797 10.0003H15.8346M15.8346 10.0003L10.0013 4.16699M15.8346 10.0003L10.0013 15.8337",
    },
    back: {
      strokeWidth: 1.5,
      d: "M20.25 12H3.75M10.5 5.25 3.75 12l6.75 6.75",
    },
  }[direction];

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={isBack ? "1em" : "1.25em"}
      height={isBack ? "1em" : "1.25em"}
      fill="none"
      className={clsx(props.className, "stroke-current")}
      viewBox={isBack ? "0 0 24 24" : "0 0 20 20"}
      {...props}
    >
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        {...pathProps}
      />
    </svg>
  );
}
