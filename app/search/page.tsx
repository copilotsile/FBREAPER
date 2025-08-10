"use client"

import { useState } from "react"
import DashboardShell from "@/components/dashboard-shell"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import DataFeed from "@/components/data-feed"
import type { ScrapedPost } from "@/lib/types"
import { Search } from "lucide-react"

const mockPosts: ScrapedPost[] = [
  {
    id: "1",
    content:
      "Just attended the peaceful protest downtown. The energy was incredible! #Protest2024 #PeacefulDemonstration",
    author: {
      name: "John Doe",
      username: "john.doe",
      avatar: "/placeholder.svg?height=40&width=40",
      profileUrl: "https://facebook.com/john.doe",
    },
    timestamp: "2024-01-15T10:30:00Z",
    reactions: { like: 45, love: 12, haha: 3, wow: 2, sad: 1, angry: 0 },
    comments: [
      {
        id: "c1",
        content: "Great photos! Wish I could have been there.",
        author: {
          name: "Jane Smith",
          username: "jane.smith",
          avatar: "/placeholder.svg?height=32&width=32",
        },
        timestamp: "2024-01-15T10:35:00Z",
        reactions: 8,
      },
    ],
    shares: 23,
    url: "https://facebook.com/post/123",
    group: "Protest Group 2024",
  },
]

export default function SearchPage() {
  const [query, setQuery] = useState("")
  const [type, setType] = useState<"keyword" | "user" | "group" | "page">("keyword")
  const [loading, setLoading] = useState(false)
  const [posts, setPosts] = useState<ScrapedPost[]>([])

  const onSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    // TODO: Hook to backend search endpoint if available.
    // For now, simulate delay and return mock data.
    setTimeout(() => {
      setPosts(mockPosts)
      setLoading(false)
    }, 800)
  }

  return (
    <DashboardShell>
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>OSINT Search</CardTitle>
            <CardDescription>Search Facebook for users, groups, pages, or keywords</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Tabs defaultValue="keyword" onValueChange={(v) => setType(v as any)}>
              <TabsList className="grid grid-cols-4">
                <TabsTrigger value="keyword">Keyword</TabsTrigger>
                <TabsTrigger value="user">User</TabsTrigger>
                <TabsTrigger value="group">Group</TabsTrigger>
                <TabsTrigger value="page">Page</TabsTrigger>
              </TabsList>
              <TabsContent value="keyword" />
              <TabsContent value="user" />
              <TabsContent value="group" />
              <TabsContent value="page" />
            </Tabs>

            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={`Search for ${type}s...`}
                  className="pl-9"
                />
              </div>
              <Button onClick={onSearch} className="bg-emerald-600 hover:bg-emerald-700">
                Search
              </Button>
            </div>

            <div className="flex flex-wrap gap-2 text-xs">
              {type === "keyword" &&
                ["#protest", "#election", "#covid", "#climate"].map((k) => (
                  <Badge
                    key={k}
                    variant="secondary"
                    className="cursor-pointer"
                    onClick={() => {
                      setQuery(k)
                      onSearch()
                    }}
                  >
                    {k}
                  </Badge>
                ))}
            </div>
          </CardContent>
        </Card>

        <DataFeed posts={posts} loading={loading} />
      </div>
    </DashboardShell>
  )
}
