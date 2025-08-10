"use client"

import { useMemo } from "react"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Github } from "lucide-react"
import { cn } from "@/lib/utils"

export default function SiteHeader() {
  const time = useMemo(() => new Date().toLocaleTimeString(), [])
  return (
    <header className={cn("sticky top-0 z-30 bg-card/60 backdrop-blur border-b")}>
      <div className="flex items-center justify-between px-4 md:px-6 py-3">
        <div className="flex items-center gap-3">
          <div className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse" aria-hidden />
          <div className="text-sm text-muted-foreground">Last updated: {time}</div>
        </div>
        <div className="flex items-center gap-2">
          <Button asChild variant="outline" size="sm">
            <Link href="/status">Status</Link>
          </Button>
          <Button asChild size="sm" className="bg-emerald-600 hover:bg-emerald-700">
            <Link href="/search">Search</Link>
          </Button>
          <Button variant="ghost" size="icon" aria-label="GitHub">
            <Github className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  )
}
