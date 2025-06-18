import Link from "next/link"
import { ModeToggle } from "@/components/theme/mode-toggle"

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold text-xl bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent">Chromalyze</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link
              href="/analyze"
              className="transition-colors hover:text-foreground/80 text-foreground hover:text-pink-500"
            >
              Analyze
            </Link>
            <Link
              href="/about"
              className="transition-colors hover:text-foreground/80 text-foreground hover:text-pink-500"
            >
              About
            </Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* Add search or other controls here */}
          </div>
          <nav className="flex items-center">
            <ModeToggle />
          </nav>
        </div>
      </div>
    </header>
  )
} 