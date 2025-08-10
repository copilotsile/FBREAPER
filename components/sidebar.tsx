"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Activity, Database, Network, Search } from "lucide-react"
import { cn } from "@/lib/utils"

const nav = [
  { href: "/search", icon: Search, label: "Search" },
  { href: "/status", icon: Activity, label: "Scraper Status" },
  { href: "/data", icon: Database, label: "Data Viewer" },
  { href: "/network", icon: Network, label: "Link Analysis" },
]

export default function Sidebar() {
  const pathname = usePathname()
  return (
    <aside className="hidden md:block w-60 shrink-0 border-r bg-card min-h-screen">
      <div className="px-4 py-4 border-b">
        <Link href="/" className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-md bg-emerald-600" aria-hidden />
          <span className="font-semibold tracking-tight">fbreaper</span>
        </Link>
      </div>
      <nav className="p-2 space-y-1">
        {nav.map((item) => {
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-2 px-3 py-2 rounded-md text-sm",
                active
                  ? "bg-emerald-600 text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground",
              )}
            >
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>
      <div className="px-4 py-4 mt-auto text-xs text-muted-foreground">v1.0.0</div>
    </aside>
  )
}
