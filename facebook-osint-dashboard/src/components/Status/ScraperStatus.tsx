import React from 'react';
import { Activity, AlertCircle, CheckCircle, Clock, Play, Pause, XCircle } from 'lucide-react';
import { ScraperStatus as ScraperStatusType, ScraperError } from '../../types';

interface ScraperStatusProps {
  status: ScraperStatusType;
}

const ScraperStatus: React.FC<ScraperStatusProps> = ({ status }) => {
  const getStatusIcon = () => {
    if (status.isActive) {
      return <Play className="h-5 w-5 text-accent-green" />;
    }
    return <Pause className="h-5 w-5 text-gray-400" />;
  };

  const getStatusColor = () => {
    if (status.isActive) return 'text-accent-green';
    return 'text-gray-400';
  };

  const formatDuration = (startTime: string) => {
    const start = new Date(startTime);
    const now = new Date();
    const diff = now.getTime() - start.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m`;
  };

  return (
    <div className="bg-dark-card rounded-lg p-6 border border-dark-border">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-white">Scraper Status</h2>
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <span className={`font-medium ${getStatusColor()}`}>
            {status.isActive ? 'Active' : 'Inactive'}
          </span>
        </div>
      </div>

      {/* Current Target */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Current Target</span>
          <span className="text-sm text-white font-mono">{status.currentTarget}</span>
        </div>
        <div className="w-full bg-dark-surface rounded-full h-2">
          <div
            className="bg-accent-blue h-2 rounded-full transition-all duration-300"
            style={{ width: `${status.progress}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>{status.processedItems} processed</span>
          <span>{status.totalItems} total</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-dark-surface rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Clock className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-400">Runtime</span>
          </div>
          <span className="text-lg font-semibold text-white">
            {formatDuration(status.startTime)}
          </span>
        </div>
        
        <div className="bg-dark-surface rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Activity className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-400">ETA</span>
          </div>
          <span className="text-lg font-semibold text-white">
            {status.estimatedCompletion}
          </span>
        </div>
      </div>

      {/* Errors Section */}
      {status.errors.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-4 w-4 text-accent-red" />
            <span className="text-sm font-medium text-white">Recent Errors</span>
          </div>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {status.errors.slice(0, 5).map((error) => (
              <ErrorItem key={error.id} error={error} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const ErrorItem: React.FC<{ error: ScraperError }> = ({ error }) => {
  const getErrorIcon = (type: string) => {
    switch (type) {
      case 'network':
        return <XCircle className="h-4 w-4 text-accent-red" />;
      case 'rate_limit':
        return <Clock className="h-4 w-4 text-accent-yellow" />;
      case 'auth':
        return <AlertCircle className="h-4 w-4 text-accent-red" />;
      default:
        return <AlertCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <div className="bg-dark-surface rounded-lg p-3 border-l-4 border-accent-red">
      <div className="flex items-start space-x-3">
        {getErrorIcon(error.type)}
        <div className="flex-1">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm font-medium text-white">{error.type}</span>
            <span className="text-xs text-gray-400">{error.timestamp}</span>
          </div>
          <p className="text-sm text-gray-300">{error.message}</p>
          <span className="text-xs text-gray-400">Target: {error.target}</span>
        </div>
      </div>
    </div>
  );
};

export default ScraperStatus;
