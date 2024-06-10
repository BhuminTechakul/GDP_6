# -*- coding: utf-8 -*-
"""
Created on Mon May 27 18:29:19 2024

@author: Win 10 Home
"""

import folium
import pandas as pd
from branca.colormap import LinearColormap

# Load the data from the Excel file
df = pd.read_excel('Location.xlsx')

# Convert 'Acai' and 'Brazil nut' columns to numeric type
df['Acai'] = pd.to_numeric(df['Acai'], errors='coerce')
df['Brazil nut'] = pd.to_numeric(df['Brazil nut'], errors='coerce')

# Create a colormap for Acai values
acai_colormap = LinearColormap(['green', 'yellow', 'red'], vmin=df['Acai'].min(), vmax=df['Acai'].max())

# Create a map centered around Brazil for Acai
m_acai = folium.Map(location=[-14.235, -51.9253], zoom_start=4)

# Add markers for each city with Acai values
for i, row in df.iterrows():
    # If latitude and longitude are available, and Acai value is not null, add a marker
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']) and pd.notnull(row['Acai']):
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=10,
            popup=f"Town: {row['City']}<br>Acai: {row['Acai']}",
            fill=True,
            color=acai_colormap(row['Acai']),
            fill_opacity=0.7
        ).add_to(m_acai)

# Add the colormap to the map
acai_colormap.add_to(m_acai)

# Save the map as HTML file for Acai
m_acai.save('map_acai.html')