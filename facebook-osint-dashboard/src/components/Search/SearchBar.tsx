import React, { useState } from 'react';
import { Search, User, Users, Building, Hash, Send } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string, type: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('keyword');

  const searchTypes = [
    { id: 'keyword', label: 'Keyword', icon: Hash },
    { id: 'user', label: 'User', icon: User },
    { id: 'group', label: 'Group', icon: Users },
    { id: 'page', label: 'Page', icon: Building },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), searchType);
    }
  };

  return (
    <div className="bg-dark-card rounded-lg p-6 border border-dark-border">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-white mb-2">OSINT Search</h2>
        <p className="text-gray-400 text-sm">
          Search for users, groups, pages, or keywords across Facebook
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Search Type Selector */}
        <div className="flex space-x-2">
          {searchTypes.map((type) => (
            <button
              key={type.id}
              type="button"
              onClick={() => setSearchType(type.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
                searchType === type.id
                  ? 'border-accent-blue bg-accent-blue/10 text-accent-blue'
                  : 'border-dark-border text-gray-400 hover:border-gray-600 hover:text-gray-300'
              }`}
            >
              <type.icon size={16} />
              <span className="text-sm font-medium">{type.label}</span>
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`Search for ${searchType}s...`}
            className="block w-full pl-10 pr-12 py-3 bg-dark-surface border border-dark-border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent"
          />
          <button
            type="submit"
            className="absolute inset-y-0 right-0 px-4 flex items-center bg-accent-blue hover:bg-blue-600 text-white rounded-r-lg transition-colors"
          >
            <Send size={16} />
          </button>
        </div>

        {/* Quick Search Examples */}
        <div className="text-sm text-gray-400">
          <span className="mr-2">Quick search:</span>
          {searchType === 'keyword' && (
            <div className="flex flex-wrap gap-2 mt-2">
              {['#protest', '#election', '#covid', '#climate'].map((keyword) => (
                <button
                  key={keyword}
                  type="button"
                  onClick={() => onSearch(keyword, 'keyword')}
                  className="px-2 py-1 bg-dark-surface rounded text-xs hover:bg-dark-border transition-colors"
                >
                  {keyword}
                </button>
              ))}
            </div>
          )}
          {searchType === 'user' && (
            <div className="flex flex-wrap gap-2 mt-2">
              {['john.doe', 'jane.smith', 'public.figure'].map((user) => (
                <button
                  key={user}
                  type="button"
                  onClick={() => onSearch(user, 'user')}
                  className="px-2 py-1 bg-dark-surface rounded text-xs hover:bg-dark-border transition-colors"
                >
                  {user}
                </button>
              ))}
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default SearchBar;
