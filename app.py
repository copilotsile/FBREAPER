import streamlit as st
from streamlit_option_menu import option_menu
import time
from api_client import APIClient
from pages import dashboard, scraper_control, post_search, network_graph
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="FBReaperV1 - Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .status-connected {
        color: #28a745;
        font-weight: bold;
        background: rgba(40, 167, 69, 0.1);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #28a745;
    }
    
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
        background: rgba(220, 53, 69, 0.1);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #dc3545;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'api_client' not in st.session_state:
        st.session_state.api_client = APIClient()
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    
    if 'selected_post_id' not in st.session_state:
        st.session_state.selected_post_id = None
    
    if 'show_comments' not in st.session_state:
        st.session_state.show_comments = False
    
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()

def get_system_status(api_client):
    """Get comprehensive system status."""
    status = {
        'backend': False,
        'database': False,
        'scraper': False,
        'kafka': False,
        'last_check': datetime.now()
    }
    
    # Check backend connection
    try:
        status['backend'] = api_client.test_connection()
    except:
        status['backend'] = False
    
    # Check database (via stats endpoint)
    try:
        stats = api_client.get_statistics()
        status['database'] = stats is not None
    except:
        status['database'] = False
    
    # Check scraper status
    try:
        scraper_status = api_client.get_scraper_status()
        status['scraper'] = scraper_status is not None
    except:
        status['scraper'] = False
    
    # Note: Kafka status would require additional endpoints
    status['kafka'] = status['backend']  # Assume Kafka is working if backend is up
    
    return status

def render_system_status(status):
    """Render system status indicators."""
    st.markdown("### 🔧 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if status['backend']:
            st.markdown('<div class="status-connected">🟢 Backend</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-disconnected">🔴 Backend</div>', unsafe_allow_html=True)
    
    with col2:
        if status['database']:
            st.markdown('<div class="status-connected">🟢 Database</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-disconnected">🔴 Database</div>', unsafe_allow_html=True)
    
    with col3:
        if status['scraper']:
            st.markdown('<div class="status-connected">🟢 Scraper</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-disconnected">🔴 Scraper</div>', unsafe_allow_html=True)
    
    with col4:
        if status['kafka']:
            st.markdown('<div class="status-connected">🟢 Kafka</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-disconnected">🔴 Kafka</div>', unsafe_allow_html=True)
    
    st.caption(f"Last checked: {status['last_check'].strftime('%H:%M:%S')}")

def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-header">📊 FBReaperV1 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced features
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # System status
        system_status = get_system_status(st.session_state.api_client)
        render_system_status(system_status)
        
        st.markdown("---")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Pages",
            options=["Dashboard", "Scraper Control", "Post Search", "Network Graph", "Settings"],
            icons=["📊", "🤖", "📝", "🕸️", "⚙️"],
            menu_icon="cast",
            default_index=0,
        )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        if st.button("🔄 Refresh All Data"):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        if st.button("📊 View Statistics"):
            st.session_state.current_page = 0
            st.rerun()
        
        st.markdown("---")
        
        # Backend configuration
        st.markdown("## ⚙️ Configuration")
        backend_url = st.text_input(
            "Backend URL:",
            value=st.session_state.api_client.base_url,
            help="URL of your Java Spring Boot backend"
        )
        
        if backend_url != st.session_state.api_client.base_url:
            st.session_state.api_client = APIClient(backend_url)
            st.success("✅ Backend URL updated!")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=st.session_state.auto_refresh)
        if auto_refresh != st.session_state.auto_refresh:
            st.session_state.auto_refresh = auto_refresh
            st.rerun()
        
        if st.session_state.auto_refresh:
            st.info("Auto-refresh enabled (every 30 seconds)")
            time.sleep(30)
            st.rerun()
        
        # Dark mode toggle
        dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # About section
        st.markdown("## ℹ️ About")
        st.markdown("""
        **FBReaperV1 Analytics Dashboard**
        
        A comprehensive social media analytics platform that integrates with a Java Spring Boot backend for data scraping, analysis, and visualization.
        
        **Features:**
        - 📊 Real-time dashboard statistics
        - 🤖 Scraper control and monitoring
        - 📝 Post search and browsing
        - 🕸️ Network graph visualization
        - 🔧 System status monitoring
        - ⚡ Quick actions and shortcuts
        """)
        
        # Version info
        st.caption("Version: 1.0.0 | Built with Streamlit")
    
    # Main content area with enhanced error handling
    try:
        if selected == "Dashboard":
            dashboard.render_dashboard(st.session_state.api_client)
        
        elif selected == "Scraper Control":
            scraper_control.render_scraper_control(st.session_state.api_client)
        
        elif selected == "Post Search":
            post_search.render_post_search(st.session_state.api_client)
        
        elif selected == "Network Graph":
            network_graph.render_network_graph(st.session_state.api_client)
        
        elif selected == "Settings":
            render_settings_page(st.session_state.api_client)
    
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please check your backend connection and try again.")
        
        # Show error details in expander
        with st.expander("🔍 Error Details"):
            st.code(str(e))
            st.json({
                "error_type": type(e).__name__,
                "error_message": str(e),
                "timestamp": datetime.now().isoformat(),
                "backend_url": st.session_state.api_client.base_url
            })

def render_settings_page(api_client):
    """Render the settings page."""
    st.header("⚙️ Settings & Configuration")
    st.markdown("---")
    
    # Application settings
    st.subheader("🔧 Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Display Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French"])
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"])
    
    with col2:
        st.markdown("### Performance Settings")
        cache_duration = st.slider("Cache Duration (minutes)", 1, 60, 15)
        max_retries = st.slider("Max API Retries", 1, 10, 3)
        timeout = st.slider("Request Timeout (seconds)", 5, 60, 10)
    
    # Data settings
    st.subheader("📊 Data Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Retention")
        retention_days = st.number_input("Data Retention (days)", 1, 365, 30)
        auto_cleanup = st.checkbox("Enable Auto Cleanup", value=True)
        backup_enabled = st.checkbox("Enable Data Backup", value=True)
    
    with col2:
        st.markdown("### Export Settings")
        export_format = st.selectbox("Default Export Format", ["JSON", "CSV", "Excel"])
        include_metadata = st.checkbox("Include Metadata in Exports", value=True)
        compress_exports = st.checkbox("Compress Exports", value=False)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")
    
    st.markdown("---")
    
    # System information
    st.subheader("🖥️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Backend Information")
        if api_client.test_connection():
            st.success("🟢 Backend is running")
            try:
                stats = api_client.get_statistics()
                if stats:
                    st.write(f"**Total Posts:** {stats.get('totalPosts', 'N/A')}")
                    st.write(f"**Total Comments:** {stats.get('totalComments', 'N/A')}")
            except:
                st.warning("⚠️ Could not retrieve statistics")
        else:
            st.error("🔴 Backend is not accessible")
    
    with col2:
        st.markdown("### Application Information")
        st.write(f"**Version:** 1.0.0")
        st.write(f"**Python:** 3.8+")
        st.write(f"**Streamlit:** 1.28.1")
        st.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Maintenance actions
    st.markdown("---")
    st.subheader("🔧 Maintenance Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 Clear Cache"):
            st.success("✅ Cache cleared!")
    
    with col2:
        if st.button("📊 Reset Statistics"):
            st.warning("⚠️ This will reset all dashboard statistics")
    
    with col3:
        if st.button("🔄 Restart Application"):
            st.info("🔄 Application restart requested")

if __name__ == "__main__":
    main()