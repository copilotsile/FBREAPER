"use client"

import { useEffect, useState } from "react"
import DashboardShell from "@/components/dashboard-shell"
import DataFeed from "@/components/data-feed"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { getPosts } from "@/lib/api"
import type { ScrapedPost } from "@/lib/types"

export default function DataPage() {
  const [posts, setPosts] = useState<ScrapedPost[]>([])
  const [loading, setLoading] = useState(false)

  const fetchPosts = async () => {
    setLoading(true)
    try {
      const data = await getPosts()
      // Map backend DTOs to ScrapedPost-ish structure if necessary:
      const normalized: ScrapedPost[] = (Array.isArray(data) ? data : []).map((p: any, idx: number) => ({
        id: p.id ?? String(idx + 1),
        content: p.content ?? "(no content)",
        author: {
          name: p.author ?? "unknown",
          username: (p.author ?? "unknown").toLowerCase().replaceAll(" ", "."),
          avatar: "/placeholder.svg?height=40&width=40",
          profileUrl: "#",
        },
        timestamp: p.timestamp ?? new Date().toISOString(),
        reactions: { like: 0, love: 0, haha: 0, wow: 0, sad: 0, angry: 0 },
        comments: [],
        shares: 0,
        url: "#",
      }))
      setPosts(normalized)
    } catch (e) {
      // fallback: no posts
      setPosts([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPosts()
  }, [])

  return (
    <DashboardShell>
      <div className="space-y-6">
        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardTitle>Scraped Data</CardTitle>
              <CardDescription>Posts collected by the scraper</CardDescription>
            </div>
            <div>
              <Button variant="outline" onClick={fetchPosts}>
                Refresh
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <DataFeed posts={posts} loading={loading} />
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  )
}
