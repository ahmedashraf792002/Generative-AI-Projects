# helper_functions.py

import streamlit as st
from sklearn import datasets
import pandas as pd

def display_dataset_info(dataset_name):
    """
    Display information, feature names, target names, sample data, 
    and provide example code for the selected sklearn dataset.

    Parameters:
    dataset_name (str): Name of the dataset to display
    """
    if dataset_name == 'Iris data':
        st.title("Iris Dataset")
        st.write("The Iris dataset is a classic dataset for classification, containing 150 samples of iris flowers with 4 features.")
        iris = datasets.load_iris()
        st.write("**Feature Names:**")
        st.dataframe(iris.feature_names)
        st.write("**Target Names:**", iris.target_names)
        st.write("**Dataset Shape:**", iris.data.shape)
        st.write("**Sample Data:**")
        st.write(iris.data[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import load_iris
                import pandas as pd

                # Load Iris dataset
                iris = load_iris()

                # X Data
                X = pd.DataFrame(iris.data, columns=iris.feature_names)

                # y Data
                y = pd.Series(iris.target, name="target")
        ''')

    elif dataset_name == 'Digits data':
        st.title("Digits Dataset")
        st.write("The Digits dataset contains 8x8 pixel images of handwritten digits (0-9) for classification tasks.")
        digits = datasets.load_digits()
        st.write("**Images Shape:**", digits.images.shape)
        st.write("**Target Names:**", digits.target_names)
        st.write("**Sample Data:**")
        st.write([digits.images[:2]])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import load_digits
                import pandas as pd

                # Load Digits dataset
                digits = load_digits()

                # X Data
                X = pd.DataFrame(digits.data)

                # y Data
                y = pd.Series(digits.target, name="target")
        ''')

    elif dataset_name == 'California Housing data':
        st.title("California Housing Dataset")
        st.write("The California Housing dataset contains data for regression tasks, with features based on the 1990 California census data.")
        housing = datasets.fetch_california_housing()
        st.write("**Feature Names:**", pd.DataFrame(housing.feature_names,columns=["value"]))
        st.write("**Dataset Shape:**", housing.data.shape)
        st.write("**Sample Data:**")
        st.write(housing.data[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import fetch_california_housing
                import pandas as pd

                # Load California Housing dataset
                housing = fetch_california_housing()

                # X Data
                X = pd.DataFrame(housing.data, columns=housing.feature_names)

                # y Data
                y = pd.Series(housing.target, name="target")
        ''')

    elif dataset_name == 'Wine data':
        st.title("Wine Dataset")
        st.write("The Wine dataset is used for classification and contains the chemical properties of wine.")
        wine = datasets.load_wine()
        st.write("**Feature Names:**", pd.DataFrame(wine.feature_names,columns=["value"]))
        st.write("**Target Names:**", wine.target_names)
        st.write("**Dataset Shape:**", wine.data.shape)
        st.write("**Sample Data:**")
        st.write(wine.data[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import load_wine
                import pandas as pd

                # Load Wine dataset
                wine = load_wine()

                # X Data
                X = pd.DataFrame(wine.data, columns=wine.feature_names)

                # y Data
                y = pd.Series(wine.target, name="target")
        ''')

    elif dataset_name == 'Breast cancer data':
        st.title("Breast Cancer Dataset")
        st.write("The Breast Cancer dataset contains features related to cancer cells and is used for classification tasks.")
        cancer = datasets.load_breast_cancer()
        st.write("**Feature Names:**", cancer.feature_names)
        st.write("**Target Names:**", cancer.target_names)
        st.write("**Dataset Shape:**", cancer.data.shape)
        st.write("**Sample Data:**")
        st.write(cancer.data[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import load_breast_cancer
                import pandas as pd

                # Load Breast Cancer dataset
                cancer = load_breast_cancer()

                # X Data
                X = pd.DataFrame(cancer.data, columns=cancer.feature_names)

                # y Data
                y = pd.Series(cancer.target, name="target")
        ''')

    elif dataset_name == 'Diabetes data':
        st.title("Diabetes Dataset")
        st.write("The Diabetes dataset contains medical data for regression tasks related to diabetes progression.")
        diabetes = datasets.load_diabetes()
        st.write("**Feature Names:**", pd.DataFrame(diabetes.feature_names,columns=["value"]))
        st.write("**Dataset Shape:**", diabetes.data.shape)
        st.write("**Sample Data:**")
        st.write(diabetes.data[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import load_diabetes
                import pandas as pd

                # Load Diabetes dataset
                diabetes = load_diabetes()

                # X Data
                X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)

                # y Data
                y = pd.Series(diabetes.target, name="target")
        ''')

    elif dataset_name == 'Sample Regression':
        st.title("Sample Regression Dataset")
        st.write("This is a synthetic dataset generated for linear regression tasks.")
        X, y = datasets.make_regression(n_samples=100, n_features=1, noise=0.1)
        st.write("**Feature Shape:**", X.shape)
        st.write("**Target Shape:**", y.shape)
        st.write("**Sample Data:**")
        st.write(X[:5], y[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import make_regression
                import pandas as pd

                # Generate Sample Regression Data
                X, y = make_regression(n_samples=100, n_features=1, noise=0.1)

                # Convert to DataFrame
                X = pd.DataFrame(X, columns=["Feature"])
                y = pd.Series(y, name="Target")
        ''')

    elif dataset_name == 'Sample Classification':
        st.title("Sample Classification Dataset")
        st.write("This is a synthetic dataset generated for binary classification tasks.")
        X, y = datasets.make_classification(n_samples=100, n_features=4, n_classes=2)
        st.write("**Feature Shape:**", X.shape)
        st.write("**Target Shape:**", y.shape)
        st.write("**Sample Data:**")
        st.write(X[:5], y[:5])
        st.write("**Code:**")
        st.code('''
                # Import Libraries
                from sklearn.datasets import make_classification
                import pandas as pd

                # Generate Sample Classification Data
                X, y = make_classification(n_samples=100, n_features=4, n_classes=2)

                # Convert to DataFrame
                X = pd.DataFrame(X, columns=[f"Feature_{i+1}" for i in range(X.shape[1])])
                y = pd.Series(y, name="Target")
        ''')
    st.success(f"{dataset_name} details displayed successfully!")


def data_cleaning(option):
    """
    Displays different options for handling missing values, outliers, and their respective code snippets.
    
    Parameters:
    - option (str): The selected data cleaning technique.
    """
    if option == "Handling Missing Values":
        st.write("### Handling Missing Values")
        st.write(
            "This section provides various techniques to handle missing data, "
            "ensuring improved data quality and reliability for analysis and machine learning models."
        )
        
        # 1. Dropping Missing Values
        st.info("**Dropping Missing Values**")
        st.write(
            "This method removes rows or columns with missing data. "
            "Use it cautiously, as it may lead to data loss."
        )
        st.write("**Code:**")
        st.code(''' 
                # Drop rows with missing values
                dataset.dropna(inplace=True)

                # Drop columns with missing values
                dataset.dropna(axis=1, inplace=True)
        ''')

        # 2. Imputation Techniques
        st.info("**Imputation Techniques**")
        
        # Mean/Median/Mode Imputation
        st.write("**Mean Imputation**")
        st.write(
            "Replace missing values with the mean of the respective feature. Useful for numerical data."
        )
        st.write("**Code:**")
        st.code(''' 
                # Replace missing values with the mean
                mean = dataset["column_name"].mean()
                dataset["column_name"].fillna(mean, inplace=True)

                # Using Sklearn
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy="mean")
                dataset["column_name"] = imputer.fit_transform(dataset[["column_name"]])
        ''')

        st.write("**Median Imputation**")
        st.write("Ideal for numerical features with skewed distributions.")
        st.write("**Code:**")
        st.code(''' 
                # Replace missing values with the median
                median = dataset["column_name"].median()
                dataset["column_name"].fillna(median, inplace=True)

                # Using Sklearn
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy="median")
                dataset["column_name"] = imputer.fit_transform(dataset[["column_name"]])
        ''')

        st.write("**Mode Imputation**")
        st.write("Best for categorical features.")
        st.write("**Code:**")
        st.code(''' 
                # Replace missing values with the mode
                mode = dataset["column_name"].mode()[0]
                dataset["column_name"].fillna(mode, inplace=True)

                # Using Sklearn
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy="most_frequent")
                dataset["column_name"] = imputer.fit_transform(dataset[["column_name"]])
        ''')

        # KNN Imputation
        st.info("**KNN Imputation**")
        st.write(
            "Uses the values of nearest neighbors to impute missing data. "
            "Works well for both numerical and categorical data."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.impute import KNNImputer

                # KNN Imputation
                imputer = KNNImputer(n_neighbors=5)
                dataset = pd.DataFrame(imputer.fit_transform(dataset), columns=dataset.columns)
        ''')

        # 3. Advanced Imputation Techniques
        st.info("**Advanced Imputation Techniques**")
        
        st.write("**Regression Imputation**")
        st.write(
            "Predicts missing values using regression models based on other features for numerical."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import LinearRegression

                # Prepare predictors and target
                predictors = dataset.drop(columns=["target_column"]).dropna()
                target = dataset["target_column"].dropna()

                # Train regression model
                model = LinearRegression()
                model.fit(predictors, target)

                # Impute missing values
                missing_indices = dataset[dataset["target_column"].isnull()].index
                predictions = model.predict(dataset.loc[missing_indices].drop(columns=["target_column"]))
                dataset.loc[missing_indices, "target_column"] = predictions
        ''')
        st.write("**Classification Imputation**")
        st.write(
            "Predicts missing values using Classification models based on other features for categorical."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import RandomForestClassifier

                # Prepare predictors and target
                predictors = dataset.drop(columns=["target_column"]).dropna()
                target = dataset["target_column"].dropna()

                # Train Classification model
                model = RandomForestClassifier()
                model.fit(predictors, target)

                # Impute missing values
                missing_indices = dataset[dataset["target_column"].isnull()].index
                predictions = model.predict(dataset.loc[missing_indices].drop(columns=["target_column"]))
                dataset.loc[missing_indices, "target_column"] = predictions
        ''')
        
        st.info("**Iterative Imputer (MICE)**")
        st.write(
            "Performs multivariate imputation by iteratively modeling each variable as a function of others."
        )
        st.write("**Regression Imputation**")
        st.write(
            "Uses a Regression models for imputation, leveraging its predictive power for numerical."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.experimental import enable_iterative_imputer
                from sklearn.impute import IterativeImputer
                from sklearn.linear_model import LinearRegression

                # Regression Imputation
                imputer = IterativeImputer(estimator=LinearRegression(), random_state=42)
                dataset = pd.DataFrame(imputer.fit_transform(dataset), columns=dataset.columns)
        ''')
        st.write("**Classification Imputation**")
        st.write(
            "Uses a Classification models for imputation, leveraging its predictive power for categorical."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.experimental import enable_iterative_imputer
                from sklearn.impute import IterativeImputer
                from sklearn.ensemble import RandomForestClassifier

                # Classification Imputation
                imputer = IterativeImputer(estimator=RandomForestClassifier(), random_state=42)
                dataset = pd.DataFrame(imputer.fit_transform(dataset), columns=dataset.columns)
        ''')

        st.success("By using these techniques, you can ensure more robust handling of missing data in your datasets.")





    # Add an option for Handling Outliers
    elif option == "Handling Outliers":
        st.write("### Handling Outliers")
        st.write(
            "This section provides various techniques to detect and handle outliers in the data. "
            "Outliers can significantly affect the performance of machine learning models, and handling them properly is crucial."
        )
        
        # 1. Z-Score Method
        st.info("**Z-Score Method**")
        st.write(
            "The Z-score method detects outliers by measuring how many standard deviations a data point is from the mean."
        )
        st.write("**Code:**")
        st.code(''' 
                from scipy import stats

                # Calculate Z-scores
                z_scores = stats.zscore(dataset["column_name"])

                # Filter out rows with Z-scores > 3 or < -3
                dataset = dataset[(z_scores < 3) & (z_scores > -3)]
        ''')

        # 2. IQR (Interquartile Range) Method
        st.info("**IQR (Interquartile Range) Method**")
        st.write(
            "The IQR method identifies outliers by measuring the spread between the 25th and 75th percentiles."
        )
        st.write("**Code:**")
        st.code(''' 
                Q1 = dataset["column_name"].quantile(0.25)
                Q3 = dataset["column_name"].quantile(0.75)

                # Calculate IQR
                IQR = Q3 - Q1

                # Filter out outliers
                dataset = dataset[(dataset["column_name"] >= (Q1 - 1.5 * IQR)) & (dataset["column_name"] <= (Q3 + 1.5 * IQR))]
        ''')
        # 3. Isolation Forest
        st.info("**Isolation Forest**")
        st.write(
            "Isolation Forest is an unsupervised algorithm that identifies outliers by isolating them from the rest of the data."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import IsolationForest

                # Create an Isolation Forest model
                model = IsolationForest(contamination=0.1)
                outliers = model.fit_predict(dataset[["column_name"]])

                # Remove outliers (labeled as -1)
                dataset = dataset[outliers != -1]
        ''')
        # 4. LocalOutlierFactor (LOF)
        st.info("**Local Outlier Factor (LOF)**")
        st.write(
            "Local Outlier Factor (LOF) identifies outliers by comparing the density of data points to their neighbors."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.neighbors import LocalOutlierFactor

                # Create LOF model
                lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
                outliers = lof.fit_predict(dataset[["column_name"]])

                # Remove outliers (labeled as -1)
                dataset = dataset[outliers != -1]
        ''')

        # 5. EllipticEnvelope
        st.info("**Elliptic Envelope**")
        st.write(
            "Elliptic Envelope fits a robust Gaussian distribution to the data and detects outliers based on the Mahalanobis distance."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.covariance import EllipticEnvelope

                # Create Elliptic Envelope model
                model = EllipticEnvelope(contamination=0.1)
                model.fit(dataset[["column_name"]])

                # Identify inliers and outliers
                outliers = model.predict(dataset[["column_name"]])

                # Remove outliers (labeled as -1)
                dataset = dataset[outliers != -1]
        ''')

        st.success("By using these techniques, you can effectively handle outliers and improve the performance of your machine learning models.")
        
    
def Preprocessing(option):
    # Encoding Categorical Variables
    if option == "Transform Object Columns":
        st.write("### Transform Object Columns")
        st.write(
            "This section provides techniques to handle categorical variables for machine learning models."
        )

        # Label Encoding
        st.info("**Label Encoding**")
        st.write(
            "Label Encoding converts each category into a unique integer label."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.preprocessing import LabelEncoder

                encoder = LabelEncoder()
                dataset["categorical_column"] = encoder.fit_transform(dataset["categorical_column"])
        ''')

        # One-Hot Encoding
        st.info("**One-Hot Encoding**")
        st.write(
            "One-Hot Encoding creates binary columns for each category in the feature."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.preprocessing import OneHotEncoder

                encoder = OneHotEncoder(sparse=False)
                encoded_data = encoder.fit_transform(dataset[["categorical_column"]])
                dataset_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())
                dataset = pd.concat([dataset, dataset_encoded], axis=1)
        ''')

        # Using `get_dummies()` (Pandas Method)
        st.info("**Using `get_dummies()` (Pandas Method)**")
        st.write(
            "`get_dummies()` automatically creates binary columns for each category. It's the easiest and most efficient way to perform One-Hot Encoding in pandas."
        )
        st.write("**Code:**")
        st.code(''' 
                # Using pandas get_dummies for One-Hot Encoding
                dataset_encoded = pd.get_dummies(dataset, columns=["categorical_column"])
                # The dataset will now have binary columns for each category in the 'categorical_column'
        ''')

        # Ordinal Encoding
        st.info("**Ordinal Encoding**")
        st.write(
            "Ordinal Encoding assigns an integer to each category based on a specified order."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.preprocessing import OrdinalEncoder

                encoder = OrdinalEncoder(categories=[['Low', 'Medium', 'High']])  # Specify the order
                dataset["categorical_column"] = encoder.fit_transform(dataset[["categorical_column"]])
        ''')

        # Target Encoding
        st.info("**Target Encoding**")
        st.write(
            "Target Encoding replaces categories with the mean of the target variable for each category."
        )
        st.write("**Code:**")
        st.code(''' 
                import category_encoders as ce

                encoder = ce.TargetEncoder()
                dataset["categorical_column"] = encoder.fit_transform(dataset["categorical_column"], dataset["target_variable"])
        ''')

        # Binary Encoding
        st.info("**Binary Encoding**")
        st.write(
            "Binary Encoding converts categories into binary digits and represents them as separate columns."
        )
        st.write("**Code:**")
        st.code(''' 
                import category_encoders as ce

                encoder = ce.BinaryEncoder()
                dataset = encoder.fit_transform(dataset["categorical_column"])
        ''')

        # Frequency Encoding
        st.info("**Frequency Encoding**")
        st.write(
            "Frequency Encoding replaces categories with the frequency of their occurrence in the dataset."
        )
        st.write("**Code:**")
        st.code(''' 
                frequency_map = dataset["categorical_column"].value_counts().to_dict()
                dataset["categorical_column_encoded"] = dataset["categorical_column"].map(frequency_map)
        ''')

        st.success("By using these techniques, you can preprocess your dataset efficiently and prepare it for machine learning models.")
    # Feature Selection
    elif option == "Feature Selection":
        st.write("### Feature Selection")
        st.write(
            "This section covers various techniques for selecting the most important features in a dataset."
        )

        # Filter Methods
        st.info("**Filter Methods**")
        st.write(
            "Filter methods evaluate each feature independently from the model, selecting features based on certain criteria."
        )

        # Correlation Matrix
        st.write("**Correlation Matrix**")
        st.write("Identifies highly correlated features and drops one of them.")
        st.write("**Code:**")
        st.code('''
                import numpy as np

                # Compute the correlation matrix
                correlation_matrix = dataset.corr()

                # Set the threshold for high correlation (e.g., 0.9)
                threshold = 0.9

                # Identify the features with high correlation (greater than the threshold)
                high_corr_features = [
                    column for column in correlation_matrix.columns 
                    if any(abs(correlation_matrix[column]) > threshold) and column != correlation_matrix.columns[correlation_matrix[column] > threshold]
                ]

                # Drop the identified high correlation features
                dataset_reduced = dataset.drop(columns=high_corr_features)
                
                # Display the dropped features and the new dataset
                print("Dropped features due to high correlation:", high_corr_features)
                print("Reduced dataset shape:", dataset_reduced.shape)
        ''')

        # Chi-Square Test
        st.write("**Chi-Square Test**")
        st.write("A statistical test to select categorical features.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import SelectKBest, chi2
                X = dataset.drop(columns=["target_variable"])
                y = dataset["target_variable"]
                selector = SelectKBest(score_func=chi2, k='all')
                selector.fit(X, y)
                selected_features = X.columns[selector.get_support()]
        ''')

        # Mutual Information
        st.write("**Mutual Information**")
        st.write("Measures the dependency between variables and selects the best features.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import mutual_info_classif
                X = dataset.drop(columns=["target_variable"])
                y = dataset["target_variable"]
                mutual_info = mutual_info_classif(X, y)
                selected_features = X.columns[mutual_info > 0.1]  # Example threshold
        ''')

        # Wrapper Methods
        st.info("**Wrapper Methods**")
        st.write(
            "Wrapper methods evaluate feature subsets using the model’s performance and select the best feature set."
        )

        # Recursive Feature Elimination (RFE)
        st.write("**Recursive Feature Elimination (RFE)**")
        st.write("RFE recursively removes features and builds the model on remaining features.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import RFE
                from sklearn.linear_model import LogisticRegression
                model = LogisticRegression()
                selector = RFE(model, n_features_to_select=5)
                selector = selector.fit(X, y)
                selected_features = X.columns[selector.support_]
        ''')

        # Forward Selection
        st.write("**Forward Selection**")
        st.write("Forward selection starts with no features and adds features based on model performance.")
        st.write("**Code:**")
        st.code('''
                from sklearn.linear_model import LogisticRegression
                from sklearn.feature_selection import SequentialFeatureSelector
                model = LogisticRegression()
                selector = SequentialFeatureSelector(model, n_features_to_select=5, direction="forward")
                selector = selector.fit(X, y)
                selected_features = X.columns[selector.get_support()]
        ''')

        # Backward Elimination (بردك)
        st.write("**Backward Elimination (بردك)**")
        st.write("Starts with all features and removes the least significant ones based on p-value.")
        st.write("**Code:**")
        st.code('''
                import statsmodels.api as sm
                X = sm.add_constant(X)  # Adds a constant column for intercept
                model = sm.OLS(y, X).fit()
                p_values = model.pvalues
                selected_features = X.columns[p_values < 0.05]  # Example threshold
        ''')

        # Embedded Methods
        st.info("**Embedded Methods**")
        st.write(
            "Embedded methods perform feature selection during model training."
        )

        # L1 Regularization (Lasso)
        st.write("**L1 Regularization (Lasso)**")
        st.write("Lasso applies L1 regularization to shrink feature coefficients to zero.")
        st.write("**Code:**")
        st.code('''
                from sklearn.linear_model import Lasso
                model = Lasso(alpha=0.01)
                model.fit(X, y)
                selected_features = X.columns[model.coef_ != 0]
        ''')

        # Tree-based Methods (Random Forest, XGBoost)
        st.write("**Tree-based Methods (Random Forest, XGBoost)**")
        st.write("Tree-based methods rank feature importance based on splits in decision trees.")
        st.write("**Code:**")
        st.code('''
                from sklearn.ensemble import RandomForestClassifier
                model = RandomForestClassifier()
                model.fit(X, y)
                feature_importance = model.feature_importances_
                selected_features = X.columns[feature_importance > 0.05]  # Example threshold
        ''')

        # SelectFromModel
        st.write("**SelectFromModel**")
        st.write("SelectFromModel selects features based on the importance weights learned by the model.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import SelectFromModel
                from sklearn.ensemble import RandomForestClassifier
                model = RandomForestClassifier()
                model.fit(X, y)

                selector = SelectFromModel(model, threshold="mean")
                selector.fit(X, y)
                selected_features = X.columns[selector.get_support()]
        ''')

        # Dimensionality Reduction
        st.info("**Dimensionality Reduction**")
        st.write(
            "Dimensionality reduction techniques reduce the number of features by transforming them into a lower-dimensional space."
        )

        # PCA (Principal Component Analysis)
        st.write("**PCA**")
        st.write("PCA transforms the data into orthogonal components that explain the most variance.")
        st.write("**Code:**")
        st.code('''
                from sklearn.decomposition import PCA
                pca = PCA(n_components=5)
                principal_components = pca.fit_transform(X)
                selected_features = principal_components
        ''')

        # LDA (Linear Discriminant Analysis)
        st.write("**LDA**")
        st.write("LDA seeks to reduce dimensions while maximizing class separability.")
        st.write("**Code:**")
        st.code('''
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
                lda = LinearDiscriminantAnalysis(n_components=2)
                lda_components = lda.fit_transform(X, y)
                selected_features = lda_components
        ''')

        # Variance Thresholding
        st.write("**Variance Thresholding**")
        st.write("Removes features with low variance.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import VarianceThreshold
                selector = VarianceThreshold(threshold=0.1)
                selector.fit(X)
                selected_features = X.columns[selector.get_support()]
        ''')

        # SelectPercentile
        st.write("**SelectPercentile**")
        st.write("SelectPercentile selects the top features based on a statistical test score.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import SelectPercentile, chi2
                X = dataset.drop(columns=["target_variable"])
                y = dataset["target_variable"]
                selector = SelectPercentile(score_func=chi2, percentile=10)
                selector.fit(X, y)
                selected_features = X.columns[selector.get_support()]
        ''')

        # GenericUnivariateSelect
        st.write("**GenericUnivariateSelect**")
        st.write("GenericUnivariateSelect selects features based on a specified univariate selection method.")
        st.write("**Code:**")
        st.code('''
                from sklearn.feature_selection import GenericUnivariateSelect, chi2
                X = dataset.drop(columns=["target_variable"])
                y = dataset["target_variable"]
                selector = GenericUnivariateSelect(score_func=chi2, mode='k_best', param=5)
                selector.fit(X, y)
                selected_features = X.columns[selector.get_support()]
        ''')

        st.success("By using these techniques, you can efficiently select the most important features for your machine learning model.")
    elif option == "Scaling":
        st.write("### Scaling")
        st.write(
            "This section covers various scaling techniques to normalize or standardize your dataset."
        )

        # Standardization (Z-score normalization)
        st.info("**Standardization (Z-score normalization)**")
        st.write(
            "Standardization transforms the data to have a mean of 0 and a standard deviation of 1."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import StandardScaler

                scaler = StandardScaler()
                dataset_scaled = scaler.fit_transform(dataset)  # Scale the entire dataset
                dataset_scaled = pd.DataFrame(dataset_scaled, columns=dataset.columns)
        ''')

        # Normalization (Min-Max scaling)
        st.info("**Normalization (Min-Max scaling)**")
        st.write(
            "Normalization scales the data to a range, usually [0, 1]. It is useful when the data has varying scales."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import MinMaxScaler

                scaler = MinMaxScaler()
                dataset_normalized = scaler.fit_transform(dataset)  # Normalize the entire dataset
                dataset_normalized = pd.DataFrame(dataset_normalized, columns=dataset.columns)
        ''')

        # Normalizer
        st.info("**Normalizer**")
        st.write(
            "Normalizer scales each sample (row) individually, ensuring that the norm (length) of each sample is 1. It is useful for text classification or clustering tasks."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import Normalizer

                normalizer = Normalizer()
                dataset_normalized = normalizer.fit_transform(dataset)  # Normalize the dataset by rows
                dataset_normalized = pd.DataFrame(dataset_normalized, columns=dataset.columns)
        ''')

        # MaxAbsScaler
        st.info("**MaxAbsScaler**")
        st.write(
            "MaxAbsScaler scales the data by dividing each feature by its maximum absolute value. This ensures that each feature is scaled to the range [-1, 1], without centering it around 0."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import MaxAbsScaler

                scaler = MaxAbsScaler()
                dataset_scaled = scaler.fit_transform(dataset)  # Scale the entire dataset
                dataset_scaled = pd.DataFrame(dataset_scaled, columns=dataset.columns)
        ''')

        # FunctionTransformer
        st.info("**FunctionTransformer**")
        st.write(
            "FunctionTransformer applies a user-defined function to the data, allowing for custom transformations such as log scaling or custom feature extraction."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import FunctionTransformer
                import numpy as np

                # Example: Applying log transformation
                transformer = FunctionTransformer(np.log1p, validate=True)  # log(x + 1) transformation
                dataset_transformed = transformer.fit_transform(dataset)
                dataset_transformed = pd.DataFrame(dataset_transformed, columns=dataset.columns)
        ''')

        # Binarizer
        st.info("**Binarizer**")
        st.write(
            "Binarizer transforms features into binary values (0 or 1) based on a threshold. It is useful for converting continuous data to binary categories."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import Binarizer

                binarizer = Binarizer(threshold=0.0)  # You can change the threshold value
                dataset_binarized = binarizer.fit_transform(dataset)  # Apply binarization
                dataset_binarized = pd.DataFrame(dataset_binarized, columns=dataset.columns)
        ''')

        # PolynomialFeatures
        st.info("**PolynomialFeatures**")
        st.write(
            "PolynomialFeatures generates polynomial and interaction features, which can help capture non-linear relationships in the data."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.preprocessing import PolynomialFeatures

                poly = PolynomialFeatures(degree=2)  # Creates polynomial features up to degree 2
                dataset_poly = poly.fit_transform(dataset)  # Apply polynomial feature transformation
                dataset_poly = pd.DataFrame(dataset_poly, columns=poly.get_feature_names_out(dataset.columns))
        ''')

        st.success(
            "By applying these scaling and transformation techniques, you can improve the performance of machine learning models that are sensitive to the scale or structure of the data."
        )

     # If the option is "Splitting Data"
    elif option == "Splitting Data":
        st.write("### Splitting Data")
        st.write(
            "This section covers techniques for splitting your dataset into training and testing sets."
        )

        # Train-Test Split using sklearn
        st.info("**Train-Test Split**")
        st.write(
            "The `train_test_split` function is the most common way to split your data into training and testing sets."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.model_selection import train_test_split

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])  # Replace "target_column" with your actual target column name
                y = dataset["target_column"]

                # Split data into training and testing sets (80% train, 20% test)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        ''')

        # K-Fold Cross Validation
        st.info("**K-Fold Cross Validation**")
        st.write(
            "K-Fold Cross Validation divides the dataset into 'k' subsets, using one subset as the test set and the remaining as the training set. This process is repeated 'k' times."
        )
        st.write("**Code:**")
        st.code('''
                from sklearn.model_selection import KFold

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # K-Fold Cross Validation (5 folds)
                kf = KFold(n_splits=5, shuffle=True, random_state=42)
                for train_index, test_index in kf.split(X):
                    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                    # Train your model on the X_train, y_train, and test it on X_test, y_test
        ''')
        st.info("**Stratified K-Fold Cross-Validation**")
        st.write("Stratified K-Fold ensures that each fold maintains the same proportion of classes as the original dataset.")
        st.code("""
        from sklearn.model_selection import StratifiedKFold
        
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        for train_index, test_index in skf.split(X, y):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        st.info("**Leave-P-Out Cross-Validation**")
        st.write("Leave-P-Out is similar to LOOCV but leaves P data points out in each iteration.")
        st.code("""
        from sklearn.model_selection import LeavePOut
        
        lpo = LeavePOut(p=2)
        for train_index, test_index in lpo.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        st.info("**Group K-Fold Cross-Validation**")
        st.write("Group K-Fold ensures that the same group is not represented in both the training and test sets.")
        st.code("""
        from sklearn.model_selection import GroupKFold
        
        gkf = GroupKFold(n_splits=5)
        groups = [...]  # Define groups for the data points
        for train_index, test_index in gkf.split(X, y, groups):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        st.info("**Time Series Split (Rolling Cross-Validation)**")
        st.write("Time Series Split is used for time-dependent data. It avoids future data leaking into the training set.")
        st.code("""
        from sklearn.model_selection import TimeSeriesSplit
        
        tscv = TimeSeriesSplit(n_splits=5)
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        
        st.info("**Repeated K-Fold Cross-Validation**")
        st.write("Repeated K-Fold repeats K-Fold multiple times with different random splits.")
        st.code("""
        from sklearn.model_selection import RepeatedKFold
        
        rkf = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)
        for train_index, test_index in rkf.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        st.info("**ShuffleSplit Cross-Validation**")
        st.write("ShuffleSplit randomly splits the data into training and test sets multiple times.")
        st.code("""
        from sklearn.model_selection import ShuffleSplit
        
        ss = ShuffleSplit(n_splits=5, test_size=0.25, random_state=42)
        for train_index, test_index in ss.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)

        st.info("**Stratified ShuffleSplit**")
        st.write("Stratified ShuffleSplit combines Stratified K-Fold and ShuffleSplit.")
        st.code("""
        from sklearn.model_selection import StratifiedShuffleSplit
        
        sss = StratifiedShuffleSplit(n_splits=5, test_size=0.25, random_state=42)
        for train_index, test_index in sss.split(X, y):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            # Train your model on the X_train, y_train, and test it on X_test, y_test
        """)
        st.success(
            "By using these methods, you can ensure that your model is evaluated on multiple splits of the data, leading to better performance estimates."
        )
    # If the option is "Data Balancing"
    elif option == "Data Balancing":
        st.write("### Data Balancing")
        st.write(
            "This section provides methods to handle imbalanced datasets and balance the class distribution."
        )

        # Oversampling using SMOTE
        st.info("**Oversampling using SMOTE (Synthetic Minority Over-sampling Technique)**")
        st.write(
            "SMOTE generates synthetic samples of the minority class to balance the dataset."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import SMOTE

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply SMOTE
                smote = SMOTE(sampling_strategy="auto", random_state=42)
                X_res, y_res = smote.fit_resample(X, y)
        ''')

        # SMOTEENN (SMOTE + Edited Nearest Neighbors)
        st.info("**SMOTEENN (SMOTE + Edited Nearest Neighbors)**")
        st.write(
            "SMOTEENN combines SMOTE for oversampling and Edited Nearest Neighbors for cleaning noisy samples."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import SMOTEENN

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply SMOTEENN
                smoteenn = SMOTEENN(sampling_strategy="auto", random_state=42)
                X_res, y_res = smoteenn.fit_resample(X, y)
        ''')
        # SMOTE for Categorical Features (SMOTEC)
        st.info("**SMOTE for Categorical Features (SMOTEC)**")
        st.write(
            "SMOTEC is a variant of SMOTE that is suitable for datasets with categorical features."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import SMOTENC

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Specify the categorical feature indices (0-based)
                categorical_features = [0, 2, 3]  # Example: column indices for categorical features

                # Apply SMOTEC
                smotec = SMOTENC(categorical_features=categorical_features, sampling_strategy="auto", random_state=42)
                X_res, y_res = smotec.fit_resample(X, y)
        ''')

        # Random Oversampling
        st.info("**Random Oversampling using RandomOverSampler**")
        st.write(
            "Random Oversampling generates synthetic samples by randomly duplicating minority class samples."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import RandomOverSampler

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply Random Oversampling
                ros = RandomOverSampler(sampling_strategy="auto", random_state=42)
                X_res, y_res = ros.fit_resample(X, y)
        ''')

        # ADASYN (Adaptive Synthetic Sampling)
        st.info("**ADASYN (Adaptive Synthetic Sampling)**")
        st.write(
            "ADASYN creates synthetic samples focusing more on the minority class samples that are difficult to learn."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import ADASYN

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply ADASYN
                adasyn = ADASYN(sampling_strategy="auto", random_state=42)
                X_res, y_res = adasyn.fit_resample(X, y)
        ''')
        # Borderline-SMOTE
        st.info("**Borderline-SMOTE**")
        st.write(
            "Borderline-SMOTE focuses on generating synthetic data near the decision boundary between classes."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import BorderlineSMOTE

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply Borderline-SMOTE
                borderline_smote = BorderlineSMOTE(sampling_strategy="auto", random_state=42)
                X_res, y_res = borderline_smote.fit_resample(X, y)
        ''')
        # KMeansSMOTE
        st.info("**KMeansSMOTE**")
        st.write(
            "KMeansSMOTE combines k-means clustering with SMOTE to generate synthetic samples based on clusters."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import KMeansSMOTE

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply KMeansSMOTE
                kmeans_smote = KMeansSMOTE(sampling_strategy="auto", random_state=42)
                X_res, y_res = kmeans_smote.fit_resample(X, y)
        ''')

        # SVMSMOTE (SMOTE with SVM)
        st.info("**SVMSMOTE (SMOTE with SVM)**")
        st.write(
            "SVMSMOTE combines SMOTE with Support Vector Machines to generate synthetic samples near the decision boundary."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.over_sampling import SVMSMOTE

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply SVMSMOTE
                svmsmote = SVMSMOTE(sampling_strategy="auto", random_state=42)
                X_res, y_res = svmsmote.fit_resample(X, y)
        ''')        

        # Undersampling using RandomUnderSampler
        st.info("**Undersampling using RandomUnderSampler**")
        st.write(
            "RandomUnderSampler reduces the number of samples in the majority class by randomly removing data points, balancing the dataset."
        )
        st.write("**Code:**")
        st.code(''' 
                from imblearn.under_sampling import RandomUnderSampler

                # Splitting dataset into features (X) and target variable (y)
                X = dataset.drop(columns=["target_column"])
                y = dataset["target_column"]

                # Apply Random Under-sampling
                undersampler = RandomUnderSampler(sampling_strategy="auto", random_state=42)
                X_res, y_res = undersampler.fit_resample(X, y)
        ''')
        # Compute Class Weights (Balanced by Count)
        st.info("**Class Weights (Balanced by Count)**")
        st.write(
            "Class weights can be computed based on the frequency of each class in the dataset."
        )
        st.write("**Code:**")
        st.code(''' 
                from sklearn.utils.class_weight import compute_class_weight

                # Calculate class weights
                class_weights = compute_class_weight(
                    class_weight='balanced', 
                    classes=np.unique(y), 
                    y=y
                )

                class_weight_dict = dict(zip(np.unique(y), class_weights))
                print(class_weight_dict)
        ''')

        # Explanation of `compute_class_weight`:
        st.write(
            "The `compute_class_weight` function computes weights for each class in the target variable based on their frequency in the dataset."
        )

        st.success(
            "By using these techniques, you can mitigate the effects of class imbalance and improve model performance."
        )
