"use client";

import { ErrorFallback } from "@/app/components/ErrorFallback";

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function Error({ error: _error, reset }: ErrorProps) {
  return (
    <body className="flex min-h-screen flex-col">
      <ErrorFallback reset={reset} />
    </body>
  );
}
