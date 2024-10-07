from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
from GIANTS_personas_classification import classify_market, classify_income, classify_age, classify_mode_of_transport, classify_city, classify_gender, classify_trip_purpose

# Preprocess data specifically for clustering
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd

def preprocess_for_clustering(df):
    """Preprocesses the data for clustering by encoding and scaling all relevant features."""
    
    # Define all the categorical columns to be encoded
    categorical_columns = ['age', 'market', 'gender', 'user_type', 'education', 'income', 'mode']

    
    # Apply OneHotEncoder to the categorical columns
    encoder = OneHotEncoder(drop='first', sparse_output=False)  # Drop first to avoid collinearity
    encoded_data = encoder.fit_transform(df[categorical_columns])
    
    # Create a DataFrame with encoded data
    df_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    
    # Scale the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_encoded)
    
    return df_scaled, df_encoded


def perform_clustering(df_scaled, df_encoded, n_clusters=3):
    """Performs KMeans clustering and assigns cluster labels to the DataFrame."""
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(df_scaled)
    
    # Ensure df_encoded is a DataFrame
    df_encoded = pd.DataFrame(df_encoded, columns=df_encoded.columns)
    
    # Assign the cluster labels to df_encoded
    df_encoded['cluster'] = clusters
    
    return df_encoded



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def visualize_clusters_with_pca(df_scaled, df_with_clusters):
    """Visualizes clusters using PCA in 3D using Plotly."""
    
    # Apply PCA to reduce the data to 3 components
    pca = PCA(n_components=3)
    df_pca = pca.fit_transform(df_scaled)

    # Convert to a DataFrame for easier plotting
    df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2', 'PC3'])
    df_pca['cluster'] = df_with_clusters['cluster']

    # Create a 3D scatter plot with Plotly
    fig = px.scatter_3d(
        df_pca,
        x='PC1', y='PC2', z='PC3',
        color='cluster',
        title='3D Cluster Visualization with PCA',
        labels={'PC1': 'PCA Component 1', 'PC2': 'PCA Component 2', 'PC3': 'PCA Component 3'}
    )
    
    fig.show()

    # Return PCA object for further analysis
    return pca




def plot_elbow_method(df_scaled, max_clusters=10):
    """Creates an elbow plot to determine the optimal number of clusters."""
    
    # List to store the inertia values for each number of clusters
    inertia = []
    
    # Fit KMeans with varying number of clusters (from 1 to max_clusters)
    for n_clusters in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)
    
    # Plot the inertia values for each number of clusters
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_clusters + 1), inertia, marker='o', linestyle='--')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia (Sum of Squared Distances)')
    plt.grid(True)
    plt.show()

def summarize_clusters(df_with_clusters):
    """Summarizes the key characteristics of each cluster and displays it in a nice table format."""
    # Group by cluster and calculate the mean of each one-hot encoded column
    cluster_summary = df_with_clusters.groupby('cluster').mean()
    
    # Display the summary as a formatted DataFrame with two decimal places
    styled_summary = cluster_summary.style.format("{:.2f}")  # Format numbers with 2 decimal places for readability
    
    # Optionally return the styled summary for further display or use
    return styled_summary

def plot_pca_loadings(pca, feature_names):
    """Plots the loadings of each feature on the first two principal components."""
    # Get PCA Loadings
    pca_loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=feature_names)
    print("\nPCA Loadings:")
    print(pca_loadings)

    # Plot the PCA Loadings
    plt.figure(figsize=(8, 6))
    plt.bar(pca_loadings.index, pca_loadings['PC1'], color='blue', alpha=0.6, label='PC1')
    plt.bar(pca_loadings.index, pca_loadings['PC2'], color='red', alpha=0.6, label='PC2')
    plt.title('PCA Loadings for PC1 and PC2')
    plt.ylabel('Feature Contribution')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return pca_loadings


def plot_explained_variance(pca):
    """Plots the explained variance for each principal component."""
    explained_variance = pca.explained_variance_ratio_

    plt.figure(figsize=(8, 6))
    plt.plot(np.cumsum(explained_variance), marker='o', linestyle='--')
    plt.title('Cumulative Explained Variance')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Variance Explained')
    plt.grid(True)
    plt.show()
