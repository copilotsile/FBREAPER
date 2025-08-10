import streamlit as st
import time
from datetime import datetime

def render_scraper_control(api_client):
    """Render the scraper control page."""
    
    st.header("🤖 Scraper Control")
    st.markdown("---")
    
    # Connection status
    col1, col2 = st.columns([1, 3])
    with col1:
        if api_client.test_connection():
            st.success("🟢 Connected")
        else:
            st.error("🔴 Disconnected")
    
    with col2:
        st.caption(f"Backend: {api_client.base_url}")
    
    st.markdown("---")
    
    # Scraper Status Section
    st.subheader("📊 Current Status")
    
    # Auto-refresh status
    if st.button("🔄 Refresh Status"):
        st.rerun()
    
    # Note: Backend doesn't have a dedicated status endpoint, so we'll show a simplified status
    status_data = {
        'status': 'UNKNOWN',
        'progress': 0,
        'currentKeyword': 'None',
        'details': 'Status monitoring not available in current backend version'
    }
    
    # Display status information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = status_data.get('status', 'Unknown')
        if status == 'RUNNING':
            st.success(f"🟢 Status: {status}")
        elif status == 'STOPPED':
            st.error(f"🔴 Status: {status}")
        elif status == 'PAUSED':
            st.warning(f"🟡 Status: {status}")
        else:
            st.info(f"ℹ️ Status: {status}")
    
    with col2:
        progress = status_data.get('progress', 0)
        st.metric("Progress", f"{progress}%")
    
    with col3:
        current_keyword = status_data.get('currentKeyword', 'None')
        st.metric("Current Keyword", current_keyword)
    
    # Progress bar
    if 'progress' in status_data:
        st.progress(status_data['progress'] / 100)
    
    # Status details
    if 'details' in status_data:
        st.info(f"**Details:** {status_data['details']}")
    
    st.markdown("---")
    
    # Scraper Control Section
    st.subheader("🎮 Scraper Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Start New Scraping Session")
        
        with st.form("start_scraper"):
            keyword = st.text_input(
                "Enter keyword to scrape:",
                placeholder="e.g., python, machine learning, data science",
                help="Enter the keyword you want to scrape for"
            )
            
            # Optional parameters
            st.markdown("**Optional Parameters:**")
            max_posts = st.number_input(
                "Maximum posts to scrape:",
                min_value=1,
                max_value=1000,
                value=100,
                help="Maximum number of posts to collect"
            )
            
            delay = st.number_input(
                "Delay between requests (seconds):",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1,
                help="Delay to avoid rate limiting"
            )
            
            submitted = st.form_submit_button("🚀 Start Scraping")
            
            if submitted:
                if keyword.strip():
                    with st.spinner("Starting scraper..."):
                        result = api_client.start_scraper(keyword)
                    
                    if result:
                        st.success(f"✅ Scraper started successfully for keyword: '{keyword}'")
                        st.info(f"Session ID: {result.get('sessionId', 'N/A')}")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Failed to start scraper. Please check the logs.")
                else:
                    st.error("❌ Please enter a keyword to scrape.")
    
    with col2:
        st.markdown("### Stop Current Session")
        
        st.info("ℹ️ Stop functionality not available in current backend version.")
        st.caption("The backend doesn't provide a stop endpoint. You may need to manually stop the scraper process.")
    
    st.markdown("---")
    
    # Session History
    st.subheader("📋 Recent Sessions")
    st.info("Session history not available in current backend version.")
    st.caption("The backend doesn't provide session history tracking.")
    
    # Real-time monitoring
    st.markdown("---")
    st.subheader("📡 Real-time Monitoring")
    
    if st.checkbox("Enable auto-refresh (every 10 seconds)"):
        st.info("🔄 Auto-refresh enabled. The status will update automatically.")
        time.sleep(10)
        st.rerun()