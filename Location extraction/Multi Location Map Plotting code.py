# -*- coding: utf-8 -*-
"""
Created on Mon May 27 18:29:19 2024

@author: Win 10 Home
"""

import folium
import pandas as pd
from branca.colormap import LinearColormap

# Load the data from CSV
data = pd.read_excel('LocationForecast.xlsx')

# Years to include (excluding 2017, 2018, 2019)
years = ["Year "+ str(i)  for i in range(2000, 2051) if i not in [2017, 2018, 2019]]
# Define the minimum and maximum values for the color scale
min_value = 1
max_value = 1200

# Define the number of colors in the colormap
num_colors = 10

# Create a logarithmic colormap
colors = ['lightgreen','yellow','orange', 'red']  # Define your colors here
acai_colormap = LinearColormap(colors=colors, vmin=min_value, vmax=max_value)
colors2 = ['red','darkred','black']
acai_colormap2 = LinearColormap(colors=colors2, vmin=1200, vmax=63000)

# Iterate over each year
for year in years:
    # Create a map
    m_acai = folium.Map(location=[-10, -58.9253], zoom_start=5)
    # Add markers to the map
    for _, row in data.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            acai_value = row[year]
            if pd.notnull(acai_value) and acai_value > 0 and acai_value<1200:
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=5,
                    popup=f"Town: {row['City']}<br>Acai: {acai_value}",
                    fill=True,
                    fill_color=acai_colormap(acai_value),
                    fill_opacity=0.8,
                    color='black',  # Outline color
                    weight=1 # Outline weight
                ).add_to(m_acai)
            elif pd.notnull(acai_value) and acai_value > 0 and acai_value>1200:
                 folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=5,
                    popup=f"Town: {row['City']}<br>Acai: {acai_value}",
                    fill=True,
                    fill_color=acai_colormap2(acai_value),
                    fill_opacity=0.8,
                    color='black',  # Outline color
                    weight=1 # Outline weight
                ).add_to(m_acai)
    acai_colormap.add_to(m_acai)
    acai_colormap2.add_to(m_acai)
    
    
    # Add a title
    title_html = f'''
        <h3 align="center" style="font-size:20px"><b>Acai production in {year} (Tonnes)</b></h3>
    '''
    m_acai.get_root().html.add_child(folium.Element(title_html))

    # Save the map to an HTML file
    m_acai.save(f'map_acai_production_{year}.html')


