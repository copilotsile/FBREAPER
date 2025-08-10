const BASE_URL =
  (typeof window !== "undefined" && (window as any).NEXT_PUBLIC_API_URL) ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8080"

export async function getHealth(): Promise<any> {
  const res = await fetch(`${BASE_URL}/api/health`, { cache: "no-store" })
  if (!res.ok) throw new Error("Health check failed")
  return res.json()
}

export async function getPosts(): Promise<any[]> {
  const res = await fetch(`${BASE_URL}/api/data/posts`, { cache: "no-store" })
  if (!res.ok) throw new Error("Failed to fetch posts")
  return res.json()
}
