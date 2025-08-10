"use client"

import { useState } from "react"
import type { ScrapedPost, Comment as CommentType } from "@/lib/types"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { MessageCircle, Share2, ThumbsUp, Clock, ExternalLink } from "lucide-react"

export default function DataFeed({ posts, loading = false }: { posts: ScrapedPost[]; loading?: boolean }) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({})

  const toggle = (id: string) => setExpanded((s) => ({ ...s, [id]: !s[id] }))

  const totalReactions = (reactions: ScrapedPost["reactions"]) =>
    Object.values(reactions ?? {}).reduce((acc, n) => acc + n, 0)

  const formatTime = (ts: string) => {
    const d = new Date(ts)
    if (Number.isNaN(d.getTime())) return "unknown"
    const diff = Date.now() - d.getTime()
    const m = Math.floor(diff / 60000)
    const h = Math.floor(m / 60)
    const days = Math.floor(h / 24)
    if (m < 60) return `${m}m ago`
    if (h < 24) return `${h}h ago`
    return `${days}d ago`
  }

  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <Card key={i} className="p-6 animate-pulse">
            <div className="h-4 w-1/3 bg-muted rounded mb-3" />
            <div className="h-4 w-2/3 bg-muted rounded mb-3" />
            <div className="h-4 w-1/2 bg-muted rounded" />
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {posts.map((post) => (
        <Card key={post.id} className="p-4">
          <div className="flex items-start gap-3">
            <img
              src={post.author.avatar || "/placeholder.svg"}
              alt={`${post.author.name} avatar`}
              className="h-10 w-10 rounded-full object-cover"
              onError={(e) => {
                ;(e.currentTarget as HTMLImageElement).src = "/placeholder.svg?height=40&width=40"
              }}
            />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium">{post.author.name}</span>
                <span className="text-xs text-muted-foreground">@{post.author.username}</span>
                {post.group && <Badge variant="outline">{post.group}</Badge>}
                {post.page && <Badge variant="secondary">{post.page}</Badge>}
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock className="h-3 w-3" />
                <span>{formatTime(post.timestamp)}</span>
                <a
                  href={post.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 hover:underline"
                >
                  <ExternalLink className="h-3 w-3" />
                  Open
                </a>
              </div>
              <p className="mt-3 text-sm">{post.content}</p>

              <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                <span className="inline-flex items-center gap-1">
                  <ThumbsUp className="h-4 w-4 text-emerald-600" />
                  {totalReactions(post.reactions)}
                </span>
                <span className="inline-flex items-center gap-1">
                  <MessageCircle className="h-4 w-4 text-emerald-600" />
                  {post.comments?.length ?? 0}
                </span>
                <span className="inline-flex items-center gap-1">
                  <Share2 className="h-4 w-4 text-emerald-600" />
                  {post.shares ?? 0}
                </span>
              </div>

              {post.comments?.length ? (
                <div className="mt-3">
                  <button className="text-emerald-700 hover:underline text-sm" onClick={() => toggle(post.id)}>
                    {expanded[post.id] ? "Hide comments" : `Show ${post.comments.length} comments`}
                  </button>

                  {expanded[post.id] && (
                    <div className="mt-3 space-y-3 border-t pt-3">
                      {post.comments.map((c) => (
                        <Comment key={c.id} comment={c} />
                      ))}
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}

function Comment({ comment }: { comment: CommentType }) {
  const formatTime = (ts: string) => {
    const d = new Date(ts)
    if (Number.isNaN(d.getTime())) return "unknown"
    const diff = Date.now() - d.getTime()
    const m = Math.floor(diff / 60000)
    const h = Math.floor(m / 60)
    const days = Math.floor(h / 24)
    if (m < 60) return `${m}m ago`
    if (h < 24) return `${h}h ago`
    return `${days}d ago`
  }

  return (
    <div className="flex gap-3">
      <img
        src={comment.author.avatar || "/placeholder.svg"}
        alt={`${comment.author.name} avatar`}
        className="h-8 w-8 rounded-full object-cover"
        onError={(e) => {
          ;(e.currentTarget as HTMLImageElement).src = "/placeholder.svg?height=32&width=32"
        }}
      />
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-medium">{comment.author.name}</span>
          <span className="text-xs text-muted-foreground">{formatTime(comment.timestamp)}</span>
        </div>
        <p className="text-sm mt-1">{comment.content}</p>
      </div>
    </div>
  )
}
