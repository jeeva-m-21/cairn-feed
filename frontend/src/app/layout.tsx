import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cairn — Know what matters",
  description: "A personal analyst for the AI and developer world.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
