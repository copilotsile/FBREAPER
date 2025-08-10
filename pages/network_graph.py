import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

def render_network_graph(api_client):
    """Render the network graph visualization page."""
    
    st.header("🕸️ Network Graph Visualization")
    st.markdown("---")
    
    # Get posts for selection
    with st.spinner("Loading posts for analysis..."):
        posts_data = api_client.get_posts()
    
    if not posts_data:
        st.warning("⚠️ Unable to load posts. Please check your backend connection.")
        return
    
    # Convert to DataFrame
    if isinstance(posts_data, list):
        df = pd.DataFrame(posts_data)
    else:
        df = pd.DataFrame([posts_data])
    
    if df.empty:
        st.info("📭 No posts found for network analysis.")
        return
    
    # Post selection
    st.subheader("📊 Select Post for Network Analysis")
    
    # Create a selection interface
    if 'selected_post_id' not in st.session_state:
        st.session_state.selected_post_id = None
    
    # Display posts in a selectbox
    post_options = {f"{post.get('author', 'Unknown')} - {post.get('content', 'No content')[:50]}...": post.get('id') 
                   for post in posts_data if post.get('id')}
    
    if post_options:
        selected_post_display = st.selectbox(
            "Choose a post for network analysis:",
            options=list(post_options.keys()),
            index=0 if not st.session_state.selected_post_id else None
        )
        
        selected_post_id = post_options[selected_post_display]
        
        if st.button("🔍 Analyze Network"):
            st.session_state.selected_post_id = selected_post_id
    
    # Network analysis section
    if st.session_state.selected_post_id:
        st.markdown("---")
        st.subheader(f"🕸️ Network Analysis for Post: {st.session_state.selected_post_id}")
        
        with st.spinner("Performing network analysis..."):
            analysis_data = api_client.get_link_analysis(st.session_state.selected_post_id)
        
        if not analysis_data:
            st.warning("⚠️ Unable to perform network analysis for this post.")
            return
        
        # Display analysis results
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Nodes", analysis_data.get('nodes', []).__len__())
        
        with col2:
            st.metric("Edges", analysis_data.get('edges', []).__len__())
        
        # Network metrics
        if 'metrics' in analysis_data:
            metrics = analysis_data['metrics']
            st.subheader("📈 Network Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Density", f"{metrics.get('density', 0):.3f}")
            
            with col2:
                st.metric("Clustering", f"{metrics.get('clustering', 0):.3f}")
            
            with col3:
                st.metric("Diameter", metrics.get('diameter', 0))
            
            with col4:
                st.metric("Avg Degree", f"{metrics.get('avgDegree', 0):.2f}")
        
        # Create network visualization
        st.subheader("🕸️ Network Graph")
        
        # Create PyVis network
        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")
        
        # Add nodes
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
                'default': '#a29bfe'
            }
            
            net.add_node(
                node_id, 
                label=label,
                color=color_map.get(node_type, color_map['default']),
                size=20
            )
        
        # Add edges
        edges = analysis_data.get('edges', [])
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            edge_type = edge.get('type', 'default')
            
            # Color edges by type
            edge_color_map = {
                'mentions': '#e17055',
                'replies': '#00b894',
                'shares': '#fdcb6e',
                'default': '#636e72'
            }
            
            net.add_edge(
                source, 
                target,
                color=edge_color_map.get(edge_type, edge_color_map['default']),
                width=2
            )
        
        # Set physics options
        net.set_options("""
        var options = {
          "physics": {
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
        }
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
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
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
                              title='Network Graph',
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20,l=5,r=5,t=40),
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                          )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Community detection results
        if 'communities' in analysis_data:
            st.subheader("👥 Detected Communities")
            communities = analysis_data['communities']
            
            for i, community in enumerate(communities):
                with st.expander(f"Community {i+1} ({len(community)} members)"):
                    st.write(f"Members: {', '.join(community)}")
        
        # Shortest path analysis
        if 'shortestPaths' in analysis_data:
            st.subheader("🛤️ Shortest Paths")
            shortest_paths = analysis_data['shortestPaths']
            
            for path in shortest_paths:
                st.write(f"**Path:** {' → '.join(path['nodes'])} (Length: {path['length']})")
    
    else:
        st.info("👆 Please select a post above to perform network analysis.")