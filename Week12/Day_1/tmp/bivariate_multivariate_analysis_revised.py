import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
data = pd.read_csv(file_path)

# Convert revenue and metascore to numeric types
for column in ['Revenue (Millions)', 'Metascore']:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Bivariate & Multivariate Analysis
def bivariate_multivariate_analysis(data):
    # Correlation Matrix Heatmap
    plt.figure(figsize=(12, 8))
    correlation_matrix = data[['Rating', 'Revenue (Millions)', 'Metascore', 'Votes', 'Runtime (Minutes)']].corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix Heatmap')
    plt.savefig('correlation_matrix_heatmap.png')
    
    # Rating vs Revenue Scatter Plot with Trend Line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Rating', y='Revenue (Millions)', data=data, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Rating vs Revenue')
    plt.xlabel('Rating')
    plt.ylabel('Revenue (Millions)')
    plt.savefig('rating_vs_revenue.png')
    
    # Genre vs Rating Box Plots
    genres = data['Genre'].str.get_dummies(sep=',')
    genre_ratings = pd.concat([data['Rating'], genres], axis=1)
    genre_ratings = pd.melt(genre_ratings, id_vars=['Rating'], var_name='Genre', value_name='Present')
    genre_ratings = genre_ratings[genre_ratings['Present'] == 1]
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='Genre', y='Rating', data=genre_ratings, palette='Set3')
    plt.xticks(rotation=90)
    plt.title('Genre vs Rating')
    plt.xlabel('Genre')
    plt.ylabel('Rating')
    plt.savefig('genre_vs_rating.png')

    # Director performance analysis
    top_directors = data.groupby('Director')['Rating'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_directors.values, y=top_directors.index, palette='coolwarm')
    plt.title('Top Directors by Average Rating')
    plt.xlabel('Average Rating')
    plt.ylabel('Director')
    plt.savefig('top_directors_performance.png')

    # Year vs Rating Trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Year', y='Rating', data=data, ci=None)
    plt.title('Year vs Average Rating')
    plt.xlabel('Year')
    plt.ylabel('Average Rating')
    plt.savefig('year_vs_rating_trend.png')

# Run the bivariate and multivariate analysis
bivariate_multivariate_analysis(data)
print('Bivariate and multivariate analysis completed and plots have been saved.')