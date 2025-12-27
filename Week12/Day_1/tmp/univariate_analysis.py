import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
data = pd.read_csv(file_path)

# Univariate Analysis

def univariate_analysis(data):
    # Rating Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Rating'].dropna(), bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Movie Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.savefig('rating_distribution.png')
    print('Rating distribution plotted and saved as rating_distribution.png')

    # Revenue Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Revenue (Millions)'].dropna(), bins=20, kde=True, color='salmon')
    plt.title('Distribution of Movie Revenue')
    plt.xlabel('Revenue (Millions)')
    plt.ylabel('Frequency')
    plt.savefig('revenue_distribution.png')
    print('Revenue distribution plotted and saved as revenue_distribution.png')

    # Genre Frequency Analysis
    genres = data['Genre'].str.get_dummies(sep=',')
    genre_counts = genres.sum().sort_values(ascending=False)
    plt.figure(figsize=(14, 8))
    sns.barplot(y=genre_counts.index, x=genre_counts.values, palette='viridis')
    plt.title('Genre Frequency Analysis')
    plt.xlabel('Number of Movies')
    plt.ylabel('Genre')
    plt.savefig('genre_frequency.png')
    print('Genre frequency analysis plotted and saved as genre_frequency.png')

    # Release Year Trends
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Year'].dropna(), bins=20, color='lightgreen')
    plt.title('Movie Release Year Trends')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.savefig('release_year_trends.png')
    print('Release year trends plotted and saved as release_year_trends.png')

    # Runtime Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data['Runtime (Minutes)'].dropna(), bins=20, color='lightblue')
    plt.title('Distribution of Movie Runtimes')
    plt.xlabel('Runtime (Minutes)')
    plt.ylabel('Frequency')
    plt.savefig('runtime_distribution.png')
    print('Runtime distribution plotted and saved as runtime_distribution.png')

# Run the univariate analysis
print('--- Univariate Analysis ---')
univariate_analysis(data)