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
        # Note: Backend doesn't support pagination parameters, but we'll handle it client-side
        return self._make_request('GET', '/api/data/posts')
    
    def get_post_comments(self, post_id: str) -> Optional[Dict]:
        """Get comments for a specific post."""
        # Note: Backend doesn't have direct post->comments endpoint, we'll get all comments and filter
        return self._make_request('GET', '/api/data/comments')
    
    def get_network_graph(self) -> Optional[Dict]:
        """Get network graph data."""
        # Note: Backend doesn't have network graph endpoint, we'll use link analysis
        return None
    
    def get_statistics(self) -> Optional[Dict]:
        """Get dashboard statistics."""
        return self._make_request('GET', '/api/data/stats')
    
    def stop_scraper(self) -> Optional[Dict]:
        """Stop the scraper."""
        # Note: Backend doesn't have stop endpoint, we'll use the status endpoint
        return None
    
    def test_connection(self) -> bool:
        """Test if the backend is reachable."""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_link_analysis(self, post_id: str) -> Optional[Dict]:
        """Get link analysis for a specific post."""
        return self._make_request('GET', f'/api/link-analysis/{post_id}')
    
    def get_post_by_id(self, post_id: str) -> Optional[Dict]:
        """Get a specific post by ID."""
        return self._make_request('GET', f'/api/posts/{post_id}')
    
    def get_comment_by_id(self, comment_id: str) -> Optional[Dict]:
        """Get a specific comment by ID."""
        return self._make_request('GET', f'/api/comments/{comment_id}')