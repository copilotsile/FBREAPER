import React from 'react';
import { Search, Activity, Database, Network, Settings, BarChart3, ChevronLeft, ChevronRight } from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggle }) => {
  const navigationItems = [
    { icon: Search, label: 'Search', href: '/search', active: true },
    { icon: Activity, label: 'Scraper Status', href: '/status' },
    { icon: Database, label: 'Data Viewer', href: '/data' },
    { icon: Network, label: 'Link Analysis', href: '/network' },
    { icon: BarChart3, label: 'Analytics', href: '/analytics' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ];

  return (
    <div className={`bg-dark-surface border-r border-dark-border transition-all duration-300 ${
      collapsed ? 'w-16' : 'w-64'
    }`}>
      <div className="flex flex-col h-full">
        {/* Toggle Button */}
        <div className="p-4 border-b border-dark-border">
          <button
            onClick={onToggle}
            className="w-full flex items-center justify-center p-2 rounded-lg bg-dark-card hover:bg-dark-border transition-colors"
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 p-4 space-y-2">
          {navigationItems.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                item.active
                  ? 'bg-accent-blue text-white'
                  : 'text-gray-300 hover:bg-dark-card hover:text-white'
              }`}
            >
              <item.icon size={20} />
              {!collapsed && <span className="font-medium">{item.label}</span>}
            </a>
          ))}
        </nav>

        {/* Footer */}
        {!collapsed && (
          <div className="p-4 border-t border-dark-border">
            <div className="text-xs text-gray-500 text-center">
              v1.0.0
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
