#!/usr/bin/env python3
"""
Data cleaning script for global forest cover dataset (1990-2020).
Assumes input file 'global_forest_cover.csv' with columns:
    Year, Region, Forest_Cover_ha
Outputs cleaned dataset to 'global_forest_cover_clean.csv'.
"""

import pandas as pd
import numpy as np
import os

def load_and_clean(input_path='global_forest_cover.csv', output_path='global_forest_cover_clean.csv'):
    """
    Load raw forest cover data, perform cleaning operations, and save cleaned version.
    """
    # Load dataset
    df = pd.read_csv(input_path)
    
    # Display initial info
    print(f"Original dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Missing values per column:\n{df.isnull().sum()}")
    
    # Ensure correct data types
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Forest_Cover_ha'] = pd.to_numeric(df['Forest_Cover_ha'], errors='coerce')
    df['Region'] = df['Region'].astype(str)
    
    # Handle missing values
    # For numeric forest cover, fill with region‑wise median of the same year if possible,
    # otherwise with overall region median.
    numeric_cols = ['Year', 'Forest_Cover_ha']
    for col in numeric_cols:
        if col == 'Forest_Cover_ha':
            # Group by Region and Year to compute medians
            medians = df.groupby(['Region', 'Year'])['Forest_Cover_ha'].transform('median')
            df['Forest_Cover_ha'] = df['Forest_Cover_ha'].fillna(medians)
            # If still missing, fill with region median
            region_medians = df.groupby('Region')['Forest_Cover_ha'].transform('median')
            df['Forest_Cover_ha'] = df['Forest_Cover_ha'].fillna(region_medians)
        else:
            # Year missing? drop rows where Year is NaN (should not happen in this dataset)
            df = df.dropna(subset=['Year'])
    
    # Drop any rows where Region is empty string
    df = df[df['Region'].str.strip() != '']
    
    # Sort by Region and Year for consistency
    df = df.sort_values(['Region', 'Year']).reset_index(drop=True)
    
    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")
    print(f"Cleaned dataset shape: {df.shape}")
    print(f"Missing values after cleaning:\n{df.isnull().sum()}")
    
    return df

if __name__ == '__main__':
    # If running as script, perform cleaning
    df_clean = load_and_clean()
    print("Data cleaning completed successfully.")