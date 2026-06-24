import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Projector",
  description: "Projecting truth, one frame at a time.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
