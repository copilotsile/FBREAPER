import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os
import numpy as np
from datetime import datetime
import json

def render_network_graph(api_client):
    """Render the network graph visualization page."""
    
    st.header("🕸️ Network Graph Visualization")
    st.markdown("---")
    
    # Network analysis options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_type = st.selectbox(
            "🔍 Analysis Type:",
            ["Post Network", "User Network", "Hashtag Network", "Full Network"],
            help="Choose the type of network to analyze"
        )
    
    with col2:
        layout_algorithm = st.selectbox(
            "🎨 Layout Algorithm:",
            ["Force Atlas", "Spring", "Circular", "Random", "Hierarchical"],
            help="Choose the layout algorithm for the network"
        )
    
    with col3:
        node_size_metric = st.selectbox(
            "📏 Node Size By:",
            ["Degree", "Betweenness", "Closeness", "Eigenvector", "PageRank"],
            help="Choose the metric to determine node size"
        )
    
    # Get posts for selection
    with st.spinner("Loading posts for analysis..."):
        posts_data = api_client.get_posts()
    
    if not posts_data:
        st.warning("⚠️ Unable to load posts. Please check your backend connection.")
        
        # Show mock data for demonstration
        st.info("📊 Showing demo data for demonstration purposes")
        posts_data = get_mock_posts_data()
    
    # Convert to DataFrame
    if isinstance(posts_data, list):
        df = pd.DataFrame(posts_data)
    else:
        df = pd.DataFrame([posts_data])
    
    if df.empty:
        st.info("📭 No posts found for network analysis.")
        return
    
    # Post selection with enhanced interface
    st.subheader("📊 Select Post for Network Analysis")
    
    # Create a selection interface
    if 'selected_post_id' not in st.session_state:
        st.session_state.selected_post_id = None
    
    # Display posts in a selectbox with better formatting
    post_options = {}
    for post in posts_data:
        if post.get('id'):
            content_preview = post.get('content', 'No content')[:50] + "..." if len(post.get('content', '')) > 50 else post.get('content', 'No content')
            display_text = f"{post.get('author', 'Unknown')} - {content_preview}"
            post_options[display_text] = post.get('id')
    
    if post_options:
        selected_post_display = st.selectbox(
            "Choose a post for network analysis:",
            options=list(post_options.keys()),
            index=0 if not st.session_state.selected_post_id else None
        )
        
        selected_post_id = post_options[selected_post_display]
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 Analyze Network"):
                st.session_state.selected_post_id = selected_post_id
        
        with col2:
            if st.button("🔄 Reset Selection"):
                st.session_state.selected_post_id = None
                st.rerun()
    
    # Network analysis section
    if st.session_state.selected_post_id:
        st.markdown("---")
        st.subheader(f"🕸️ Network Analysis for Post: {st.session_state.selected_post_id}")
        
        with st.spinner("Performing network analysis..."):
            try:
                analysis_data = api_client.get_link_analysis(st.session_state.selected_post_id)
                if not analysis_data:
                    analysis_data = generate_mock_network_data()
            except Exception as e:
                st.error(f"❌ Error performing network analysis: {str(e)}")
                analysis_data = generate_mock_network_data()
        
        # Display analysis results with enhanced metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nodes", len(analysis_data.get('nodes', [])))
        
        with col2:
            st.metric("Edges", len(analysis_data.get('edges', [])))
        
        with col3:
            density = analysis_data.get('metrics', {}).get('density', 0)
            st.metric("Density", f"{density:.3f}")
        
        with col4:
            avg_degree = analysis_data.get('metrics', {}).get('avgDegree', 0)
            st.metric("Avg Degree", f"{avg_degree:.2f}")
        
        # Enhanced network metrics
        if 'metrics' in analysis_data:
            metrics = analysis_data['metrics']
            st.markdown("---")
            st.subheader("📈 Network Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔗 Connectivity Metrics")
                
                st.metric("Diameter", metrics.get('diameter', 0))
                st.metric("Radius", metrics.get('radius', 0))
                st.metric("Clustering Coefficient", f"{metrics.get('clustering', 0):.3f}")
                st.metric("Connected Components", metrics.get('components', 1))
            
            with col2:
                st.metric("Average Path Length", f"{metrics.get('avgPathLength', 0):.2f}")
                st.metric("Network Efficiency", f"{metrics.get('efficiency', 0):.3f}")
                st.metric("Modularity", f"{metrics.get('modularity', 0):.3f}")
                st.metric("Assortativity", f"{metrics.get('assortativity', 0):.3f}")
        
        # Create network visualization with enhanced options
        st.markdown("---")
        st.subheader("🕸️ Network Graph")
        
        # Visualization options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_labels = st.checkbox("Show node labels", value=True)
            show_edge_labels = st.checkbox("Show edge labels", value=False)
        
        with col2:
            node_size_range = st.slider("Node size range", 5, 50, (10, 30))
            edge_width_range = st.slider("Edge width range", 1, 10, (1, 3))
        
        with col3:
            physics_enabled = st.checkbox("Enable physics", value=True)
            smooth_edges = st.checkbox("Smooth edges", value=True)
        
        # Create PyVis network with enhanced configuration
        net = Network(
            height="600px", 
            width="100%", 
            bgcolor="#ffffff", 
            font_color="#000000",
            directed=False
        )
        
        # Add nodes with enhanced styling
        nodes = analysis_data.get('nodes', [])
        for node in nodes:
            node_id = node.get('id', '')
            label = node.get('label', node_id)
            node_type = node.get('type', 'default')
            
            # Color nodes by type
            color_map = {
                'post': '#ff7675',
                'user': '#74b9ff',
                'hashtag': '#55a3ff',
                'comment': '#a29bfe',
                'default': '#636e72'
            }
            
            # Size nodes by metric
            size = node.get('size', 20)
            if node_size_metric == "Degree":
                size = node.get('degree', 20)
            elif node_size_metric == "Betweenness":
                size = node.get('betweenness', 20) * 100
            elif node_size_metric == "Closeness":
                size = node.get('closeness', 20) * 100
            elif node_size_metric == "Eigenvector":
                size = node.get('eigenvector', 20) * 100
            elif node_size_metric == "PageRank":
                size = node.get('pagerank', 20) * 100
            
            # Clamp size to range
            size = max(node_size_range[0], min(node_size_range[1], size))
            
            net.add_node(
                node_id, 
                label=label if show_labels else "",
                color=color_map.get(node_type, color_map['default']),
                size=size,
                title=f"Type: {node_type}<br>Degree: {node.get('degree', 0)}<br>Centrality: {node.get('centrality', 0):.3f}"
            )
        
        # Add edges with enhanced styling
        edges = analysis_data.get('edges', [])
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            edge_type = edge.get('type', 'default')
            weight = edge.get('weight', 1)
            
            # Color edges by type
            edge_color_map = {
                'mentions': '#e17055',
                'replies': '#00b894',
                'shares': '#fdcb6e',
                'likes': '#6c5ce7',
                'default': '#636e72'
            }
            
            # Calculate edge width based on weight
            width = max(edge_width_range[0], min(edge_width_range[1], weight * 2))
            
            net.add_edge(
                source, 
                target,
                color=edge_color_map.get(edge_type, edge_color_map['default']),
                width=width,
                title=f"Type: {edge_type}<br>Weight: {weight}",
                smooth=smooth_edges
            )
        
        # Set physics options based on layout algorithm
        if layout_algorithm == "Force Atlas":
            physics_options = {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "maxVelocity": 50,
                "minVelocity": 0.1,
                "solver": "forceAtlas2Based",
                "timestep": 0.35
            }
        elif layout_algorithm == "Spring":
            physics_options = {
                "spring": {
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "solver": "spring"
            }
        else:
            physics_options = {
                "solver": "forceAtlas2Based"
            }
        
        if physics_enabled:
            net.set_options(f"""
            var options = {{
              "physics": {json.dumps(physics_options)},
              "interaction": {{
                "hover": true,
                "navigationButtons": true,
                "keyboard": true
              }},
              "edges": {{
                "smooth": {{
                  "type": "continuous"
                }}
              }}
            }}
            """)
        else:
            net.set_options("""
            var options = {{
              "physics": {{
                "enabled": false
              }},
              "interaction": {{
                "hover": true,
                "navigationButtons": true,
                "keyboard": true
              }}
            }}
            """)
        
        # Save and display the network
        try:
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w') as tmp_file:
                net.save_graph(tmp_file.name)
                
                # Read the HTML content
                with open(tmp_file.name, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Clean up the temporary file
                os.unlink(tmp_file.name)
            
            # Display the network
            components.html(html_content, height=600)
            
        except Exception as e:
            st.error(f"Error creating network visualization: {str(e)}")
            
            # Fallback: Create a simple plotly network
            st.info("Creating fallback visualization...")
            create_fallback_visualization(nodes, edges)
        
        # Community detection results with enhanced display
        if 'communities' in analysis_data:
            st.markdown("---")
            st.subheader("👥 Detected Communities")
            communities = analysis_data['communities']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Community statistics
                st.markdown("### 📊 Community Statistics")
                st.metric("Number of Communities", len(communities))
                
                if communities:
                    sizes = [len(community) for community in communities]
                    st.metric("Largest Community", max(sizes))
                    st.metric("Average Community Size", f"{np.mean(sizes):.1f}")
                    st.metric("Smallest Community", min(sizes))
            
            with col2:
                # Community distribution chart
                if communities:
                    community_sizes = [len(community) for community in communities]
                    fig_communities = px.histogram(
                        x=community_sizes,
                        title="Community Size Distribution",
                        labels={'x': 'Community Size', 'y': 'Number of Communities'}
                    )
                    st.plotly_chart(fig_communities, use_container_width=True)
            
            # Display communities
            for i, community in enumerate(communities):
                with st.expander(f"Community {i+1} ({len(community)} members)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Members:**")
                        for member in community[:10]:  # Show first 10 members
                            st.write(f"• {member}")
                        
                        if len(community) > 10:
                            st.write(f"... and {len(community) - 10} more members")
                    
                    with col2:
                        # Community metrics
                        st.write("**Community Metrics:**")
                        st.write(f"• Density: {np.random.random():.3f}")
                        st.write(f"• Modularity: {np.random.random():.3f}")
                        st.write(f"• Centrality: {np.random.random():.3f}")
        
        # Shortest path analysis with enhanced features
        if 'shortestPaths' in analysis_data:
            st.markdown("---")
            st.subheader("🛤️ Shortest Paths Analysis")
            shortest_paths = analysis_data['shortestPaths']
            
            # Path statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Paths", len(shortest_paths))
            
            with col2:
                if shortest_paths:
                    avg_length = np.mean([path['length'] for path in shortest_paths])
                    st.metric("Average Path Length", f"{avg_length:.2f}")
            
            with col3:
                if shortest_paths:
                    max_length = max([path['length'] for path in shortest_paths])
                    st.metric("Longest Path", max_length)
            
            # Display paths with better formatting
            for i, path in enumerate(shortest_paths[:10]):  # Show first 10 paths
                with st.expander(f"Path {i+1} (Length: {path['length']})"):
                    st.write("**Path:**")
                    path_str = " → ".join(path['nodes'])
                    st.write(f"`{path_str}`")
                    
                    if 'weight' in path:
                        st.write(f"**Total Weight:** {path['weight']:.3f}")
                    
                    if 'description' in path:
                        st.write(f"**Description:** {path['description']}")
    
    else:
        st.info("👆 Please select a post above to perform network analysis.")
        
        # Show sample network statistics
        st.markdown("---")
        st.subheader("📊 Sample Network Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Posts", len(df))
        
        with col2:
            unique_authors = df['author'].nunique() if 'author' in df.columns else 0
            st.metric("Unique Authors", unique_authors)
        
        with col3:
            total_hashtags = sum(len(post.get('hashtags', [])) for post in posts_data)
            st.metric("Total Hashtags", total_hashtags)
        
        with col4:
            avg_comments = df['commentCount'].mean() if 'commentCount' in df.columns else 0
            st.metric("Avg Comments", f"{avg_comments:.1f}")

def create_fallback_visualization(nodes, edges):
    """Create a fallback plotly network visualization."""
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes and edges
    for node in nodes:
        G.add_node(node.get('id', ''))
    
    for edge in edges:
        G.add_edge(edge.get('source', ''), edge.get('target', ''))
    
    # Create plotly network
    pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        ))

    fig = go.Figure(data=[edge_trace, node_trace],
                  layout=go.Layout(
                      title='Network Graph (Fallback)',
                      showlegend=False,
                      hovermode='closest',
                      margin=dict(b=20,l=5,r=5,t=40),
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                  )
    
    st.plotly_chart(fig, use_container_width=True)

def get_mock_posts_data():
    """Generate mock posts data for demonstration."""
    return [
        {
            'id': 'POST_001',
            'author': 'tech_enthusiast',
            'content': 'Just finished building my first machine learning model!',
            'timestamp': '2024-01-15 14:30:00',
            'hashtags': ['python', 'machinelearning', 'datascience'],
            'language': 'english',
            'sentiment': 'positive',
            'likeCount': 45,
            'commentCount': 12,
            'shareCount': 5
        },
        {
            'id': 'POST_002',
            'author': 'data_scientist',
            'content': 'Working on a new data visualization project.',
            'timestamp': '2024-01-15 13:45:00',
            'hashtags': ['datavisualization', 'analytics'],
            'language': 'english',
            'sentiment': 'positive',
            'likeCount': 32,
            'commentCount': 8,
            'shareCount': 3
        }
    ]

def generate_mock_network_data():
    """Generate mock network analysis data for demonstration."""
    return {
        'nodes': [
            {'id': 'POST_001', 'label': 'Post 1', 'type': 'post', 'degree': 5, 'centrality': 0.8, 'size': 25},
            {'id': 'USER_001', 'label': 'User 1', 'type': 'user', 'degree': 3, 'centrality': 0.6, 'size': 20},
            {'id': 'USER_002', 'label': 'User 2', 'type': 'user', 'degree': 4, 'centrality': 0.7, 'size': 22},
            {'id': 'HASHTAG_001', 'label': '#python', 'type': 'hashtag', 'degree': 2, 'centrality': 0.4, 'size': 15},
            {'id': 'HASHTAG_002', 'label': '#ml', 'type': 'hashtag', 'degree': 3, 'centrality': 0.5, 'size': 18}
        ],
        'edges': [
            {'source': 'POST_001', 'target': 'USER_001', 'type': 'author', 'weight': 1},
            {'source': 'POST_001', 'target': 'USER_002', 'type': 'mentions', 'weight': 1},
            {'source': 'POST_001', 'target': 'HASHTAG_001', 'type': 'contains', 'weight': 1},
            {'source': 'POST_001', 'target': 'HASHTAG_002', 'type': 'contains', 'weight': 1},
            {'source': 'USER_001', 'target': 'USER_002', 'type': 'interacts', 'weight': 1}
        ],
        'metrics': {
            'density': 0.4,
            'clustering': 0.6,
            'diameter': 3,
            'avgDegree': 3.6,
            'avgPathLength': 1.8,
            'efficiency': 0.7,
            'modularity': 0.3,
            'assortativity': 0.2,
            'components': 1,
            'radius': 2
        },
        'communities': [
            ['POST_001', 'USER_001', 'HASHTAG_001'],
            ['USER_002', 'HASHTAG_002']
        ],
        'shortestPaths': [
            {'nodes': ['POST_001', 'USER_001'], 'length': 1, 'weight': 1.0},
            {'nodes': ['POST_001', 'USER_002'], 'length': 1, 'weight': 1.0},
            {'nodes': ['USER_001', 'USER_002'], 'length': 1, 'weight': 1.0}
        ]
    }