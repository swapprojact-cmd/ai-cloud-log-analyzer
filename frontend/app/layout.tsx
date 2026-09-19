import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Cloud Log Analyzer",
  description: "Upload, analyze and investigate application logs with ML anomaly detection and AI explanations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
