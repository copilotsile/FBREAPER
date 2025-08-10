import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np

def render_dashboard(api_client):
    """Render the dashboard page with statistics and charts."""
    
    st.header("📊 Dashboard Statistics")
    st.markdown("---")
    
    # Auto-refresh every 30 seconds
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    with col2:
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    with col3:
        if st.checkbox("🔄 Auto-refresh (30s)"):
            time.sleep(30)
            st.rerun()
    
    # Get statistics with loading spinner
    with st.spinner("Loading dashboard statistics..."):
        stats_data = api_client.get_statistics()
    
    if not stats_data:
        st.warning("⚠️ Unable to load statistics. Please check your backend connection.")
        
        # Show mock data for demonstration
        st.info("📊 Showing demo data for demonstration purposes")
        stats_data = get_mock_statistics()
    
    # Display key metrics in columns with enhanced styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📄 Total Posts</h3>
            <h2>{}</h2>
            <p>+{} today</p>
        </div>
        """.format(
            stats_data.get('totalPosts', 0),
            stats_data.get('postsToday', 0)
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💬 Total Comments</h3>
            <h2>{}</h2>
            <p>+{} today</p>
        </div>
        """.format(
            stats_data.get('totalComments', 0),
            stats_data.get('commentsToday', 0)
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Active Users</h3>
            <h2>{}</h2>
            <p>+{} today</p>
        </div>
        """.format(
            stats_data.get('activeUsers', 0),
            stats_data.get('newUsersToday', 0)
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 Scraping Sessions</h3>
            <h2>{}</h2>
            <p>+{} today</p>
        </div>
        """.format(
            stats_data.get('scrapingSessions', 0),
            stats_data.get('sessionsToday', 0)
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced analytics section
    st.subheader("📈 Advanced Analytics")
    
    # Charts section with enhanced layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Posts Over Time")
        if 'postsOverTime' in stats_data and stats_data['postsOverTime']:
            df_posts = pd.DataFrame(stats_data['postsOverTime'])
            if not df_posts.empty:
                fig_posts = px.line(
                    df_posts, 
                    x='date', 
                    y='count',
                    title="Posts Collected Over Time",
                    color_discrete_sequence=['#667eea']
                )
                fig_posts.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#333')
                )
                st.plotly_chart(fig_posts, use_container_width=True)
            else:
                st.info("No posts data available for charting.")
        else:
            # Show mock data
            mock_posts_data = generate_mock_time_series_data('posts')
            df_posts = pd.DataFrame(mock_posts_data)
            fig_posts = px.line(
                df_posts, 
                x='date', 
                y='count',
                title="Posts Collected Over Time (Demo)",
                color_discrete_sequence=['#667eea']
            )
            fig_posts.update_layout(height=400)
            st.plotly_chart(fig_posts, use_container_width=True)
    
    with col2:
        st.markdown("### 💬 Comments Over Time")
        if 'commentsOverTime' in stats_data and stats_data['commentsOverTime']:
            df_comments = pd.DataFrame(stats_data['commentsOverTime'])
            if not df_comments.empty:
                fig_comments = px.line(
                    df_comments, 
                    x='date', 
                    y='count',
                    title="Comments Collected Over Time",
                    color_discrete_sequence=['#764ba2']
                )
                fig_comments.update_layout(height=400)
                st.plotly_chart(fig_comments, use_container_width=True)
            else:
                st.info("No comments data available for charting.")
        else:
            # Show mock data
            mock_comments_data = generate_mock_time_series_data('comments')
            df_comments = pd.DataFrame(mock_comments_data)
            fig_comments = px.line(
                df_comments, 
                x='date', 
                y='count',
                title="Comments Collected Over Time (Demo)",
                color_discrete_sequence=['#764ba2']
            )
            fig_comments.update_layout(height=400)
            st.plotly_chart(fig_comments, use_container_width=True)
    
    # Sentiment analysis section
    st.markdown("---")
    st.subheader("😊 Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution pie chart
        sentiment_data = stats_data.get('sentimentDistribution', {
            'positive': 45,
            'neutral': 35,
            'negative': 20
        })
        
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=list(sentiment_data.keys()),
            values=list(sentiment_data.values()),
            hole=0.4,
            marker_colors=['#28a745', '#ffc107', '#dc3545']
        )])
        
        fig_sentiment.update_layout(
            title="Sentiment Distribution",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Sentiment over time
        sentiment_time_data = stats_data.get('sentimentOverTime', generate_mock_sentiment_data())
        df_sentiment = pd.DataFrame(sentiment_time_data)
        
        if not df_sentiment.empty:
            fig_sentiment_time = px.line(
                df_sentiment,
                x='date',
                y=['positive', 'neutral', 'negative'],
                title="Sentiment Trends Over Time",
                color_discrete_map={
                    'positive': '#28a745',
                    'neutral': '#ffc107',
                    'negative': '#dc3545'
                }
            )
            fig_sentiment_time.update_layout(height=400)
            st.plotly_chart(fig_sentiment_time, use_container_width=True)
        else:
            st.info("No sentiment time series data available.")
    
    # Top keywords and hashtags
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Top Keywords")
        if 'topKeywords' in stats_data and stats_data['topKeywords']:
            df_keywords = pd.DataFrame(stats_data['topKeywords'])
            if not df_keywords.empty:
                fig_keywords = px.bar(
                    df_keywords,
                    x='keyword',
                    y='count',
                    title="Most Scraped Keywords",
                    color_discrete_sequence=['#667eea']
                )
                fig_keywords.update_layout(height=400)
                st.plotly_chart(fig_keywords, use_container_width=True)
            else:
                st.info("No keyword data available.")
        else:
            # Show mock data
            mock_keywords = [
                {'keyword': 'python', 'count': 150},
                {'keyword': 'machine learning', 'count': 120},
                {'keyword': 'data science', 'count': 95},
                {'keyword': 'AI', 'count': 80},
                {'keyword': 'programming', 'count': 65}
            ]
            df_keywords = pd.DataFrame(mock_keywords)
            fig_keywords = px.bar(
                df_keywords,
                x='keyword',
                y='count',
                title="Most Scraped Keywords (Demo)",
                color_discrete_sequence=['#667eea']
            )
            fig_keywords.update_layout(height=400)
            st.plotly_chart(fig_keywords, use_container_width=True)
    
    with col2:
        st.subheader("🏷️ Top Hashtags")
        hashtag_data = stats_data.get('topHashtags', [
            {'hashtag': '#python', 'count': 200},
            {'hashtag': '#datascience', 'count': 180},
            {'hashtag': '#machinelearning', 'count': 160},
            {'hashtag': '#AI', 'count': 140},
            {'hashtag': '#programming', 'count': 120}
        ])
        
        df_hashtags = pd.DataFrame(hashtag_data)
        fig_hashtags = px.bar(
            df_hashtags,
            x='hashtag',
            y='count',
            title="Most Used Hashtags",
            color_discrete_sequence=['#764ba2']
        )
        fig_hashtags.update_layout(height=400)
        st.plotly_chart(fig_hashtags, use_container_width=True)
    
    # User engagement metrics
    st.markdown("---")
    st.subheader("👥 User Engagement Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    engagement_data = stats_data.get('engagementMetrics', {
        'avgLikes': 45,
        'avgComments': 12,
        'avgShares': 8,
        'engagementRate': 3.2
    })
    
    with col1:
        st.metric(
            label="Avg Likes per Post",
            value=engagement_data.get('avgLikes', 0),
            delta=2.5
        )
    
    with col2:
        st.metric(
            label="Avg Comments per Post",
            value=engagement_data.get('avgComments', 0),
            delta=1.2
        )
    
    with col3:
        st.metric(
            label="Avg Shares per Post",
            value=engagement_data.get('avgShares', 0),
            delta=0.8
        )
    
    with col4:
        st.metric(
            label="Engagement Rate",
            value=f"{engagement_data.get('engagementRate', 0)}%",
            delta=0.3
        )
    
    # Recent activity with enhanced display
    st.markdown("---")
    st.subheader("🕒 Recent Activity")
    
    if 'recentActivity' in stats_data and stats_data['recentActivity']:
        for i, activity in enumerate(stats_data['recentActivity'][:10]):
            timestamp = activity.get('timestamp', 'Unknown')
            action = activity.get('action', 'Unknown')
            details = activity.get('details', '')
            
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(timestamp)
            with col2:
                st.write(f"**{action}:** {details}")
            
            if i < len(stats_data['recentActivity']) - 1:
                st.markdown("---")
    else:
        # Show mock activity
        mock_activities = [
            {'timestamp': '2024-01-15 14:30:00', 'action': 'New Post Scraped', 'details': 'Post about Python programming from user @tech_enthusiast'},
            {'timestamp': '2024-01-15 14:25:00', 'action': 'Comment Added', 'details': 'Comment on machine learning post from @data_scientist'},
            {'timestamp': '2024-01-15 14:20:00', 'action': 'Scraping Session Started', 'details': 'Started scraping for keyword "artificial intelligence"'},
            {'timestamp': '2024-01-15 14:15:00', 'action': 'New User Detected', 'details': 'User @ai_researcher joined the conversation'},
            {'timestamp': '2024-01-15 14:10:00', 'action': 'Sentiment Analysis', 'details': 'Analyzed 50 new posts for sentiment'}
        ]
        
        for i, activity in enumerate(mock_activities):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.caption(activity['timestamp'])
            with col2:
                st.write(f"**{activity['action']}:** {activity['details']}")
            
            if i < len(mock_activities) - 1:
                st.markdown("---")

def get_mock_statistics():
    """Generate mock statistics for demonstration."""
    return {
        'totalPosts': 1250,
        'postsToday': 45,
        'totalComments': 3200,
        'commentsToday': 120,
        'activeUsers': 850,
        'newUsersToday': 25,
        'scrapingSessions': 15,
        'sessionsToday': 3,
        'sentimentDistribution': {
            'positive': 45,
            'neutral': 35,
            'negative': 20
        },
        'engagementMetrics': {
            'avgLikes': 45,
            'avgComments': 12,
            'avgShares': 8,
            'engagementRate': 3.2
        }
    }

def generate_mock_time_series_data(data_type):
    """Generate mock time series data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    np.random.seed(42)
    
    if data_type == 'posts':
        base_count = 40
        noise = np.random.normal(0, 5, len(dates))
        trend = np.linspace(0, 10, len(dates))
        counts = [max(0, int(base_count + noise[i] + trend[i])) for i in range(len(dates))]
    else:  # comments
        base_count = 100
        noise = np.random.normal(0, 15, len(dates))
        trend = np.linspace(0, 20, len(dates))
        counts = [max(0, int(base_count + noise[i] + trend[i])) for i in range(len(dates))]
    
    return [{'date': date.strftime('%Y-%m-%d'), 'count': count} for date, count in zip(dates, counts)]

def generate_mock_sentiment_data():
    """Generate mock sentiment time series data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    np.random.seed(42)
    
    data = []
    for date in dates:
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'positive': int(40 + np.random.normal(0, 5)),
            'neutral': int(35 + np.random.normal(0, 5)),
            'negative': int(20 + np.random.normal(0, 3))
        })
    
    return data