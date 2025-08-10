"use client"

import DashboardShell from "@/components/dashboard-shell"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import ScraperStatusPanel from "@/components/scraper-status"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import { getHealth } from "@/lib/api"
import type { ScraperStatus } from "@/lib/types"

const mockStatus: ScraperStatus = {
  isActive: true,
  currentTarget: "protest.group.2024",
  progress: 67,
  totalItems: 1500,
  processedItems: 1005,
  errors: [
    {
      id: "1",
      message: "Rate limit exceeded for target group",
      timestamp: "2024-01-15T10:30:00Z",
      target: "protest.group.2024",
      type: "rate_limit",
    },
  ],
  startTime: "2024-01-15T08:00:00Z",
  estimatedCompletion: "2h 15m",
}

export default function StatusPage() {
  const [status, setStatus] = useState<ScraperStatus>(mockStatus)
  const [backendUp, setBackendUp] = useState<boolean | null>(null)

  useEffect(() => {
    const check = async () => {
      try {
        const res = await getHealth()
        setBackendUp(res?.status === "UP")
      } catch {
        setBackendUp(false)
      }
    }
    check()
  }, [])

  return (
    <DashboardShell>
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Scraper Status</CardTitle>
              <CardDescription>Live operational metrics and recent errors</CardDescription>
            </CardHeader>
            <CardContent>
              <ScraperStatusPanel status={status} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Backend</CardTitle>
              <CardDescription>FBReaper Java backend health</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-sm">
                Status:{" "}
                {backendUp === null ? (
                  <span className="text-muted-foreground">Checking...</span>
                ) : backendUp ? (
                  <span className="text-emerald-600 font-medium">UP</span>
                ) : (
                  <span className="text-red-600 font-medium">DOWN</span>
                )}
              </div>
              <Button
                variant="outline"
                onClick={async () => {
                  try {
                    const res = await getHealth()
                    setBackendUp(res?.status === "UP")
                  } catch {
                    setBackendUp(false)
                  }
                }}
              >
                Re-check
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardShell>
  )
}
