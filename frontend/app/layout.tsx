import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Cloud Log Analyzer",
  description: "Cloud log monitoring, anomaly detection, and AI-assisted incident analysis.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
