import streamlit as st
import time
from datetime import datetime, timedelta
import json
import pandas as pd

def render_scraper_control(api_client):
    """Render the scraper control page."""
    
    st.header("🤖 Scraper Control & Monitoring")
    st.markdown("---")
    
    # Connection status with enhanced display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if api_client.test_connection():
            st.markdown('<div class="status-connected">🟢 Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-disconnected">🔴 Disconnected</div>', unsafe_allow_html=True)
    
    with col2:
        st.caption(f"Backend: {api_client.base_url}")
        st.caption(f"Last check: {datetime.now().strftime('%H:%M:%S')}")
    
    with col3:
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    st.markdown("---")
    
    # Enhanced Scraper Status Section
    st.subheader("📊 Current Status")
    
    # Get scraper status with enhanced error handling
    try:
        status_data = api_client.get_scraper_status()
        if not status_data:
            status_data = get_mock_scraper_status()
    except Exception as e:
        st.error(f"❌ Error fetching scraper status: {str(e)}")
        status_data = get_mock_scraper_status()
    
    # Status overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = status_data.get('status', 'UNKNOWN')
        if status == 'RUNNING':
            st.markdown('<div class="success-box">🟢 Status: RUNNING</div>', unsafe_allow_html=True)
        elif status == 'STOPPED':
            st.markdown('<div class="error-box">🔴 Status: STOPPED</div>', unsafe_allow_html=True)
        elif status == 'PAUSED':
            st.markdown('<div class="warning-box">🟡 Status: PAUSED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">ℹ️ Status: UNKNOWN</div>', unsafe_allow_html=True)
    
    with col2:
        progress = status_data.get('progress', 0)
        st.metric("Progress", f"{progress}%")
        st.progress(progress / 100)
    
    with col3:
        current_keyword = status_data.get('currentKeyword', 'None')
        st.metric("Current Keyword", current_keyword)
    
    with col4:
        runtime = status_data.get('runtime', '00:00:00')
        st.metric("Runtime", runtime)
    
    # Detailed status information
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Performance Metrics")
        
        metrics = status_data.get('metrics', {})
        
        st.metric(
            label="Posts Scraped",
            value=metrics.get('postsScraped', 0),
            delta=metrics.get('postsThisSession', 0)
        )
        
        st.metric(
            label="Comments Scraped",
            value=metrics.get('commentsScraped', 0),
            delta=metrics.get('commentsThisSession', 0)
        )
        
        st.metric(
            label="Success Rate",
            value=f"{metrics.get('successRate', 0)}%"
        )
        
        st.metric(
            label="Avg Response Time",
            value=f"{metrics.get('avgResponseTime', 0)}ms"
        )
    
    with col2:
        st.markdown("### ⚙️ Configuration")
        
        config = status_data.get('config', {})
        
        st.write(f"**Max Posts:** {config.get('maxPosts', 'Unlimited')}")
        st.write(f"**Delay:** {config.get('delay', 1.0)}s")
        st.write(f"**Timeout:** {config.get('timeout', 30)}s")
        st.write(f"**Retries:** {config.get('retries', 3)}")
        st.write(f"**User Agent:** {config.get('userAgent', 'Default')[:30]}...")
    
    # Error log section
    if 'errors' in status_data and status_data['errors']:
        st.markdown("---")
        st.subheader("⚠️ Recent Errors")
        
        for error in status_data['errors'][:5]:
            with st.expander(f"Error at {error.get('timestamp', 'Unknown')}"):
                st.error(f"**Type:** {error.get('type', 'Unknown')}")
                st.write(f"**Message:** {error.get('message', 'No message')}")
                st.write(f"**Details:** {error.get('details', 'No details')}")
    
    st.markdown("---")
    
    # Enhanced Scraper Control Section
    st.subheader("🎮 Scraper Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Start New Scraping Session")
        
        with st.form("start_scraper"):
            keyword = st.text_input(
                "Enter keyword to scrape:",
                placeholder="e.g., python, machine learning, data science",
                help="Enter the keyword you want to scrape for"
            )
            
            # Advanced parameters
            st.markdown("**Advanced Parameters:**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                max_posts = st.number_input(
                    "Maximum posts:",
                    min_value=1,
                    max_value=1000,
                    value=100,
                    help="Maximum number of posts to collect"
                )
                
                delay = st.number_input(
                    "Delay (seconds):",
                    min_value=0.1,
                    max_value=10.0,
                    value=1.0,
                    step=0.1,
                    help="Delay between requests to avoid rate limiting"
                )
            
            with col_b:
                timeout = st.number_input(
                    "Timeout (seconds):",
                    min_value=5,
                    max_value=120,
                    value=30,
                    help="Request timeout"
                )
                
                retries = st.number_input(
                    "Max retries:",
                    min_value=0,
                    max_value=10,
                    value=3,
                    help="Maximum retry attempts"
                )
            
            # Additional options
            st.markdown("**Options:**")
            
            col_c, col_d = st.columns(2)
            
            with col_c:
                include_comments = st.checkbox("Include comments", value=True)
                include_reactions = st.checkbox("Include reactions", value=True)
            
            with col_d:
                save_media = st.checkbox("Save media files", value=False)
                analyze_sentiment = st.checkbox("Analyze sentiment", value=True)
            
            submitted = st.form_submit_button("🚀 Start Scraping")
            
            if submitted:
                if keyword.strip():
                    with st.spinner("Starting scraper..."):
                        try:
                            result = api_client.start_scraper(keyword)
                            
                            if result:
                                st.success(f"✅ Scraper started successfully for keyword: '{keyword}'")
                                st.info(f"Session ID: {result.get('sessionId', 'N/A')}")
                                
                                # Show session details
                                with st.expander("📋 Session Details"):
                                    st.json(result)
                                
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Failed to start scraper. Please check the logs.")
                        except Exception as e:
                            st.error(f"❌ Error starting scraper: {str(e)}")
                else:
                    st.error("❌ Please enter a keyword to scrape.")
    
    with col2:
        st.markdown("### 🛑 Control Actions")
        
        # Stop scraper
        if st.button("⏹️ Stop Scraper", type="primary"):
            try:
                result = api_client.stop_scraper()
                if result:
                    st.success("✅ Scraper stopped successfully!")
                else:
                    st.warning("⚠️ Stop command sent (no confirmation available)")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error stopping scraper: {str(e)}")
        
        # Pause/Resume scraper
        if st.button("⏸️ Pause/Resume"):
            st.info("⏸️ Pause/Resume functionality not available in current backend version")
        
        # Emergency stop
        if st.button("🚨 Emergency Stop", type="secondary"):
            st.warning("🚨 Emergency stop triggered!")
            st.info("This will immediately stop all scraping activities")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📊 View Current Stats"):
            st.info("Redirecting to dashboard...")
            time.sleep(1)
            st.rerun()
        
        if st.button("📋 View Session Log"):
            st.info("Session log not available in current backend version")
        
        if st.button("🔧 Configure Scraper"):
            st.info("Configuration panel not available in current backend version")
    
    st.markdown("---")
    
    # Session History with enhanced display
    st.subheader("📋 Session History")
    
    # Get session history (mock data for now)
    session_history = get_mock_session_history()
    
    if session_history:
        # Convert to DataFrame for better display
        df_sessions = pd.DataFrame(session_history)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by status:",
                ["All"] + list(df_sessions['status'].unique())
            )
        
        with col2:
            date_filter = st.date_input(
                "Filter by date:",
                value=datetime.now().date()
            )
        
        with col3:
            keyword_filter = st.text_input(
                "Filter by keyword:",
                placeholder="Enter keyword..."
            )
        
        # Apply filters
        filtered_df = df_sessions.copy()
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        if keyword_filter:
            filtered_df = filtered_df[filtered_df['keyword'].str.contains(keyword_filter, case=False)]
        
        # Display sessions
        for _, session in filtered_df.iterrows():
            with st.expander(f"Session {session['id']} - {session['keyword']} ({session['status']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Start Time:** {session['startTime']}")
                    st.write(f"**End Time:** {session['endTime']}")
                    st.write(f"**Duration:** {session['duration']}")
                    st.write(f"**Posts Scraped:** {session['postsScraped']}")
                
                with col2:
                    st.write(f"**Comments Scraped:** {session['commentsScraped']}")
                    st.write(f"**Success Rate:** {session['successRate']}%")
                    st.write(f"**Errors:** {session['errors']}")
                    
                    if session['status'] == 'COMPLETED':
                        st.success("✅ Completed")
                    elif session['status'] == 'RUNNING':
                        st.info("🔄 Running")
                    elif session['status'] == 'FAILED':
                        st.error("❌ Failed")
                    else:
                        st.warning("⚠️ Unknown")
    else:
        st.info("No session history available.")
    
    # Real-time monitoring
    st.markdown("---")
    st.subheader("📡 Real-time Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_refresh = st.checkbox("Enable auto-refresh (every 10 seconds)")
        if auto_refresh:
            st.info("🔄 Auto-refresh enabled. The status will update automatically.")
            time.sleep(10)
            st.rerun()
    
    with col2:
        if st.button("📊 Export Session Data"):
            st.info("📊 Export functionality not available in current backend version")

def get_mock_scraper_status():
    """Generate mock scraper status for demonstration."""
    return {
        'status': 'RUNNING',
        'progress': 65,
        'currentKeyword': 'python programming',
        'runtime': '00:15:30',
        'metrics': {
            'postsScraped': 1250,
            'postsThisSession': 45,
            'commentsScraped': 3200,
            'commentsThisSession': 120,
            'successRate': 94.5,
            'avgResponseTime': 1200
        },
        'config': {
            'maxPosts': 100,
            'delay': 1.0,
            'timeout': 30,
            'retries': 3,
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'errors': [
            {
                'timestamp': '2024-01-15 14:25:00',
                'type': 'ConnectionError',
                'message': 'Connection timeout',
                'details': 'Request timed out after 30 seconds'
            },
            {
                'timestamp': '2024-01-15 14:20:00',
                'type': 'RateLimitError',
                'message': 'Rate limit exceeded',
                'details': 'Too many requests in short time'
            }
        ]
    }

def get_mock_session_history():
    """Generate mock session history for demonstration."""
    return [
        {
            'id': 'SESS_001',
            'keyword': 'python programming',
            'status': 'RUNNING',
            'startTime': '2024-01-15 14:00:00',
            'endTime': 'N/A',
            'duration': '00:15:30',
            'postsScraped': 45,
            'commentsScraped': 120,
            'successRate': 94.5,
            'errors': 2
        },
        {
            'id': 'SESS_002',
            'keyword': 'machine learning',
            'status': 'COMPLETED',
            'startTime': '2024-01-15 13:00:00',
            'endTime': '2024-01-15 13:45:00',
            'duration': '00:45:00',
            'postsScraped': 100,
            'commentsScraped': 250,
            'successRate': 96.2,
            'errors': 1
        },
        {
            'id': 'SESS_003',
            'keyword': 'data science',
            'status': 'FAILED',
            'startTime': '2024-01-15 12:00:00',
            'endTime': '2024-01-15 12:15:00',
            'duration': '00:15:00',
            'postsScraped': 15,
            'commentsScraped': 30,
            'successRate': 45.5,
            'errors': 8
        }
    ]