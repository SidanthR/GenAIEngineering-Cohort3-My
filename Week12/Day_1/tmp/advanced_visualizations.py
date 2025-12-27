import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
data = pd.read_csv(file_path)

# Advanced Visualizations
def advanced_visualizations(data):
    # Top 20 Highest-Rated Movies
    top_rated_movies = data.sort_values(by='Rating', ascending=False).head(20)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Rating', y='Title', data=top_rated_movies, palette='Spectral')
    plt.title('Top 20 Highest-Rated Movies')
    plt.xlabel('Rating')
    plt.ylabel('Movie Title')
    plt.savefig('top_20_highest_rated_movies.png')

    # Top 20 Highest-Grossing Movies
    top_grossing_movies = data.sort_values(by='Revenue (Millions)', ascending=False).head(20)
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Revenue (Millions)', y='Title', data=top_grossing_movies, palette='cubehelix')
    plt.title('Top 20 Highest-Grossing Movies')
    plt.xlabel('Revenue (Millions)')
    plt.ylabel('Movie Title')
    plt.savefig('top_20_highest_grossing_movies.png')

    # Genre Popularity over Time (Stacked Area Chart)
    data['Year'] = pd.to_datetime(data['Year'], format='%Y')
    genres = data['Genre'].str.get_dummies(sep=',')
    genres_with_year = pd.concat([data['Year'], genres], axis=1)
    genres_sum = genres_with_year.groupby('Year').sum()
    plt.figure(figsize=(14, 8))
    genres_sum.plot(kind='area', stacked=True, colormap='tab20', alpha=0.5)
    plt.title('Genre Popularity Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig('genre_popularity_over_time.png')

    # Rating Distribution by Decade
    data['Decade'] = (data['Year'].dt.year // 10) * 10
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Decade', y='Rating', data=data)
    plt.title('Rating Distribution by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Rating')
    plt.savefig('rating_distribution_by_decade.png')

    # Revenue vs Rating Colored by Genre (Scatter Plot)
    plt.figure(figsize=(10, 6))
    for genre in ['Action', 'Adventure', 'Comedy', 'Drama', 'Animation']:
        subset = data[data['Genre'].str.contains(genre, na=False)]
        plt.scatter(subset['Rating'], subset['Revenue (Millions)'], label=genre, alpha=0.6)
    plt.title('Revenue vs Rating by Genre')
    plt.xlabel('Rating')
    plt.ylabel('Revenue (Millions)')
    plt.legend()
    plt.savefig('revenue_vs_rating_by_genre.png')

# Run the advanced visualizations function
advanced_visualizations(data)
print('Advanced visualizations completed and saved.')