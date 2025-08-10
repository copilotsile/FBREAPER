import React, { useState, useEffect } from 'react';
import SearchBar from '../components/Search/SearchBar';
import ScraperStatus from '../components/Status/ScraperStatus';
import DataFeed from '../components/DataViewer/DataFeed';
import NetworkGraph from '../components/Network/NetworkGraph';
import { ScrapedPost, ScraperStatus as ScraperStatusType, NetworkNode, NetworkLink, DashboardStats } from '../types';

const Dashboard: React.FC = () => {
  const [currentView, setCurrentView] = useState<'search' | 'status' | 'data' | 'network'>('search');
  const [posts, setPosts] = useState<ScrapedPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<DashboardStats>({
    totalPosts: 0,
    totalComments: 0,
    totalReactions: 0,
    activeScrapers: 0,
    errorsToday: 0,
    dataCollectedToday: 0,
  });

  // Mock data for demonstration
  const mockScraperStatus: ScraperStatusType = {
    isActive: true,
    currentTarget: 'protest.group.2024',
    progress: 67,
    totalItems: 1500,
    processedItems: 1005,
    errors: [
      {
        id: '1',
        message: 'Rate limit exceeded for target group',
        timestamp: '2024-01-15T10:30:00Z',
        target: 'protest.group.2024',
        type: 'rate_limit',
      },
      {
        id: '2',
        message: 'Network timeout while fetching comments',
        timestamp: '2024-01-15T10:25:00Z',
        target: 'protest.group.2024',
        type: 'network',
      },
    ],
    startTime: '2024-01-15T08:00:00Z',
    estimatedCompletion: '2h 15m',
  };

  const mockNetworkNodes: NetworkNode[] = [
    { id: '1', label: 'John Doe', type: 'user', connections: 45, avatar: 'https://via.placeholder.com/32x32/3b82f6/ffffff?text=J' },
    { id: '2', label: 'Protest Group 2024', type: 'group', connections: 1200 },
    { id: '3', label: 'Jane Smith', type: 'user', connections: 23, avatar: 'https://via.placeholder.com/32x32/10b981/ffffff?text=J' },
    { id: '4', label: 'News Page', type: 'page', connections: 8900 },
    { id: '5', label: 'Post #1234', type: 'post', connections: 156 },
  ];

  const mockNetworkLinks: NetworkLink[] = [
    { source: '1', target: '2', strength: 0.8, type: 'comment' },
    { source: '3', target: '2', strength: 0.6, type: 'reaction' },
    { source: '4', target: '2', strength: 0.9, type: 'share' },
    { source: '1', target: '5', strength: 0.7, type: 'comment' },
  ];

  const mockPosts: ScrapedPost[] = [
    {
      id: '1',
      content: 'Just attended the peaceful protest downtown. The energy was incredible! #Protest2024 #PeacefulDemonstration',
      author: {
        name: 'John Doe',
        username: 'john.doe',
        avatar: 'https://via.placeholder.com/40x40/3b82f6/ffffff?text=J',
        profileUrl: 'https://facebook.com/john.doe',
      },
      timestamp: '2024-01-15T10:30:00Z',
      reactions: { like: 45, love: 12, haha: 3, wow: 2, sad: 1, angry: 0 },
      comments: [
        {
          id: 'c1',
          content: 'Great photos! Wish I could have been there.',
          author: { name: 'Jane Smith', username: 'jane.smith', avatar: 'https://via.placeholder.com/32x32/10b981/ffffff?text=J' },
          timestamp: '2024-01-15T10:35:00Z',
          reactions: 8,
        },
        {
          id: 'c2',
          content: 'Stay safe out there! The movement is growing stronger.',
          author: { name: 'Mike Johnson', username: 'mike.j', avatar: 'https://via.placeholder.com/32x32/f59e0b/ffffff?text=M' },
          timestamp: '2024-01-15T10:40:00Z',
          reactions: 15,
        },
      ],
      shares: 23,
      url: 'https://facebook.com/post/123',
      group: 'Protest Group 2024',
    },
    {
      id: '2',
      content: 'Breaking: Major developments in the ongoing situation. More details to follow. #BreakingNews #Update',
      author: {
        name: 'News Page',
        username: 'news.page',
        avatar: 'https://via.placeholder.com/40x40/ef4444/ffffff?text=N',
        profileUrl: 'https://facebook.com/news.page',
      },
      timestamp: '2024-01-15T09:15:00Z',
      reactions: { like: 234, love: 89, haha: 12, wow: 45, sad: 23, angry: 67 },
      comments: [
        {
          id: 'c3',
          content: 'This is getting out of hand. We need leadership now.',
          author: { name: 'Sarah Wilson', username: 'sarah.w', avatar: 'https://via.placeholder.com/32x32/8b5cf6/ffffff?text=S' },
          timestamp: '2024-01-15T09:20:00Z',
          reactions: 34,
        },
      ],
      shares: 156,
      url: 'https://facebook.com/post/456',
      page: 'News Page',
    },
  ];

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        totalPosts: prev.totalPosts + Math.floor(Math.random() * 3),
        totalComments: prev.totalComments + Math.floor(Math.random() * 10),
        totalReactions: prev.totalReactions + Math.floor(Math.random() * 50),
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (query: string, type: string) => {
    setLoading(true);
    setCurrentView('data');
    
    // Simulate API call
    setTimeout(() => {
      setPosts(mockPosts);
      setLoading(false);
    }, 1500);
  };

  const renderContent = () => {
    switch (currentView) {
      case 'search':
        return (
          <div className="p-6">
            <SearchBar onSearch={handleSearch} />
          </div>
        );
      case 'status':
        return (
          <div className="p-6">
            <ScraperStatus status={mockScraperStatus} />
          </div>
        );
      case 'data':
        return (
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-white mb-2">Scraped Data</h2>
              <p className="text-gray-400">Showing results from recent searches</p>
            </div>
            <DataFeed posts={posts} loading={loading} />
          </div>
        );
      case 'network':
        return (
          <div className="p-6">
            <NetworkGraph nodes={mockNetworkNodes} links={mockNetworkLinks} />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Stats Bar */}
      <div className="bg-dark-surface border-b border-dark-border px-6 py-3">
        <div className="grid grid-cols-6 gap-4 text-center">
          <div>
            <p className="text-lg font-bold text-white">{stats.totalPosts}</p>
            <p className="text-xs text-gray-400">Total Posts</p>
          </div>
          <div>
            <p className="text-lg font-bold text-white">{stats.totalComments}</p>
            <p className="text-xs text-gray-400">Comments</p>
          </div>
          <div>
            <p className="text-lg font-bold text-white">{stats.totalReactions}</p>
            <p className="text-xs text-gray-400">Reactions</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-green">{stats.activeScrapers}</p>
            <p className="text-xs text-gray-400">Active Scrapers</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-red">{stats.errorsToday}</p>
            <p className="text-xs text-gray-400">Errors Today</p>
          </div>
          <div>
            <p className="text-lg font-bold text-accent-blue">{stats.dataCollectedToday}</p>
            <p className="text-xs text-gray-400">Data Collected</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {renderContent()}
      </div>
    </div>
  );
};

export default Dashboard;
