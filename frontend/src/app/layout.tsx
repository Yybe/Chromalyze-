import type { Metadata } from 'next'
import './globals.css'
import { Header } from "@/components/layout/header";
import { ThemeProvider } from "@/components/providers/theme-provider";

export const metadata: Metadata = {
  title: 'Chromalyze - Professional Beauty Analysis',
  description: 'AI-powered face shape and color season analysis with personalized beauty recommendations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-gray-50 dark:bg-gray-900 font-sans antialiased" suppressHydrationWarning>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="relative flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">{children}</main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
