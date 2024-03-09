import { Navbar } from "@/components/Navbar";
import { createClient } from "@/utils/supabase/server";
import { GeistSans } from "geist/font/sans";
import { redirect } from "next/navigation";
import AuthButton from "../components/AuthButton";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const defaultUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : "http://localhost:3000";

export const metadata = {
  metadataBase: new URL(defaultUrl),
  title: "TensionNews",
  description: "The Business & Finance News Hub",
};

const RootLayout = async ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="en" className={GeistSans.className}>
      <body className="dark grid min-h-screen bg-background text-foreground">
        {children}
        <Toaster />
      </body>
    </html>
  );
};

export default RootLayout;
