import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import matplotlib.pyplot as plt
import io
from PIL import Image

# Initialize session state
if 'nodes' not in st.session_state:
    st.session_state.nodes = [{'x': 0, 'y': 0, 'children_count': 0}]
if 'edges' not in st.session_state:
    st.session_state.edges = []

def add_child(parent_node):
    new_x = parent_node['x'] + parent_node['children_count']
    new_y = parent_node['y'] - 1
    st.session_state.nodes.append({
        'x': new_x, 
        'y': new_y, 
        'children_count': 0
    })
    st.session_state.edges.append({
        'x1': parent_node['x'],
        'y1': parent_node['y'],
        'x2': new_x,
        'y2': new_y
    })
    parent_node['children_count'] += 1

def create_figure():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect('equal')
    ax.invert_yaxis()  # CORRECTED METHOD NAME
    ax.grid(True)
    
    # Draw edges
    for edge in st.session_state.edges:
        ax.plot(
            [edge['x1'], edge['x2']],
            [edge['y1'], edge['y2']],
            'gray',
            zorder=1
        )
    
    # Draw nodes
    for node in st.session_state.nodes:
        ax.plot(
            node['x'], 
            node['y'], 
            'o',
            markersize=30,
            color='lightblue',
            zorder=2
        )
        ax.text(
            node['x'], 
            node['y'], 
            f"({node['x']},{node['y']})",
            ha='center',
            va='center',
            fontsize=8,
            zorder=3
        )
    
    # Set dynamic axis limits
    all_x = [n['x'] for n in st.session_state.nodes] + [0]
    all_y = [n['y'] for n in st.session_state.nodes] + [0]
    pad = 1
    ax.set_xlim(min(all_x)-pad, max(all_x)+pad)
    ax.set_ylim(max(all_y)+pad, min(all_y)-pad)
    
    return fig

# Create figure and convert to PIL Image
fig = create_figure()
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=100, bbox_inches='tight')
plt.close(fig)  # Prevent memory leaks
buf.seek(0)
img = Image.open(buf)

# Display image and get coordinates
click_coords = streamlit_image_coordinates(img, key="tree")

if click_coords:
    # Convert image coordinates to data coordinates
    ax = fig.gca()
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    img_width, img_height = img.size
    
    x_data = x_min + (click_coords['x'] / img_width) * (x_max - x_min)
    y_data = y_min + (click_coords['y'] / img_height) * (y_max - y_min)
    
    # Find closest node within tolerance
    tolerance = 0.5
    closest_node = None
    min_dist = float('inf')
    
    for node in st.session_state.nodes:
        dx = node['x'] - x_data
        dy = node['y'] - y_data
        dist = dx**2 + dy**2
        if dist < min_dist and dist < tolerance**2:
            min_dist = dist
            closest_node = node
    
    if closest_node:
        add_child(closest_node)
        st.rerun()

st.write("Click on any node to add its child. Nodes follow grid-based positioning:")
st.markdown("- First child appears below parent (y-1)")
st.markdown("- Subsequent children appear to the right (x+1)")
st.markdown("Refresh page to reset tree")