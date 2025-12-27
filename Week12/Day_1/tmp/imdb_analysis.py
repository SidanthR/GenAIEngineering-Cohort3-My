import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats

# Load the dataset
file_path = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"
data = pd.read_csv(file_path)

# Function to perform Data Overview & Quality Assessment
def data_overview(data):
    # Dataset shape and info
    print('Data Shape:', data.shape)
    print('Data Info:')
    print(data.info())
    
    # Missing values analysis
    missing_values = data.isnull().sum()
    missing_values_percent = (missing_values / data.shape[0]) * 100
    missing_data_df = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_values_percent})
    print('\nMissing Values Analysis:')
    print(missing_data_df)

    # Plotting missing values
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
    plt.title('Missing Values Heatmap')
    plt.savefig('missing_values_heatmap.png')

    # Statistical summary of numerical variables
    print('\nStatistical Summary of Numerical Columns:')
    print(data.describe())

# Run the overview
print('--- Data Overview & Quality Assessment ---')
data_overview(data)