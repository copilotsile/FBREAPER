import streamlit as st
from streamlit_option_menu import option_menu
import time
from api_client import APIClient
from pages import dashboard, scraper_control, post_search, network_graph

# Page configuration
st.set_page_config(
    page_title="FBReaperV1 - Social Media Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    .status-connected {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
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

def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📊 FBReaperV1 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Connection status
        if st.session_state.api_client.test_connection():
            st.success("🟢 Backend Connected")
        else:
            st.error("🔴 Backend Disconnected")
            st.info("Please ensure your Java Spring Boot backend is running on http://localhost:8080")
        
        st.markdown("---")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Pages",
            options=["Dashboard", "Scraper Control", "Post Search", "Network Graph"],
            icons=["📊", "🤖", "📝", "🕸️"],
            menu_icon="cast",
            default_index=0,
        )
        
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
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
        if auto_refresh:
            st.info("Auto-refresh enabled (every 30 seconds)")
            time.sleep(30)
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
        """)
    
    # Main content area
    try:
        if selected == "Dashboard":
            dashboard.render_dashboard(st.session_state.api_client)
        
        elif selected == "Scraper Control":
            scraper_control.render_scraper_control(st.session_state.api_client)
        
        elif selected == "Post Search":
            post_search.render_post_search(st.session_state.api_client)
        
        elif selected == "Network Graph":
            network_graph.render_network_graph(st.session_state.api_client)
    
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please check your backend connection and try again.")
        
        # Show error details in expander
        with st.expander("🔍 Error Details"):
            st.code(str(e))

if __name__ == "__main__":
    main()