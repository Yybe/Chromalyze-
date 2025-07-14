import Link from "next/link"
import { ModeToggle } from "@/components/theme/mode-toggle"

export function Header() {
  return (
    <header className="bg-background border-b border-border shadow-sm">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center">
              <span className="font-bold text-2xl bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">Chromalyze</span>
            </Link>
            <nav className="hidden md:flex items-center space-x-6">
              <Link
                href="/analyze"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                Analyze
              </Link>
              <Link
                href="/history"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                History
              </Link>
              <Link
                href="/about"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                About
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            <ModeToggle />
          </div>
        </div>
      </div>
    </header>
  )
}