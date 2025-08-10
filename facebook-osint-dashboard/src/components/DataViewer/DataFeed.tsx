import React, { useState } from 'react';
import { Heart, MessageCircle, Share, ThumbsUp, Clock, User, ExternalLink } from 'lucide-react';
import { ScrapedPost, Comment } from '../../types';

interface DataFeedProps {
  posts: ScrapedPost[];
  loading?: boolean;
}

const DataFeed: React.FC<DataFeedProps> = ({ posts, loading = false }) => {
  const [expandedPosts, setExpandedPosts] = useState<Set<string>>(new Set());

  const togglePostExpansion = (postId: string) => {
    const newExpanded = new Set(expandedPosts);
    if (newExpanded.has(postId)) {
      newExpanded.delete(postId);
    } else {
      newExpanded.add(postId);
    }
    setExpandedPosts(newExpanded);
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const getTotalReactions = (reactions: ScrapedPost['reactions']) => {
    return Object.values(reactions).reduce((sum, count) => sum + count, 0);
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-dark-card rounded-lg p-6 border border-dark-border animate-pulse">
            <div className="flex items-start space-x-4">
              <div className="w-10 h-10 bg-dark-surface rounded-full"></div>
              <div className="flex-1 space-y-3">
                <div className="h-4 bg-dark-surface rounded w-1/4"></div>
                <div className="h-4 bg-dark-surface rounded w-3/4"></div>
                <div className="h-4 bg-dark-surface rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
      {posts.map((post) => (
        <PostCard
          key={post.id}
          post={post}
          isExpanded={expandedPosts.has(post.id)}
          onToggleExpansion={() => togglePostExpansion(post.id)}
          formatTimestamp={formatTimestamp}
          getTotalReactions={getTotalReactions}
        />
      ))}
    </div>
  );
};

interface PostCardProps {
  post: ScrapedPost;
  isExpanded: boolean;
  onToggleExpansion: () => void;
  formatTimestamp: (timestamp: string) => string;
  getTotalReactions: (reactions: ScrapedPost['reactions']) => number;
}

const PostCard: React.FC<PostCardProps> = ({
  post,
  isExpanded,
  onToggleExpansion,
  formatTimestamp,
  getTotalReactions,
}) => {
  return (
    <div className="bg-dark-card rounded-lg border border-dark-border overflow-hidden">
      {/* Post Header */}
      <div className="p-4 border-b border-dark-border">
        <div className="flex items-start space-x-3">
          <img
            src={post.author.avatar}
            alt={post.author.name}
            className="w-10 h-10 rounded-full object-cover"
            onError={(e) => {
              e.currentTarget.src = 'https://via.placeholder.com/40x40/2d3748/ffffff?text=U';
            }}
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <span className="font-medium text-white">{post.author.name}</span>
              <span className="text-gray-400">@{post.author.username}</span>
              {post.group && (
                <span className="text-xs bg-accent-blue/20 text-accent-blue px-2 py-1 rounded">
                  {post.group}
                </span>
              )}
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <Clock className="h-3 w-3" />
              <span>{formatTimestamp(post.timestamp)}</span>
            </div>
          </div>
          <a
            href={post.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
          >
            <ExternalLink className="h-4 w-4" />
          </a>
        </div>
      </div>

      {/* Post Content */}
      <div className="p-4">
        <p className="text-gray-300 leading-relaxed mb-4">{post.content}</p>

        {/* Reactions and Engagement */}
        <div className="flex items-center justify-between text-sm text-gray-400 mb-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <ThumbsUp className="h-4 w-4 text-accent-blue" />
              <span>{getTotalReactions(post.reactions)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <MessageCircle className="h-4 w-4 text-accent-green" />
              <span>{post.comments.length}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Share className="h-4 w-4 text-accent-yellow" />
              <span>{post.shares}</span>
            </div>
          </div>
        </div>

        {/* Comments Preview */}
        {post.comments.length > 0 && (
          <div className="space-y-3">
            <button
              onClick={onToggleExpansion}
              className="text-sm text-accent-blue hover:text-blue-400 transition-colors"
            >
              {isExpanded ? 'Hide' : `Show ${post.comments.length} comments`}
            </button>

            {isExpanded && (
              <div className="space-y-3 border-t border-dark-border pt-3">
                {post.comments.map((comment) => (
                  <CommentItem key={comment.id} comment={comment} formatTimestamp={formatTimestamp} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

interface CommentItemProps {
  comment: Comment;
  formatTimestamp: (timestamp: string) => string;
}

const CommentItem: React.FC<CommentItemProps> = ({ comment, formatTimestamp }) => {
  return (
    <div className="flex space-x-3">
      <img
        src={comment.author.avatar}
        alt={comment.author.name}
        className="w-8 h-8 rounded-full object-cover flex-shrink-0"
        onError={(e) => {
          e.currentTarget.src = 'https://via.placeholder.com/32x32/2d3748/ffffff?text=U';
        }}
      />
      <div className="flex-1">
        <div className="flex items-center space-x-2 mb-1">
          <span className="text-sm font-medium text-white">{comment.author.name}</span>
          <span className="text-xs text-gray-400">{formatTimestamp(comment.timestamp)}</span>
        </div>
        <p className="text-sm text-gray-300 mb-2">{comment.content}</p>
        {comment.reactions > 0 && (
          <div className="flex items-center space-x-1 text-xs text-gray-400">
            <Heart className="h-3 w-3 text-accent-red" />
            <span>{comment.reactions}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataFeed;
