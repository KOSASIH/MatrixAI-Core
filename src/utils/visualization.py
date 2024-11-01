# src/utils/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> None:
    """Plot a histogram for a specified column in the DataFrame."""
    plt.figure(figsize=(10, 6))
    plt.hist(df[column], bins=bins, color='blue', alpha=0.7)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def plot_scatter(df: pd.DataFrame, x_column: str, y_column: str) -> None:
    """Plot a scatter plot for two specified columns in the DataFrame."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x_column], df[y_column], alpha=0.6)
    plt.title(f'Scatter Plot of {x_column} vs {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid()
    plt.show()

def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """Plot a correlation matrix heatmap for the DataFrame."""
    plt.figure(figsize=(12, 8))
    correlation = df.corr()
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title('Correlation Matrix')
    plt.show()
