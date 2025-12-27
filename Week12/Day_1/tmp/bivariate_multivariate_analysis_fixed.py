import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load the dataset
file_path = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
data = pd.read_csv(file_path)

# Convert appropriate columns to numeric, handling errors
data['Revenue (Millions)'] = pd.to_numeric(data['Revenue (Millions)'], errors='coerce')
data['Metascore'] = pd.to_numeric(data['Metascore'], errors='coerce')

def clean_column_names(data):
    data.columns = [re.sub(r'[\s]+', '_', col) for col in data.columns]
    return data

# Bivariate & Multivariate Analysis
def bivariate_multivariate_analysis(data):
    data = clean_column_names(data)
    # Correlation Matrix Heatmap
    plt.figure(figsize=(12, 8))
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix Heatmap')
    plt.savefig('correlation_matrix_fixed.png')
    print('Correlation matrix heatmap saved as correlation_matrix_fixed.png')

    # Rating vs Revenue Scatter Plot with Trend Line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Rating', y='Revenue_(Millions)', data=data, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Rating vs Revenue')
    plt.xlabel('Rating')
    plt.ylabel('Revenue (Millions)')
    plt.savefig('rating_vs_revenue_fixed.png')
    print('Rating vs Revenue plot saved as rating_vs_revenue_fixed.png')

    # Genre vs Rating Box Plots
    genres = data['Genre'].str.get_dummies(sep=',')
    for genre in genres.columns:
        data[genre] = genres[genre]
    genre_ratings = pd.melt(data, id_vars=['Rating'], value_vars=genres.columns)
    genre_ratings = genre_ratings[genre_ratings['value'] == 1]
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='variable', y='Rating', data=genre_ratings, palette='Set3')
    plt.xticks(rotation=90)
    plt.title('Genre vs Rating')
    plt.xlabel('Genre')
    plt.ylabel('Rating')
    plt.savefig('genre_vs_rating_fixed.png')
    print('Genre vs Rating box plots saved as genre_vs_rating_fixed.png')

    # Director Performance Analysis
    top_directors = data.groupby('Director')['Rating'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_directors.values, y=top_directors.index, palette='mako')
    plt.title('Top Directors by Average Rating')
    plt.xlabel('Average Rating')
    plt.ylabel('Director')
    plt.savefig('top_directors_fixed.png')
    print('Top directors by average rating bar chart saved as top_directors_fixed.png')

    # Year vs Rating Trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Year', y='Rating', data=data, ci=None)
    plt.title('Year vs Average Rating')
    plt.xlabel('Year')
    plt.ylabel('Average Rating')
    plt.savefig('year_vs_rating_fixed.png')
    print('Year vs Average Rating line plot saved as year_vs_rating_fixed.png')

# Run the analysis
print('--- Bivariate & Multivariate Analysis ---')
bivariate_multivariate_analysis(data)