"use client"

import DashboardShell from "@/components/dashboard-shell"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import NetworkGraph from "@/components/network-graph"
import type { NetworkNode, NetworkLink } from "@/lib/types"

const mockNodes: NetworkNode[] = [
  { id: "1", label: "John Doe", type: "user", connections: 45, avatar: "/placeholder.svg?height=32&width=32" },
  { id: "2", label: "Protest Group 2024", type: "group", connections: 1200 },
  { id: "3", label: "Jane Smith", type: "user", connections: 23, avatar: "/placeholder.svg?height=32&width=32" },
  { id: "4", label: "News Page", type: "page", connections: 8900 },
  { id: "5", label: "Post #1234", type: "post", connections: 156 },
]

const mockLinks: NetworkLink[] = [
  { source: "1", target: "2", strength: 0.8, type: "comment" },
  { source: "3", target: "2", strength: 0.6, type: "reaction" },
  { source: "4", target: "2", strength: 0.9, type: "share" },
  { source: "1", target: "5", strength: 0.7, type: "comment" },
]

export default function NetworkPage() {
  return (
    <DashboardShell>
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Link Analysis</CardTitle>
            <CardDescription>Visualize connections between users, groups, pages, and posts</CardDescription>
          </CardHeader>
          <CardContent>
            <NetworkGraph nodes={mockNodes} links={mockLinks} />
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  )
}
