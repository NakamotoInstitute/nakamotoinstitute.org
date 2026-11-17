"use client";

import { ErrorFallback } from "@/app/components/ErrorFallback";

import "./globals.css";

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({
  error: _error,
  reset,
}: GlobalErrorProps) {
  return (
    <html lang="en" className="bg-cream text-dark font-serif">
      <body className="flex min-h-screen flex-col">
        <ErrorFallback reset={reset} />
      </body>
    </html>
  );
}
