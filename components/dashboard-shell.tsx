"use client"

import type { ReactNode } from "react"
import Sidebar from "@/components/sidebar"
import SiteHeader from "@/components/site-header"

export default function DashboardShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        <Sidebar />
        <div className="flex-1 min-w-0">
          <SiteHeader />
          <main className="px-4 md:px-6 py-6">{children}</main>
        </div>
      </div>
    </div>
  )
}
