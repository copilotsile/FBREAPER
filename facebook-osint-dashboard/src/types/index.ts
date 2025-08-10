export interface ScrapedPost {
  id: string;
  content: string;
  author: {
    name: string;
    username: string;
    avatar: string;
    profileUrl: string;
  };
  timestamp: string;
  reactions: {
    like: number;
    love: number;
    haha: number;
    wow: number;
    sad: number;
    angry: number;
  };
  comments: Comment[];
  shares: number;
  url: string;
  group?: string;
  page?: string;
}

export interface Comment {
  id: string;
  content: string;
  author: {
    name: string;
    username: string;
    avatar: string;
  };
  timestamp: string;
  reactions: number;
  replies?: Comment[];
}

export interface ScraperStatus {
  isActive: boolean;
  currentTarget: string;
  progress: number;
  totalItems: number;
  processedItems: number;
  errors: ScraperError[];
  startTime: string;
  estimatedCompletion: string;
}

export interface ScraperError {
  id: string;
  message: string;
  timestamp: string;
  target: string;
  type: 'network' | 'parsing' | 'rate_limit' | 'auth' | 'unknown';
}

export interface NetworkNode {
  id: string;
  label: string;
  type: 'user' | 'group' | 'page' | 'post';
  connections: number;
  avatar?: string;
}

export interface NetworkLink {
  source: string;
  target: string;
  strength: number;
  type: 'comment' | 'reaction' | 'share' | 'mention';
}

export interface SearchResult {
  type: 'user' | 'group' | 'page' | 'keyword';
  query: string;
  results: ScrapedPost[];
  totalCount: number;
  timestamp: string;
}

export interface DashboardStats {
  totalPosts: number;
  totalComments: number;
  totalReactions: number;
  activeScrapers: number;
  errorsToday: number;
  dataCollectedToday: number;
}
