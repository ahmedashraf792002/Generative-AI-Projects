import streamlit as st

def unsupervised_models(option):
    if option == 'KMeans':
        st.write("### KMeans Clustering")
        st.write("""
        **KMeans Clustering** is an unsupervised learning algorithm used to divide data into `k` clusters. The algorithm assigns each data point to the nearest cluster and updates the cluster centers based on the mean of the assigned points.
        """)
        st.write("**Code:**")
        st.code("""
        from sklearn.cluster import KMeans

        # Create KMeans model
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(X)

        # Get cluster labels and centers
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_
        """)
    elif option == 'MiniBatchKMeans':
        st.write("### MiniBatchKMeans Clustering")
        st.write("""
        **MiniBatchKMeans** is a faster version of KMeans that uses small batches to update the centers rather than using the full dataset. This is particularly useful when dealing with large datasets.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.cluster import MiniBatchKMeans

            # Create MiniBatchKMeans model
            mini_kmeans = MiniBatchKMeans(n_clusters=3)
            mini_kmeans.fit(X)

            # Get cluster labels and centers
            labels = mini_kmeans.labels_
            centers = mini_kmeans.cluster_centers_
            """)
    elif option == 'Hierarchical Clustering':
        st.write("### Hierarchical Clustering")
        st.write("""
        **Hierarchical Clustering** is a method of cluster analysis which seeks to build a hierarchy of clusters. It starts by treating each data point as a separate cluster and then merges them into larger clusters.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.cluster import AgglomerativeClustering

            # Create AgglomerativeClustering model
            agg_clust = AgglomerativeClustering(n_clusters=3)
            labels = agg_clust.fit_predict(X)
            """)
    elif option == 'DBSCAN':
        st.write("### DBSCAN Clustering")
        st.write("""
        **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that can find arbitrarily shaped clusters and is useful in identifying noise points.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.cluster import DBSCAN

            # Create DBSCAN model
            dbscan = DBSCAN(eps=0.2, min_samples=5)
            labels = dbscan.fit_predict(X)
            """)
    elif option == 'LatentDirichletAllocation':
        st.write("### Latent Dirichlet Allocation (LDA)")
        st.write("""
        **Latent Dirichlet Allocation (LDA)** is a probabilistic model used for discovering topics in a collection of text documents. It assumes each document is a mixture of topics.
        """)
        st.write("**Code:**")
        st.code("""
        from sklearn.decomposition import LatentDirichletAllocation
        from sklearn.feature_extraction.text import CountVectorizer

        # Sample documents for LDA
        documents = ['I love programming in Python.', 'Python is great for data analysis.', 'Machine learning is fun.', 'Scientific data is the future of technology.']

        # Convert documents to numerical format
        vectorizer = CountVectorizer(stop_words='english')
        X_lda = vectorizer.fit_transform(documents)

        # Apply LDA
        lda = LatentDirichletAllocation(n_components=2, random_state=42)
        lda.fit(X_lda)

        # Display topics
        for topic_idx, topic in enumerate(lda.components_):
            print(f"Topic {topic_idx}:")
            print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        """)
    elif option == 'GaussianMixture':
        st.write("### Gaussian Mixture Model (GMM)")
        st.write("""
        **Gaussian Mixture Model (GMM)** is a probabilistic model that assumes all data points are generated from a mixture of several Gaussian distributions with unknown parameters.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.mixture import GaussianMixture

            # Create GMM model
            gmm = GaussianMixture(n_components=3)
            gmm.fit(X)

            # Get cluster labels
            labels = gmm.predict(X)
            """)
    elif option == "Dimensionality Reduction":
        st.write("### Dimensionality Reduction")
        st.info('**PCA**')
        st.subheader("Principal Component Analysis (PCA)")
        st.write("""
        **Principal Component Analysis (PCA)** is a technique used to reduce the dimensionality of data by transforming it into a new coordinate system. The first principal components capture the most variance in the data.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.decomposition import PCA

            # Apply PCA to reduce data to 2 components
            pca = PCA(n_components=2)
            X_reduced = pca.fit_transform(X)
            """)
        st.info('**TSNE**')
        st.write("""
        **t-SNE** is a non-linear dimensionality reduction technique that is particularly useful for visualizing high-dimensional data in 2 or 3 dimensions while maintaining the neighborhood relationships between data points.
        """)
        st.write("**Code:**")
        st.code("""
            from sklearn.manifold import TSNE

            # Apply t-SNE to reduce data to 2 components
            tsne = TSNE(n_components=2)
            X_tsne = tsne.fit_transform(X)

            # Plot the results using matplotlib
            import matplotlib.pyplot as plt
            plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels)
            plt.show()
            """)
        st.info('**LDA (Linear Discriminant Analysis)**')
        st.write("""
        **Linear Discriminant Analysis (LDA)** is used for dimensionality reduction while preserving as much class discriminatory information as possible. Unlike PCA, LDA takes into account class labels and attempts to find a feature space that maximizes class separation.
        """)
        st.write("**Code:**")
        st.code("""
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

        # Apply LDA to reduce data to 2 components
        lda = LinearDiscriminantAnalysis(n_components=2)
        X_lda = lda.fit_transform(X, y)  # y is the target variable (labels)

        # Plot the results using matplotlib
        import matplotlib.pyplot as plt
        plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y)
        plt.show()
        """)
    st.success(f"{option} Unsupervised model implementation details displayed successfully!")
def Evaluation(option):
    if option == "Silhouette Score":
        st.write("### Silhouette Score")
        st.write("**Silhouette Score** Measures how similar each point is to its own cluster compared to other clusters. A higher score indicates that the clusters are well-separated.")
        st.write("**Code**")
        st.code("""
                from sklearn.metrics import silhouette_score
                # Assuming X is your dataset and labels are the predicted cluster labels
                score = silhouette_score(X, labels) 
                print("Silhouette Score:", score)
                """)
    elif option == "Davies-Bouldin Index":
        st.write("### Davies-Bouldin Index")
        st.write("**Davies-Bouldin Index** Measures the average similarity ratio of each cluster with the cluster that is most similar to it. Lower values indicate better clustering.")
        st.write("**Code**")
        st.code("""
                from sklearn.metrics import davies_bouldin_score
                # Assuming X is your dataset and labels are the predicted cluster labels
                score = davies_bouldin_score(X, labels)
                print("Davies-Bouldin Index:", score)
                """)
    elif option == "Dimensionality Reduction Evaluation":
        st.write("### Dimensionality Reduction Evaluation")
        st.info("**PCA Explained Variance Ratio**")
        st.write("**Explained Variance Ratio** Measures how much of the data's variance is captured by each principal component.")
        st.write("**Code**")
        st.code("""
                from sklearn.decomposition import PCA
                pca = PCA(n_components=2)
                pca.fit(X)
                print("Explained Variance Ratio:", pca.explained_variance_ratio_)
                """)
        st.info("**PCA Reconstruction Error**")
        st.write("**Reconstruction Error** Measures how much information is lost when the data is projected to a lower-dimensional space and then reconstructed.")
        st.write("**Code**")
        st.code("""
                from sklearn.decomposition import PCA
                import numpy as np
                
                # Fit PCA
                pca = PCA(n_components=2)
                X_reduced = pca.fit_transform(X)
                
                # Reconstruct the data
                X_reconstructed = pca.inverse_transform(X_reduced)
                
                # Compute the reconstruction error (mean squared error)
                reconstruction_error = np.mean((X - X_reconstructed) ** 2)
                print("Reconstruction Error:", reconstruction_error)
                """)
    st.success(f"{option} model Evaluation implementation details displayed successfully!")