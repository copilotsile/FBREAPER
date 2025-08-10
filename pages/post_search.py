import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def render_post_search(api_client):
    """Render the post search page."""
    
    st.header("📝 Post Search & Browse")
    st.markdown("---")
    
    # Enhanced search and filter options
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = st.text_input(
            "🔍 Search posts:",
            placeholder="Enter keywords to search...",
            help="Search in post content, author, or hashtags"
        )
    
    with col2:
        sort_by = st.selectbox(
            "📊 Sort by:",
            ["Newest First", "Oldest First", "Author", "Most Comments", "Most Likes", "Sentiment"],
            help="Choose how to sort the posts"
        )
    
    with col3:
        posts_per_page = st.selectbox(
            "📄 Posts per page:",
            [10, 20, 50, 100],
            index=1,
            help="Number of posts to display per page"
        )
    
    with col4:
        date_range = st.selectbox(
            "📅 Date range:",
            ["All Time", "Today", "Last 7 days", "Last 30 days", "Last 90 days"],
            help="Filter posts by date range"
        )
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentiment_filter = st.selectbox(
                "😊 Sentiment:",
                ["All", "Positive", "Neutral", "Negative"],
                help="Filter by sentiment analysis"
            )
            
            language_filter = st.selectbox(
                "🌐 Language:",
                ["All", "English", "Spanish", "French", "German", "Other"],
                help="Filter by post language"
            )
        
        with col2:
            min_likes = st.number_input(
                "👍 Min likes:",
                min_value=0,
                value=0,
                help="Minimum number of likes"
            )
            
            min_comments = st.number_input(
                "💬 Min comments:",
                min_value=0,
                value=0,
                help="Minimum number of comments"
            )
        
        with col3:
            author_filter = st.text_input(
                "👤 Author:",
                placeholder="Filter by specific author...",
                help="Filter posts by author name"
            )
            
            hashtag_filter = st.text_input(
                "🏷️ Hashtag:",
                placeholder="Filter by hashtag...",
                help="Filter posts containing specific hashtag"
            )
    
    # Load posts with spinner
    with st.spinner("Loading posts..."):
        posts_data = api_client.get_posts()
    
    if not posts_data:
        st.warning("⚠️ Unable to load posts. Please check your backend connection.")
        
        # Show mock data for demonstration
        st.info("📊 Showing demo data for demonstration purposes")
        posts_data = get_mock_posts_data()
    
    # Convert to DataFrame for easier manipulation
    if isinstance(posts_data, list):
        df = pd.DataFrame(posts_data)
    else:
        df = pd.DataFrame([posts_data])
    
    if df.empty:
        st.info("📭 No posts found in the database.")
        return
    
    # Apply search filter
    if search_term:
        mask = (
            df['content'].str.contains(search_term, case=False, na=False) |
            df['author'].str.contains(search_term, case=False, na=False) |
            df['hashtags'].astype(str).str.contains(search_term, case=False, na=False)
        )
        df = df[mask]
    
    # Apply sentiment filter
    if sentiment_filter != "All":
        df = df[df['sentiment'] == sentiment_filter.lower()]
    
    # Apply language filter
    if language_filter != "All":
        df = df[df['language'] == language_filter.lower()]
    
    # Apply author filter
    if author_filter:
        df = df[df['author'].str.contains(author_filter, case=False, na=False)]
    
    # Apply hashtag filter
    if hashtag_filter:
        df = df[df['hashtags'].astype(str).str.contains(hashtag_filter, case=False, na=False)]
    
    # Apply date range filter
    if date_range != "All Time":
        now = datetime.now()
        if date_range == "Today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == "Last 7 days":
            start_date = now - timedelta(days=7)
        elif date_range == "Last 30 days":
            start_date = now - timedelta(days=30)
        elif date_range == "Last 90 days":
            start_date = now - timedelta(days=90)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['timestamp'] >= start_date]
    
    # Apply sorting
    if sort_by == "Newest First":
        df = df.sort_values('timestamp', ascending=False)
    elif sort_by == "Oldest First":
        df = df.sort_values('timestamp', ascending=True)
    elif sort_by == "Author":
        df = df.sort_values('author')
    elif sort_by == "Most Comments":
        df = df.sort_values('commentCount', ascending=False)
    elif sort_by == "Most Likes":
        df = df.sort_values('likeCount', ascending=False)
    elif sort_by == "Sentiment":
        sentiment_order = {'positive': 3, 'neutral': 2, 'negative': 1}
        df['sentiment_order'] = df['sentiment'].map(sentiment_order)
        df = df.sort_values('sentiment_order', ascending=False)
        df = df.drop('sentiment_order', axis=1)
    
    # Statistics summary
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", len(df))
    
    with col2:
        avg_sentiment = df['sentiment'].value_counts().index[0] if not df.empty else "N/A"
        st.metric("Most Common Sentiment", avg_sentiment.title())
    
    with col3:
        top_author = df['author'].value_counts().index[0] if not df.empty else "N/A"
        st.metric("Top Author", top_author)
    
    with col4:
        total_likes = df['likeCount'].sum() if 'likeCount' in df.columns else 0
        st.metric("Total Likes", total_likes)
    
    # Pagination
    total_posts = len(df)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page
    
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        if st.button("⬅️ Previous") and st.session_state.get('current_page', 0) > 0:
            st.session_state.current_page -= 1
    
    with col2:
        st.write(f"Page {st.session_state.get('current_page', 0) + 1} of {total_pages} ({total_posts} total posts)")
    
    with col3:
        if st.button("Next ➡️") and st.session_state.get('current_page', 0) < total_pages - 1:
            st.session_state.current_page += 1
    
    with col4:
        if st.button("📊 Export"):
            export_data(df)
    
    # Display posts for current page
    current_page = st.session_state.get('current_page', 0)
    start_idx = current_page * posts_per_page
    end_idx = min(start_idx + posts_per_page, total_posts)
    
    page_posts = df.iloc[start_idx:end_idx]
    
    st.markdown("---")
    
    # Display posts with enhanced styling
    for idx, post in page_posts.iterrows():
        with st.expander(f"📄 {post.get('author', 'Unknown')} - {post.get('timestamp', 'Unknown')}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Post content
                st.write(f"**Author:** {post.get('author', 'Unknown')}")
                st.write(f"**Content:** {post.get('content', 'No content')}")
                
                # Hashtags
                if post.get('hashtags'):
                    hashtags = post.get('hashtags', [])
                    if isinstance(hashtags, str):
                        hashtags = [hashtags]
                    st.write(f"**Hashtags:** {', '.join(hashtags)}")
                
                # Language and sentiment
                col_a, col_b = st.columns(2)
                with col_a:
                    if post.get('language'):
                        st.write(f"**Language:** {post.get('language', 'Unknown')}")
                
                with col_b:
                    if post.get('sentiment'):
                        sentiment = post.get('sentiment', 'neutral')
                        if sentiment == 'positive':
                            st.success(f"😊 Sentiment: {sentiment}")
                        elif sentiment == 'negative':
                            st.error(f"😞 Sentiment: {sentiment}")
                        else:
                            st.info(f"😐 Sentiment: {sentiment}")
                
                # Engagement metrics
                col_c, col_d, col_e = st.columns(3)
                with col_c:
                    st.metric("👍 Likes", post.get('likeCount', 0))
                with col_d:
                    st.metric("💬 Comments", post.get('commentCount', 0))
                with col_e:
                    st.metric("🔄 Shares", post.get('shareCount', 0))
            
            with col2:
                st.write(f"**ID:** {post.get('id', 'N/A')}")
                st.write(f"**Type:** {post.get('postType', 'Unknown')}")
                st.write(f"**Platform:** {post.get('platform', 'Facebook')}")
                
                # Button to view comments
                if st.button(f"💬 View Comments", key=f"comments_{post.get('id')}"):
                    st.session_state.selected_post_id = post.get('id')
                    st.session_state.show_comments = True
    
    # Comments section with enhanced display
    if st.session_state.get('show_comments', False) and st.session_state.get('selected_post_id'):
        st.markdown("---")
        st.subheader(f"💬 Comments for Post {st.session_state.selected_post_id}")
        
        with st.spinner("Loading comments..."):
            comments_data = api_client.get_post_comments(st.session_state.selected_post_id)
        
        if comments_data:
            # Filter comments for the selected post
            if isinstance(comments_data, list):
                post_comments = [c for c in comments_data if c.get('postId') == st.session_state.selected_post_id]
            else:
                post_comments = []
            
            if post_comments:
                # Comments statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Comments", len(post_comments))
                with col2:
                    positive_comments = len([c for c in post_comments if c.get('sentiment') == 'positive'])
                    st.metric("Positive", positive_comments)
                with col3:
                    negative_comments = len([c for c in post_comments if c.get('sentiment') == 'negative'])
                    st.metric("Negative", negative_comments)
                
                # Display comments
                for comment in post_comments:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**{comment.get('author', 'Unknown')}:** {comment.get('text', 'No text')}")
                            
                            # Comment metadata
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.caption(f"📅 {comment.get('timestamp', 'Unknown')}")
                            with col_b:
                                if comment.get('sentiment'):
                                    sentiment = comment.get('sentiment', 'neutral')
                                    if sentiment == 'positive':
                                        st.success("😊 Positive")
                                    elif sentiment == 'negative':
                                        st.error("😞 Negative")
                                    else:
                                        st.info("😐 Neutral")
                        
                        with col2:
                            st.caption(f"👍 {comment.get('likes', 0)}")
                            st.caption(f"💬 {comment.get('replies', 0)}")
            else:
                st.info("No comments found for this post.")
        else:
            st.warning("Unable to load comments. Please check your connection.")
        
        if st.button("❌ Close Comments"):
            st.session_state.show_comments = False
            st.session_state.selected_post_id = None
            st.rerun()
    
    # Data visualization section
    if not df.empty:
        st.markdown("---")
        st.subheader("📊 Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                fig_sentiment = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Sentiment Distribution",
                    color_discrete_map={
                        'positive': '#28a745',
                        'neutral': '#ffc107',
                        'negative': '#dc3545'
                    }
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            # Posts over time
            if 'timestamp' in df.columns:
                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                daily_posts = df['date'].value_counts().sort_index()
                
                fig_timeline = px.line(
                    x=daily_posts.index,
                    y=daily_posts.values,
                    title="Posts Over Time",
                    labels={'x': 'Date', 'y': 'Number of Posts'}
                )
                st.plotly_chart(fig_timeline, use_container_width=True)

def get_mock_posts_data():
    """Generate mock posts data for demonstration."""
    return [
        {
            'id': 'POST_001',
            'author': 'tech_enthusiast',
            'content': 'Just finished building my first machine learning model! The results are amazing. #python #machinelearning #datascience',
            'timestamp': '2024-01-15 14:30:00',
            'hashtags': ['python', 'machinelearning', 'datascience'],
            'language': 'english',
            'sentiment': 'positive',
            'likeCount': 45,
            'commentCount': 12,
            'shareCount': 5,
            'postType': 'text',
            'platform': 'Facebook'
        },
        {
            'id': 'POST_002',
            'author': 'data_scientist',
            'content': 'Working on a new data visualization project. The insights we\'re discovering are incredible! #datavisualization #analytics',
            'timestamp': '2024-01-15 13:45:00',
            'hashtags': ['datavisualization', 'analytics'],
            'language': 'english',
            'sentiment': 'positive',
            'likeCount': 32,
            'commentCount': 8,
            'shareCount': 3,
            'postType': 'text',
            'platform': 'Facebook'
        },
        {
            'id': 'POST_003',
            'author': 'programmer_guru',
            'content': 'Having issues with my code today. Nothing seems to work as expected. #programming #frustrated',
            'timestamp': '2024-01-15 12:20:00',
            'hashtags': ['programming', 'frustrated'],
            'language': 'english',
            'sentiment': 'negative',
            'likeCount': 15,
            'commentCount': 25,
            'shareCount': 2,
            'postType': 'text',
            'platform': 'Facebook'
        }
    ]

def export_data(df):
    """Export data to CSV or JSON."""
    if df.empty:
        st.warning("No data to export.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"posts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📄 Export to JSON"):
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"posts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )