import streamlit as st
import pandas as pd
from datetime import datetime

def render_post_search(api_client):
    """Render the post search page."""
    
    st.header("📝 Post Search & Browse")
    st.markdown("---")
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input(
            "Search posts:",
            placeholder="Enter keywords to search...",
            help="Search in post content, author, or hashtags"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Newest First", "Oldest First", "Author", "Most Comments"],
            help="Choose how to sort the posts"
        )
    
    with col3:
        posts_per_page = st.selectbox(
            "Posts per page:",
            [10, 20, 50, 100],
            index=1,
            help="Number of posts to display per page"
        )
    
    # Load posts with spinner
    with st.spinner("Loading posts..."):
        posts_data = api_client.get_posts()
    
    if not posts_data:
        st.warning("⚠️ Unable to load posts. Please check your backend connection.")
        return
    
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
    
    # Apply sorting
    if sort_by == "Newest First":
        df = df.sort_values('timestamp', ascending=False)
    elif sort_by == "Oldest First":
        df = df.sort_values('timestamp', ascending=True)
    elif sort_by == "Author":
        df = df.sort_values('author')
    
    # Pagination
    total_posts = len(df)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous") and st.session_state.get('current_page', 0) > 0:
            st.session_state.current_page -= 1
    
    with col2:
        st.write(f"Page {st.session_state.get('current_page', 0) + 1} of {total_pages} ({total_posts} total posts)")
    
    with col3:
        if st.button("Next ➡️") and st.session_state.get('current_page', 0) < total_pages - 1:
            st.session_state.current_page += 1
    
    # Display posts for current page
    current_page = st.session_state.get('current_page', 0)
    start_idx = current_page * posts_per_page
    end_idx = min(start_idx + posts_per_page, total_posts)
    
    page_posts = df.iloc[start_idx:end_idx]
    
    st.markdown("---")
    
    # Display posts
    for idx, post in page_posts.iterrows():
        with st.expander(f"📄 {post.get('author', 'Unknown')} - {post.get('timestamp', 'Unknown')}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Author:** {post.get('author', 'Unknown')}")
                st.write(f"**Content:** {post.get('content', 'No content')}")
                
                if post.get('hashtags'):
                    hashtags = post.get('hashtags', [])
                    if isinstance(hashtags, str):
                        hashtags = [hashtags]
                    st.write(f"**Hashtags:** {', '.join(hashtags)}")
                
                if post.get('language'):
                    st.write(f"**Language:** {post.get('language', 'Unknown')}")
                
                if post.get('sentiment'):
                    sentiment = post.get('sentiment', 'neutral')
                    if sentiment == 'positive':
                        st.success(f"😊 Sentiment: {sentiment}")
                    elif sentiment == 'negative':
                        st.error(f"😞 Sentiment: {sentiment}")
                    else:
                        st.info(f"😐 Sentiment: {sentiment}")
            
            with col2:
                st.write(f"**ID:** {post.get('id', 'N/A')}")
                st.write(f"**Type:** {post.get('postType', 'Unknown')}")
                
                # Button to view comments
                if st.button(f"💬 Comments", key=f"comments_{post.get('id')}"):
                    st.session_state.selected_post_id = post.get('id')
                    st.session_state.show_comments = True
    
    # Comments section
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
                for comment in post_comments:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**{comment.get('author', 'Unknown')}:** {comment.get('text', 'No text')}")
                        
                        with col2:
                            st.caption(f"{comment.get('timestamp', 'Unknown')}")
                            
                            if comment.get('sentiment'):
                                sentiment = comment.get('sentiment', 'neutral')
                                if sentiment == 'positive':
                                    st.success("😊")
                                elif sentiment == 'negative':
                                    st.error("😞")
                                else:
                                    st.info("😐")
            else:
                st.info("No comments found for this post.")
        
        if st.button("❌ Close Comments"):
            st.session_state.show_comments = False
            st.session_state.selected_post_id = None
            st.rerun()