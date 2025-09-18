import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { ThemeProvider } from "next-themes";

export const metadata: Metadata = {
  title: "HiAnime - Watch Anime Online",
  description: "Stream thousands of anime episodes in HD quality. Your ultimate destination for watching anime online free.",
  keywords: ["anime", "streaming", "watch anime", "anime online", "HD anime", "subbed anime", "dubbed anime"],
  authors: [{ name: "HiAnime Team" }],
  openGraph: {
    title: "HiAnime - Watch Anime Online",
    description: "Stream thousands of anime episodes in HD quality. Your ultimate destination for watching anime online free.",
    url: "https://hianime.com",
    siteName: "HiAnime",
    type: "website",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "HiAnime - Watch Anime Online",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "HiAnime - Watch Anime Online",
    description: "Stream thousands of anime episodes in HD quality. Your ultimate destination for watching anime online free.",
    images: ["/og-image.jpg"],
  },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className="antialiased bg-background text-foreground"
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false}
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
