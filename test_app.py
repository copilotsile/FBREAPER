#!/usr/bin/env python3
"""
Simple test script to verify the Streamlit application components.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient

def test_api_client():
    """Test the API client functionality."""
    print("🧪 Testing API Client...")
    
    # Create API client
    client = APIClient("http://localhost:8080")
    
    # Test connection
    print("  Testing connection...")
    if client.test_connection():
        print("  ✅ Backend connection successful")
    else:
        print("  ❌ Backend connection failed")
        print("  ℹ️  Make sure your Java Spring Boot backend is running on http://localhost:8080")
        return False
    
    # Test endpoints
    print("  Testing endpoints...")
    
    # Test health endpoint
    try:
        response = client.session.get(f"{client.base_url}/api/health")
        if response.status_code == 200:
            print("  ✅ Health endpoint working")
        else:
            print(f"  ❌ Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health endpoint error: {e}")
    
    # Test data endpoints
    try:
        posts = client.get_posts()
        if posts is not None:
            print(f"  ✅ Posts endpoint working (found {len(posts) if isinstance(posts, list) else 1} posts)")
        else:
            print("  ⚠️  Posts endpoint returned None")
    except Exception as e:
        print(f"  ❌ Posts endpoint error: {e}")
    
    try:
        stats = client.get_statistics()
        if stats is not None:
            print("  ✅ Statistics endpoint working")
        else:
            print("  ⚠️  Statistics endpoint returned None")
    except Exception as e:
        print(f"  ❌ Statistics endpoint error: {e}")
    
    return True

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("  ✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return False
    
    try:
        from streamlit_option_menu import option_menu
        print("  ✅ streamlit-option-menu imported successfully")
    except ImportError as e:
        print(f"  ❌ streamlit-option-menu import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("  ✅ Plotly imported successfully")
    except ImportError as e:
        print(f"  ❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("  ✅ Pandas imported successfully")
    except ImportError as e:
        print(f"  ❌ Pandas import failed: {e}")
        return False
    
    try:
        from pyvis.network import Network
        print("  ✅ PyVis imported successfully")
    except ImportError as e:
        print(f"  ❌ PyVis import failed: {e}")
        return False
    
    try:
        import networkx as nx
        print("  ✅ NetworkX imported successfully")
    except ImportError as e:
        print(f"  ❌ NetworkX import failed: {e}")
        return False
    
    return True

def test_pages():
    """Test that all page modules can be imported."""
    print("🧪 Testing page modules...")
    
    try:
        from pages import dashboard, scraper_control, post_search, network_graph
        print("  ✅ All page modules imported successfully")
    except ImportError as e:
        print(f"  ❌ Page module import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Starting FBReaperV1 Streamlit App Tests")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    print()
    
    # Test page modules
    if not test_pages():
        print("\n❌ Page module tests failed.")
        return False
    
    print()
    
    # Test API client
    if not test_api_client():
        print("\n❌ API client tests failed.")
        print("   Make sure your Java Spring Boot backend is running.")
        return False
    
    print()
    print("✅ All tests passed!")
    print("\n🎉 Your Streamlit application is ready to run!")
    print("   Run: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)