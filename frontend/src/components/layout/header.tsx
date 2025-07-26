import Link from "next/link"
import { ModeToggle } from "@/components/theme/mode-toggle"

export function Header() {
  return (
    <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center">
              <span className="font-bold text-2xl text-blue-600 dark:text-blue-400">Chromalyze</span>
            </Link>
            <nav className="hidden md:flex items-center space-x-6">
              <Link
                href="/analyze"
                className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                Analyze
              </Link>
              <Link
                href="/history"
                className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                History
              </Link>
              <Link
                href="/about"
                className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium"
              >
                About
              </Link>
            </nav>
          </div>
          <div className="flex items-center no-overlap">
            <ModeToggle />
          </div>
        </div>
      </div>
    </header>
  )
}