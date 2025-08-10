"use client"

import type { ScraperError, ScraperStatus } from "@/lib/types"
import { Progress } from "@/components/ui/progress"
import { Card } from "@/components/ui/card"
import { AlertCircle, Clock, Pause, Play } from "lucide-react"

export default function ScraperStatusPanel({ status }: { status: ScraperStatus }) {
  const runtime = formatDuration(status.startTime)
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">Current target</div>
        <div className="text-sm font-mono">{status.currentTarget}</div>
      </div>
      <Progress value={status.progress} />

      <div className="grid grid-cols-2 gap-4">
        <Card className="p-4">
          <div className="text-sm text-muted-foreground flex items-center gap-2">
            <Clock className="h-4 w-4" />
            Runtime
          </div>
          <div className="mt-1 font-medium">{runtime}</div>
        </Card>
        <Card className="p-4">
          <div className="text-sm text-muted-foreground">ETA</div>
          <div className="mt-1 font-medium">{status.estimatedCompletion}</div>
        </Card>
      </div>

      <div className="flex items-center gap-2">
        {status.isActive ? (
          <>
            <Play className="h-4 w-4 text-emerald-600" />
            <span className="text-sm font-medium text-emerald-700">Active</span>
          </>
        ) : (
          <>
            <Pause className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Inactive</span>
          </>
        )}
        <div className="ml-auto text-xs text-muted-foreground">
          {status.processedItems} / {status.totalItems} processed
        </div>
      </div>

      {status.errors?.length ? (
        <div className="space-y-2">
          <div className="text-sm font-medium">Recent errors</div>
          <div className="space-y-2 max-h-44 overflow-auto pr-1">
            {status.errors.slice(0, 5).map((e) => (
              <ErrorItem key={e.id} error={e} />
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}

function ErrorItem({ error }: { error: ScraperError }) {
  return (
    <Card className="p-3 border-l-4 border-red-500">
      <div className="flex items-start gap-2">
        <AlertCircle className="h-4 w-4 text-red-600 mt-0.5" />
        <div className="min-w-0">
          <div className="flex items-center justify-between gap-2">
            <div className="text-sm font-medium capitalize">{error.type.replace("_", " ")}</div>
            <div className="text-xs text-muted-foreground">{error.timestamp}</div>
          </div>
          <div className="text-sm">{error.message}</div>
          <div className="text-xs text-muted-foreground">Target: {error.target}</div>
        </div>
      </div>
    </Card>
  )
}

function formatDuration(startTime: string) {
  const start = new Date(startTime).getTime()
  if (!start) return "—"
  const diff = Date.now() - start
  const hours = Math.floor(diff / 3600000)
  const minutes = Math.floor((diff % 3600000) / 60000)
  return `${hours}h ${minutes}m`
}
