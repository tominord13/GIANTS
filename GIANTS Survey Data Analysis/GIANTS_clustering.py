from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd


# Step 1: Scale the data
def scale_data(df):
    """Scales the data using StandardScaler."""
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    return df_scaled

# Perform clustering
def perform_clustering(df_encoded, df_scaled, n_clusters=5):
    """Performs K-means clustering on the scaled data."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    
    # Predict the clusters using scaled data
    clusters = kmeans.fit_predict(df_scaled)
    
    # Assign the cluster labels back to the original DataFrame (df_encoded)
    df_encoded['Cluster'] = clusters
    
    return df_encoded

# Step 3: Visualize clusters
def visualize_clusters(df, feature_1, feature_2):
    """Visualizes clusters in a scatter plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[feature_1], df[feature_2], c=df['Cluster'], cmap='viridis')
    plt.xlabel(feature_1)
    plt.ylabel(feature_2)
    plt.title('Cluster Visualization')
    plt.colorbar(label='Cluster')
    plt.show()

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


# The visualize_clusters_with_pca function should be as follows:
def visualize_clusters_with_pca(df_scaled, clusters):
    # Apply PCA to reduce dimensions to 2 components
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_pca[:, 0], y=df_pca[:, 1], hue=clusters, palette='viridis')
    plt.title('Cluster Visualization using PCA')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(title='Cluster')
    plt.show()
