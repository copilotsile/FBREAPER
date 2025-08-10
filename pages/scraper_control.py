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
    
    with st.spinner("Loading scraper status..."):
        status_data = api_client.get_scraper_status()
    
    if not status_data:
        st.warning("⚠️ Unable to load scraper status.")
        return
    
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
        
        if status_data.get('status') == 'RUNNING':
            if st.button("🛑 Stop Scraper", type="primary"):
                with st.spinner("Stopping scraper..."):
                    result = api_client.stop_scraper()
                
                if result:
                    st.success("✅ Scraper stopped successfully")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Failed to stop scraper.")
        else:
            st.info("ℹ️ No active scraping session to stop.")
    
    st.markdown("---")
    
    # Session History
    st.subheader("📋 Recent Sessions")
    
    if 'sessionHistory' in status_data and status_data['sessionHistory']:
        for session in status_data['sessionHistory'][:5]:
            with st.expander(f"Session: {session.get('sessionId', 'N/A')} - {session.get('keyword', 'N/A')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {session.get('status', 'Unknown')}")
                
                with col2:
                    st.write(f"**Started:** {session.get('startTime', 'Unknown')}")
                
                with col3:
                    st.write(f"**Posts:** {session.get('postsCollected', 0)}")
                
                if session.get('endTime'):
                    st.write(f"**Ended:** {session['endTime']}")
                
                if session.get('error'):
                    st.error(f"**Error:** {session['error']}")
    else:
        st.info("No recent sessions found.")
    
    # Real-time monitoring
    st.markdown("---")
    st.subheader("📡 Real-time Monitoring")
    
    if st.checkbox("Enable auto-refresh (every 10 seconds)"):
        st.info("🔄 Auto-refresh enabled. The status will update automatically.")
        time.sleep(10)
        st.rerun()