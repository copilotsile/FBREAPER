import requests
import json
import time
from typing import Dict, List, Optional, Any
import streamlit as st

class APIClient:
    """Client for communicating with the Java Spring Boot backend API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {self.base_url}. Please ensure the Java Spring Boot server is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTP Error {e.response.status_code}: {e.response.text}")
            return None
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON response from server.")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def start_scraper(self, keyword: str) -> Optional[Dict]:
        """Start the scraper with a keyword."""
        data = {"keyword": keyword}
        return self._make_request('POST', '/api/scraper/scrapeByKeyword', data=data)
    
    def get_scraper_status(self) -> Optional[Dict]:
        """Get the current scraper status."""
        return self._make_request('GET', '/api/scraper/status')
    
    def get_posts(self, page: int = 0, size: int = 20) -> Optional[Dict]:
        """Get posts with pagination."""
        params = {"page": page, "size": size}
        return self._make_request('GET', '/api/data/posts', params=params)
    
    def get_post_comments(self, post_id: str) -> Optional[Dict]:
        """Get comments for a specific post."""
        return self._make_request('GET', f'/api/data/posts/{post_id}/comments')
    
    def get_network_graph(self) -> Optional[Dict]:
        """Get network graph data."""
        return self._make_request('GET', '/api/network/graph')
    
    def get_statistics(self) -> Optional[Dict]:
        """Get dashboard statistics."""
        return self._make_request('GET', '/api/data/stats')
    
    def stop_scraper(self) -> Optional[Dict]:
        """Stop the scraper."""
        return self._make_request('POST', '/api/scraper/stop')
    
    def test_connection(self) -> bool:
        """Test if the backend is reachable."""
        try:
            response = self.session.get(f"{self.base_url}/api/scraper/status", timeout=5)
            return response.status_code == 200
        except:
            return False