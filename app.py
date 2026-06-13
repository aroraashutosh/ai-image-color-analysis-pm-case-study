import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px

# 1. Define the 11 Color Categories (Standard RGB values)
COLOR_MAP = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Green": (0, 128, 0),
    "Yellow": (255, 255, 0),
    "Blue": (0, 0, 255),
    "Brown": (165, 42, 42),
    "Purple": (128, 0, 128),
    "Pink": (255, 192, 203),
    "Orange": (255, 165, 0),
    "Gray": (128, 128, 128)
}

def get_closest_color(pixel):
    """Mathematical Algorithm: Euclidean Distance to find the nearest color category."""
    distances = {}
    for color_name, rgb_val in COLOR_MAP.items():
        # Calculation: sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
        dist = np.sqrt(sum((np.array(pixel) - np.array(rgb_val))**2))
        distances[color_name] = dist
    return min(distances, key=distances.get)

# --- UI Layout ---
st.set_page_config(page_title="Alemeno Assignment", layout="centered")
st.title("🖼️ Image Color Analyzer")
st.info("This tool maps image pixels to 11 standard color categories.")

uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image
    img = Image.open(uploaded_file).convert('RGB')
    
    # PERFORMANCE OPTIMIZATION: 
    # We resize to a small sample size so the loop doesn't take minutes.
    # This is a standard 'MVP' (Minimum Viable Product) approach.
    img_small = img.copy()
    img_small.thumbnail((150, 150)) 
    
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    with st.spinner('Analyzing pixel data...'):
        pixels = list(img_small.getdata())
        counts = {name: 0 for name in COLOR_MAP.keys()}
        
        # Map each pixel to the closest category
        for pixel in pixels:
            closest = get_closest_color(pixel)
            counts[closest] += 1
            
        # Data Preparation
        total_pixels = len(pixels)
        data = []
        for color, count in counts.items():
            if count > 0:
                percentage = round((count / total_pixels) * 100, 2)
                data.append({"Color": color, "Percentage": percentage})
        
        df = pd.DataFrame(data).sort_values(by="Percentage", ascending=False)

    # Display Visuals
    st.subheader("Results")
    
    # Pie Chart
    fig_pie = px.pie(df, values='Percentage', names='Color', 
                     color='Color',
                     title="Color Distribution (%)",
                     color_discrete_map={k: f'rgb{v}' for k, v in COLOR_MAP.items()})
    st.plotly_chart(fig_pie)
    
    # Data Table
    st.table(df)