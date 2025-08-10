import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time

def render_dashboard(api_client):
    """Render the dashboard page with statistics and charts."""
    
    st.header("📊 Dashboard Statistics")
    st.markdown("---")
    
    # Auto-refresh every 30 seconds
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Get statistics with loading spinner
    with st.spinner("Loading dashboard statistics..."):
        stats_data = api_client.get_statistics()
    
    if not stats_data:
        st.warning("⚠️ Unable to load statistics. Please check your backend connection.")
        return
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Posts",
            value=stats_data.get('totalPosts', 0),
            delta=stats_data.get('postsToday', 0)
        )
    
    with col2:
        st.metric(
            label="Total Comments",
            value=stats_data.get('totalComments', 0),
            delta=stats_data.get('commentsToday', 0)
        )
    
    with col3:
        st.metric(
            label="Active Users",
            value=stats_data.get('activeUsers', 0),
            delta=stats_data.get('newUsersToday', 0)
        )
    
    with col4:
        st.metric(
            label="Scraping Sessions",
            value=stats_data.get('scrapingSessions', 0),
            delta=stats_data.get('sessionsToday', 0)
        )
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Posts Over Time")
        if 'postsOverTime' in stats_data and stats_data['postsOverTime']:
            df_posts = pd.DataFrame(stats_data['postsOverTime'])
            if not df_posts.empty:
                fig_posts = px.line(
                    df_posts, 
                    x='date', 
                    y='count',
                    title="Posts Collected Over Time"
                )
                fig_posts.update_layout(height=400)
                st.plotly_chart(fig_posts, use_container_width=True)
            else:
                st.info("No posts data available for charting.")
        else:
            st.info("No posts time series data available.")
    
    with col2:
        st.subheader("💬 Comments Over Time")
        if 'commentsOverTime' in stats_data and stats_data['commentsOverTime']:
            df_comments = pd.DataFrame(stats_data['commentsOverTime'])
            if not df_comments.empty:
                fig_comments = px.line(
                    df_comments, 
                    x='date', 
                    y='count',
                    title="Comments Collected Over Time"
                )
                fig_comments.update_layout(height=400)
                st.plotly_chart(fig_comments, use_container_width=True)
            else:
                st.info("No comments data available for charting.")
        else:
            st.info("No comments time series data available.")
    
    # Top keywords chart
    st.subheader("🔍 Top Keywords")
    if 'topKeywords' in stats_data and stats_data['topKeywords']:
        df_keywords = pd.DataFrame(stats_data['topKeywords'])
        if not df_keywords.empty:
            fig_keywords = px.bar(
                df_keywords,
                x='keyword',
                y='count',
                title="Most Scraped Keywords"
            )
            fig_keywords.update_layout(height=400)
            st.plotly_chart(fig_keywords, use_container_width=True)
        else:
            st.info("No keyword data available.")
    else:
        st.info("No keyword statistics available.")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    if 'recentActivity' in stats_data and stats_data['recentActivity']:
        for activity in stats_data['recentActivity'][:10]:
            timestamp = activity.get('timestamp', 'Unknown')
            action = activity.get('action', 'Unknown')
            details = activity.get('details', '')
            
            st.info(f"**{timestamp}** - {action}: {details}")
    else:
        st.info("No recent activity data available.")