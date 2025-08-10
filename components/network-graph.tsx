"use client"

import { useMemo, useState } from "react"
import type { NetworkLink, NetworkNode } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { RotateCcw, ZoomIn, ZoomOut, Filter } from "lucide-react"
import { Card } from "@/components/ui/card"

export default function NetworkGraph({
  nodes,
  links,
  loading = false,
}: {
  nodes: NetworkNode[]
  links: NetworkLink[]
  loading?: boolean
}) {
  const [zoom, setZoom] = useState(1)
  const [filter, setFilter] = useState<"all" | NetworkNode["type"]>("all")
  const [selected, setSelected] = useState<string | null>(null)

  const types = useMemo(
    () => [
      { id: "all", label: "All" },
      { id: "user", label: "Users" },
      { id: "group", label: "Groups" },
      { id: "page", label: "Pages" },
      { id: "post", label: "Posts" },
    ],
    [],
  )

  const filteredNodes = useMemo(() => {
    if (filter === "all") return nodes
    return nodes.filter((n) => n.type === filter)
  }, [nodes, filter])

  const filteredLinks = useMemo(() => {
    if (filter === "all") return links
    const set = new Set(filteredNodes.map((n) => n.id))
    return links.filter((l) => set.has(l.source) || set.has(l.target))
  }, [links, filter, filteredNodes])

  if (loading) {
    return (
      <Card className="p-10">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-center mt-4 text-muted-foreground">Loading network...</p>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <Filter className="h-4 w-4 text-muted-foreground" />
        {types.map((t) => (
          <Button
            key={t.id}
            size="sm"
            variant={filter === (t.id as any) ? "default" : "outline"}
            className={filter === (t.id as any) ? "bg-emerald-600 hover:bg-emerald-700" : ""}
            onClick={() => setFilter(t.id as any)}
          >
            {t.label}
          </Button>
        ))}
        <div className="ml-auto flex items-center gap-2">
          <Button
            size="icon"
            variant="outline"
            onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
            aria-label="Zoom out"
          >
            <ZoomOut className="h-4 w-4" />
          </Button>
          <span className="text-xs w-12 text-center text-muted-foreground">{Math.round(zoom * 100)}%</span>
          <Button size="icon" variant="outline" onClick={() => setZoom(Math.min(2, zoom + 0.1))} aria-label="Zoom in">
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button size="icon" variant="outline" onClick={() => setZoom(1)} aria-label="Reset zoom">
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="relative h-96 rounded-md border overflow-hidden bg-muted/30">
        {/* Simple mock positioning */}
        <div className="absolute inset-0">
          {filteredNodes.slice(0, 12).map((node, i) => {
            const left = 10 + (i % 6) * 15
            const top = 15 + Math.floor(i / 6) * 30
            const active = selected === node.id
            return (
              <button
                key={node.id}
                style={{ left: `${left}%`, top: `${top}%`, transform: `scale(${zoom})` }}
                className={`absolute h-4 w-4 rounded-full ring-2 transition-all ${
                  active ? "bg-emerald-600 ring-emerald-300" : getColor(node.type)
                }`}
                onClick={() => setSelected((s) => (s === node.id ? null : node.id))}
                title={`${node.label} (${node.connections} connections)`}
                aria-label={`Node ${node.label}`}
              />
            )
          })}
        </div>

        {/* Center overlay text */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center text-sm text-muted-foreground">
            {filteredNodes.length} nodes • {filteredLinks.length} links
          </div>
        </div>
      </div>

      {selected && (
        <Card className="p-4">
          {(() => {
            const n = nodes.find((x) => x.id === selected)
            if (!n) return null
            return (
              <div className="flex items-center gap-3">
                {n.avatar ? (
                  <img
                    src={n.avatar || "/placeholder.svg"}
                    alt={`${n.label} avatar`}
                    className="h-8 w-8 rounded-full"
                    onError={(e) => {
                      ;(e.currentTarget as HTMLImageElement).src = "/placeholder.svg?height=32&width=32"
                    }}
                  />
                ) : (
                  <div className="h-8 w-8 rounded-full bg-emerald-600" aria-hidden />
                )}
                <div>
                  <div className="font-medium">{n.label}</div>
                  <div className="text-xs text-muted-foreground capitalize">
                    {n.type} • {n.connections} connections
                  </div>
                </div>
              </div>
            )
          })()}
        </Card>
      )}
    </div>
  )
}

function getColor(type: NetworkNode["type"]) {
  switch (type) {
    case "user":
      return "bg-emerald-600 ring-emerald-300"
    case "group":
      return "bg-teal-600 ring-teal-300"
    case "page":
      return "bg-lime-600 ring-lime-300"
    case "post":
      return "bg-amber-600 ring-amber-300"
    default:
      return "bg-gray-500 ring-gray-300"
  }
}
