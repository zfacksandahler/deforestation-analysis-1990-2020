#!/usr/bin/env python3
"""
Analysis and visualization script for global forest cover trends (1990‑2020).
Loads cleaned data, calculates year‑over‑year changes, and produces time‑series plot.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_cleaned_data(path='global_forest_cover_clean.csv'):
    """Load cleaned dataset."""
    df = pd.read_csv(path)
    print(f"Loaded cleaned data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def compute_global_trend(df):
    """
    Aggregate forest cover by year (global total) and compute year‑over‑year percentage change.
    Returns DataFrame with columns: Year, Total_Cover_ha, YoY_Change_pct.
    """
    # Sum forest cover across all regions for each year
    global_df = df.groupby('Year', as_index=False)['Forest_Cover_ha'].sum()
    global_df.rename(columns={'Forest_Cover_ha': 'Total_Cover_ha'}, inplace=True)
    
    # Compute year‑over‑year percentage change
    global_df['YoY_Change_pct'] = global_df['Total_Cover_ha'].pct_change() * 100
    # First year has no previous year → NaN, fill with 0 for plotting
    global_df['YoY_Change_pct'] = global_df['YoY_Change_pct'].fillna(0)
    
    print("Global trend computed:")
    print(global_df.to_string(index=False))
    return global_df

def plot_global_trend(global_df, output_path='forest_trend.png'):
    """
    Create a two‑panel figure:
      - Top: total global forest cover over time
      - Bottom: year‑over‑year percentage change
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Panel 1: total cover
    ax1.plot(global_df['Year'], global_df['Total_Cover_ha'], marker='o', color='forestgreen', linewidth=2)
    ax1.set_ylabel('Global Forest Cover (ha)', fontsize=12)
    ax1.set_title('Global Forest Cover Trend (1990‑2020)', fontsize=14, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.fill_between(global_df['Year'], global_df['Total_Cover_ha'], alpha=0.3, color='forestgreen')
    
    # Panel 2: year‑over‑year change
    colors = ['red' if val < 0 else 'green' for val in global_df['YoY_Change_pct']]
    ax2.bar(global_df['Year'], global_df['YoY_Change_pct'], color=colors, edgecolor='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Year‑over‑Year Change (%)', fontsize=12)
    ax2.set_title('Annual Percentage Change in Forest Cover', fontsize=13)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved as {output_path}")
    plt.close()
    
def regional_analysis(df, output_path='regional_trends.png'):
    """
    Optional: plot forest cover trends for top 5 regions.
    """
    # Identify top 5 regions by average forest cover
    region_avg = df.groupby('Region')['Forest_Cover_ha'].mean().sort_values(ascending=False)
    top_regions = region_avg.head(5).index.tolist()
    print(f"Top 5 regions by average forest cover: {top_regions}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for region in top_regions:
        region_df = df[df['Region'] == region].sort_values('Year')
        ax.plot(region_df['Year'], region_df['Forest_Cover_ha'], marker='.', label=region)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Forest Cover (ha)')
    ax.set_title('Forest Cover Trends for Top 5 Regions (1990‑2020)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Regional trends plot saved as {output_path}")
    plt.close()

if __name__ == '__main__':
    # Load cleaned data
    df = load_cleaned_data()
    
    # Compute global trend
    global_trend = compute_global_trend(df)
    
    # Generate main plot
    plot_global_trend(global_trend, 'forest_trend.png')
    
    # Optional regional analysis (uncomment if desired)
    # regional_analysis(df, 'regional_trends.png')
    
    print("Analysis and visualization completed successfully.")