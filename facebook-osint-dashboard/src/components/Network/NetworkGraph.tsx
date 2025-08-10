import React, { useState, useMemo } from 'react';
import { Network, ZoomIn, ZoomOut, RotateCcw, Filter } from 'lucide-react';
import { NetworkNode, NetworkLink } from '../../types';

interface NetworkGraphProps {
  nodes: NetworkNode[];
  links: NetworkLink[];
  loading?: boolean;
}

const NetworkGraph: React.FC<NetworkGraphProps> = ({ nodes, links, loading = false }) => {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [filter, setFilter] = useState<string>('all');

  const filteredNodes = useMemo(() => {
    if (filter === 'all') return nodes;
    return nodes.filter(node => node.type === filter);
  }, [nodes, filter]);

  const filteredLinks = useMemo(() => {
    if (filter === 'all') return links;
    return links.filter(link => {
      const sourceNode = nodes.find(n => n.id === link.source);
      const targetNode = nodes.find(n => n.id === link.target);
      return sourceNode?.type === filter || targetNode?.type === filter;
    });
  }, [links, nodes, filter]);

  const nodeTypes = [
    { id: 'all', label: 'All', color: 'text-gray-400' },
    { id: 'user', label: 'Users', color: 'text-accent-blue' },
    { id: 'group', label: 'Groups', color: 'text-accent-green' },
    { id: 'page', label: 'Pages', color: 'text-accent-yellow' },
    { id: 'post', label: 'Posts', color: 'text-accent-red' },
  ];

  const selectedNodeData = selectedNode ? nodes.find(n => n.id === selectedNode) : null;

  if (loading) {
    return (
      <div className="bg-dark-card rounded-lg p-6 border border-dark-border">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-accent-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-400">Loading network data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-dark-card rounded-lg border border-dark-border">
      {/* Header */}
      <div className="p-4 border-b border-dark-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Network className="h-5 w-5 text-accent-blue" />
            <h2 className="text-lg font-semibold text-white">Link Analysis</h2>
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Zoom Controls */}
            <button
              onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
              className="p-2 bg-dark-surface rounded-lg hover:bg-dark-border transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="h-4 w-4 text-gray-400" />
            </button>
            <span className="text-sm text-gray-400 min-w-[60px] text-center">
              {Math.round(zoom * 100)}%
            </span>
            <button
              onClick={() => setZoom(Math.min(2, zoom + 0.1))}
              className="p-2 bg-dark-surface rounded-lg hover:bg-dark-border transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="h-4 w-4 text-gray-400" />
            </button>
            <button
              onClick={() => setZoom(1)}
              className="p-2 bg-dark-surface rounded-lg hover:bg-dark-border transition-colors"
              title="Reset Zoom"
            >
              <RotateCcw className="h-4 w-4 text-gray-400" />
            </button>
          </div>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="p-4 border-b border-dark-border">
        <div className="flex items-center space-x-2">
          <Filter className="h-4 w-4 text-gray-400" />
          <span className="text-sm text-gray-400">Filter by type:</span>
          <div className="flex space-x-1">
            {nodeTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setFilter(type.id)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                  filter === type.id
                    ? 'bg-accent-blue text-white'
                    : 'bg-dark-surface text-gray-400 hover:bg-dark-border'
                }`}
              >
                {type.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Network Visualization */}
      <div className="p-4">
        <div className="relative h-96 bg-dark-surface rounded-lg border border-dark-border overflow-hidden">
          {/* Placeholder for actual network visualization */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <Network className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400 mb-2">Network Visualization</p>
              <p className="text-sm text-gray-500">
                {filteredNodes.length} nodes, {filteredLinks.length} connections
              </p>
            </div>
          </div>

          {/* Mock network nodes for demonstration */}
          <div className="absolute inset-0">
            {filteredNodes.slice(0, 10).map((node, index) => (
              <div
                key={node.id}
                className={`absolute w-4 h-4 rounded-full cursor-pointer transition-all ${
                  selectedNode === node.id
                    ? 'bg-accent-blue ring-2 ring-accent-blue/50'
                    : getNodeColor(node.type)
                }`}
                style={{
                  left: `${20 + (index % 5) * 15}%`,
                  top: `${20 + Math.floor(index / 5) * 20}%`,
                  transform: `scale(${zoom})`,
                }}
                onClick={() => setSelectedNode(selectedNode === node.id ? null : node.id)}
                title={`${node.label} (${node.connections} connections)`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Node Details Panel */}
      {selectedNodeData && (
        <div className="p-4 border-t border-dark-border">
          <h3 className="text-sm font-medium text-white mb-3">Node Details</h3>
          <div className="bg-dark-surface rounded-lg p-4 space-y-3">
            <div className="flex items-center space-x-3">
              {selectedNodeData.avatar && (
                <img
                  src={selectedNodeData.avatar}
                  alt={selectedNodeData.label}
                  className="w-8 h-8 rounded-full object-cover"
                />
              )}
              <div>
                <p className="font-medium text-white">{selectedNodeData.label}</p>
                <p className="text-sm text-gray-400 capitalize">{selectedNodeData.type}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Connections:</span>
                <span className="text-white ml-2">{selectedNodeData.connections}</span>
              </div>
              <div>
                <span className="text-gray-400">ID:</span>
                <span className="text-white ml-2 font-mono text-xs">{selectedNodeData.id}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Statistics */}
      <div className="p-4 border-t border-dark-border">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-white">{filteredNodes.length}</p>
            <p className="text-xs text-gray-400">Nodes</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-white">{filteredLinks.length}</p>
            <p className="text-xs text-gray-400">Connections</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-white">
              {filteredNodes.length > 0 ? Math.round((filteredLinks.length / filteredNodes.length) * 100) / 100 : 0}
            </p>
            <p className="text-xs text-gray-400">Avg. Connections</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const getNodeColor = (type: string): string => {
  switch (type) {
    case 'user':
      return 'bg-accent-blue';
    case 'group':
      return 'bg-accent-green';
    case 'page':
      return 'bg-accent-yellow';
    case 'post':
      return 'bg-accent-red';
    default:
      return 'bg-gray-500';
  }
};

export default NetworkGraph;
