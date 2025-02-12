import streamlit as st

def Regression_Models(option):
    if option == "Linear Regression":
        st.write("### Linear Regression")
        st.write("Linear Regression assumes a linear relationship between the features and target variable.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import LinearRegression

                model = LinearRegression(fit_intercept=True, normalize=False)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`fit_intercept`: Whether to calculate the intercept.\n`normalize`: Normalize the input features.")

    elif option == "SGD Regression":
        st.write("### SGD Regression")
        st.write("Stochastic Gradient Descent for linear models with optional regularization (L1, L2).")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import SGDRegressor

                model = SGDRegressor(max_iter=1000, tol=1e-3, penalty='l2')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum number of iterations.\n`tol`: Stopping tolerance.\n`penalty`: Regularization term.")

    elif option == "Lasso":
        st.write("### Lasso Regression")
        st.write("Lasso adds L1 regularization to the loss function, leading to sparse coefficients.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import Lasso

                model = Lasso(alpha=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")

    elif option == "Ridge":
        st.write("### Ridge Regression")
        st.write("Ridge adds L2 regularization to the loss function to reduce multicollinearity.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import Ridge

                model = Ridge(alpha=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")

    elif option == "Random Forest Regressor":
        st.write("### Random Forest Regressor")
        st.write("Random Forest aggregates multiple decision trees to improve predictions.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import RandomForestRegressor

                model = RandomForestRegressor(n_estimators=100, max_depth=None)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of trees.\n`max_depth`: Maximum tree depth.")

    elif option == "Gradient Boosting Regressor":
        st.write("### Gradient Boosting Regressor")
        st.write("Gradient Boosting builds models sequentially to correct errors of previous models.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import GradientBoostingRegressor

                model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of boosting stages.\n`learning_rate`: Step size.\n`max_depth`: Maximum tree depth.")

    elif option == "AdaBoost Regressor":
        st.write("### AdaBoost Regressor")
        st.write("AdaBoost combines weak learners iteratively to minimize errors.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import AdaBoostRegressor

                model = AdaBoostRegressor(n_estimators=50, learning_rate=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of boosting stages.\n`learning_rate`: Weight applied to each regressor.")

    elif option == "SVR":
        st.write("### Support Vector Regressor (SVR)")
        st.write("SVR fits the error within a margin (epsilon).")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.svm import SVR

                model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`kernel`: Type of kernel.\n`C`: Regularization parameter.\n`epsilon`: Epsilon-tube size.")

    elif option == "Decision Tree Regressor":
        st.write("### Decision Tree Regressor")
        st.write("Decision Tree splits data into smaller subsets recursively.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.tree import DecisionTreeRegressor

                model = DecisionTreeRegressor(max_depth=None)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`max_depth`: Maximum tree depth.")

    elif option == "MLP Regressor":
        st.write("### MLP Regressor")
        st.write("MLP Regressor is a neural network-based regressor.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.neural_network import MLPRegressor

                model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=200)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`hidden_layer_sizes`: Structure of hidden layers.\n`max_iter`: Maximum iterations.")

    elif option == "KNeighbors Regressor":
        st.write("### KNeighbors Regressor")
        st.write("KNN Regressor predicts the value by averaging the target of its k nearest neighbors.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.neighbors import KNeighborsRegressor

                model = KNeighborsRegressor(n_neighbors=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_neighbors`: Number of neighbors to consider.")

    elif option == "XGB Regressor":
        st.write("### XGB Regressor")
        st.write("XGBoost uses gradient boosting framework for improved performance.")
        st.write("**Code:**")
        st.code(''' 
                from xgboost import XGBRegressor

                model = XGBRegressor(n_estimators=100, learning_rate=0.1)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of boosting stages.\n`learning_rate`: Step size.")

    elif option == "LGBM Regressor":
        st.write("### LightGBM Regressor")
        st.write("LightGBM is a gradient boosting framework that uses tree-based learning.")
        st.write("**Code:**")
        st.code(''' 
                from lightgbm import LGBMRegressor

                model = LGBMRegressor(n_estimators=100, learning_rate=0.1)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of boosting stages.\n`learning_rate`: Step size.")

    elif option == "CatBoost Regressor":
        st.write("### CatBoost Regressor")
        st.write("CatBoost is a gradient boosting library that handles categorical features effectively.")
        st.write("**Code:**")
        st.code(''' 
                from catboost import CatBoostRegressor

                model = CatBoostRegressor(iterations=1000, learning_rate=0.03)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`iterations`: Number of boosting stages.\n`learning_rate`: Step size.")
    elif option == "Isotonic Regression":
        st.write("### Isotonic Regression")
        st.write("Isotonic regression is a non-parametric approach to fit a regression model.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.isotonic import IsotonicRegression

                model = IsotonicRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("No hyperparameters to tune.")
    elif option == "Kernel Ridge":
        st.write("### Kernel Ridge Regression")
        st.write("Kernel Ridge performs ridge regression using a non-linear kernel.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.kernel_ridge import KernelRidge

                model = KernelRidge(alpha=1.0, kernel='rbf')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.\n`kernel`: Type of kernel.")

    elif option == "Gaussian Process Regressor":
        st.write("### Gaussian Process Regressor")
        st.write("Gaussian Process regression performs non-linear regression using probabilistic modeling.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.gaussian_process import GaussianProcessRegressor

                model = GaussianProcessRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`kernel`: Kernel used in the model.\n`n_restarts_optimizer`: Number of restarts for optimizer.")
    elif option == "Tweedie Regressor":
        st.write("### Tweedie Regressor")
        st.write("Tweedie regression is a type of GLM used when the variance of the target depends on the mean.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import TweedieRegressor

                model = TweedieRegressor(power=1.0, alpha=0.5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`power`: Specifies the power of the distribution.\n`alpha`: Regularization strength.")

    elif option == "Hist Gradient Boosting Regressor":
        st.write("### Hist Gradient Boosting Regressor")
        st.write("Histogram-based gradient boosting method that is faster than traditional gradient boosting.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import HistGradientBoostingRegressor

                model = HistGradientBoostingRegressor(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum number of iterations.\n`learning_rate`: The learning rate.")

    elif option == "Extra Trees Regressor":
        st.write("### Extra Trees Regressor")
        st.write("Extra Trees are an ensemble of many decision trees for improved regression.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import ExtraTreesRegressor

                model = ExtraTreesRegressor(n_estimators=100, max_depth=None)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of trees.\n`max_depth`: Maximum tree depth.")
    elif option == "Bagging Regressor":
        st.write("### Bagging Regressor")
        st.write("Bagging applies bootstrap sampling to multiple models for improved predictions.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import BaggingRegressor

                model = BaggingRegressor(base_estimator=DecisionTreeRegressor(), n_estimators=100)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`base_estimator`: Base model to use.\n`n_estimators`: Number of models.")

    elif option == "Stacking Regressor":
        st.write("### Stacking Regressor")
        st.write("Stacking combines multiple models to improve performance.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import StackingRegressor

                model = StackingRegressor(estimators=[('lr', LinearRegression()), ('rf', RandomForestRegressor())]
                ,final_estimator=RandomForestRegressor(n_estimators=10,random_state=42))
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`estimators`: Base models to stack.\n`final_estimator`: Final model.")
    elif option == "Radius Neighbors Regressor":
        st.write("### Radius Neighbors Regressor")
        st.write("Radius Neighbors regression applies a fixed radius to include nearby neighbors.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.neighbors import RadiusNeighborsRegressor

                model = RadiusNeighborsRegressor(radius=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`radius`: Maximum distance for neighbors to influence prediction.")

    elif option == "Nearest Centroid":
        st.write("### Nearest Centroid Regression")
        st.write("Nearest Centroid regression assigns the value of the nearest centroid to a given point.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.neighbors import NearestCentroid

                model = NearestCentroid()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("No hyperparameters to tune.")
    
    elif option == "NuSVR":
        st.write("### NuSVR")
        st.write("NuSVR is a Support Vector Regression model with a flexible margin.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.svm import NuSVR

                model = NuSVR(nu=0.1, C=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`nu`: Upper bound on fraction of margin errors.\n`C`: Regularization parameter.")

    elif option == "LinearSVR":
        st.write("### LinearSVR")
        st.write("LinearSVR performs linear regression with a support vector approach.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.svm import LinearSVR

                model = LinearSVR(C=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`C`: Regularization parameter.")
    elif option == "Huber Regressor":
        st.write("### Huber Regressor")
        st.write("Huber regression is a robust model that combines squared loss and absolute error.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import HuberRegressor

                model = HuberRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`epsilon`: Threshold for switching between quadratic and linear loss.")

    elif option == "ARD Regression":
        st.write("### ARD Regression")
        st.write("Automatic Relevance Determination regression applies Bayesian inference to select features.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import ARDRegression

                model = ARDRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha_1`: Shape of prior distribution.\n`lambda_1`: Scale of prior distribution.")

    elif option == "ElasticNet":
        st.write("### ElasticNet")
        st.write("ElasticNet is a regularized regression model combining Lasso and Ridge regression.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import ElasticNet

                model = ElasticNet(alpha=1.0, l1_ratio=0.5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.\n`l1_ratio`: Mixing ratio between Lasso and Ridge.")

    elif option == "Orthogonal Matching Pursuit":
        st.write("### Orthogonal Matching Pursuit")
        st.write("OMP selects the most relevant features by orthogonally matching the predictors.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import OrthogonalMatchingPursuit

                model = OrthogonalMatchingPursuit(n_nonzero_coefs=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`n_nonzero_coefs`: Number of features to select.")

    elif option == "PassiveAggressive Regressor":
        st.write("### Passive-Aggressive Regressor")
        st.write("Passive-Aggressive is an online regression method that updates based on error.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import PassiveAggressiveRegressor

                model = PassiveAggressiveRegressor(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum iterations.\n`C`: Regularization strength.")
        

    elif option == "Bayesian Ridge":
        st.write("### Bayesian Ridge Regression")
        st.write("Bayesian Ridge Regression applies a probabilistic approach to linear regression by assuming that the model parameters are distributed according to a normal distribution.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import BayesianRidge

                model = BayesianRidge()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha_1` and `alpha_2`: Prior parameters for the noise and model.")
    
    elif option == "Quantile Regressor":
        st.write("### Quantile Regressor")
        st.write("Quantile regression is used when you need to predict specific quantiles instead of the mean.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import QuantileRegressor

                model = QuantileRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")

    elif option == "Poisson Regressor":
        st.write("### Poisson Regressor")
        st.write("Poisson Regression models count data by assuming the target variable follows a Poisson distribution.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import PoissonRegressor

                model = PoissonRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")
    
    elif option == "TheilSen Regressor":
        st.write("### Theil-Sen Regressor")
        st.write("Theil-Sen Regression is a robust estimator used when the data may contain outliers.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import TheilSenRegressor

                model = TheilSenRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum number of iterations.")

    elif option == "RANSAC Regressor":
        st.write("### RANSAC Regressor")
        st.write("RANSAC is a regression method that is robust to outliers and can perform well in the presence of a significant number of outliers.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import RANSACRegressor

                model = RANSACRegressor()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`min_samples`: The minimum number of samples to consider for a valid fit.")
        
    elif option == "Logistic Regression":
        st.write("### Logistic Regression")
        st.write("Although commonly used for classification, Logistic Regression can also be used for regression tasks in some scenarios.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import LogisticRegression

                model = LogisticRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`C`: Regularization strength.")

    elif option == "ElasticNetCV":
        st.write("### ElasticNetCV")
        st.write("ElasticNetCV is a regression model that combines the Lasso and Ridge methods. It also automatically tunes the alpha and l1_ratio parameters.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import ElasticNetCV

                model = ElasticNetCV(cv=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`l1_ratio`: The mix ratio of Lasso and Ridge regularization.\n`cv`: Number of cross-validation folds.")

    elif option == "RidgeCV":
        st.write("### RidgeCV")
        st.write("RidgeCV is a version of Ridge regression that automatically selects the best regularization parameter using cross-validation.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import RidgeCV

                model = RidgeCV()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alphas`: List of candidate regularization strengths.")

    elif option == "LassoCV":
        st.write("### LassoCV")
        st.write("LassoCV is a version of Lasso regression that automatically selects the best regularization parameter using cross-validation.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.linear_model import LassoCV

                model = LassoCV()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`alphas`: List of candidate regularization strengths.")

    elif option == "Voting Regressor":
        st.write("### Voting Regressor")
        st.write("Voting Regressor combines multiple regression models to improve predictive performance by averaging their predictions.")
        st.write("**Code:**")
        st.code(''' 
                from sklearn.ensemble import VotingRegressor
                from sklearn.linear_model import LinearRegression
                from sklearn.ensemble import RandomForestRegressor

                # Create a Voting Regressor
                regressor1 = LinearRegression()
                regressor2 = RandomForestRegressor()
                model = VotingRegressor([('lr', regressor1), ('rf', regressor2)])

                # Fit the model
                model.fit(X_train, y_train)

                # Make predictions
                y_pred = model.predict(X_test)
        ''')
        st.info("**Hyperparameters:**")
        st.write("`estimators`: List of (name, model) pairs.")

    
    st.success(f"{option} model implementation details displayed successfully!")

def Regression_Check(option):
    if option == "Median Absolute Error":
        # Display the explanation and code block in Streamlit
        st.write("### Median Absolute Error")
        st.write("Median Absolute Error measures the median of the absolute errors between the predicted and actual values. It is robust to outliers.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import median_absolute_error

        # Assuming y_test and y_pred are already defined
        median_error = median_absolute_error(y_test, y_pred)
        print("Median Absolute Error:", median_error)
        """)
                
    elif option == "R2 Score":
        # Display the explanation and code block in Streamlit
        st.write("### R2 Score")
        st.write("R2 Score (Coefficient of Determination) indicates how well the regression model explains the variance of the target variable. A higher value means a better fit.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import r2_score

        # Assuming y_test and y_pred are already defined
        r2 = r2_score(y_test, y_pred)
        print("R2 Score:", r2)
        """)    

    elif option == "Mean Absolute Error":
        # Display the explanation and code block in Streamlit
        st.write("### Mean Absolute Error")
        st.write("Mean Absolute Error measures the average of the absolute differences between the predicted and actual values. It provides an intuitive measure of prediction accuracy.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import mean_absolute_error

        # Assuming y_test and y_pred are already defined
        mae = mean_absolute_error(y_test, y_pred)
        print("Mean Absolute Error:", mae)
        """)
        
    elif option == "Mean Squared Error":
        # Display the explanation and code block in Streamlit
        st.write("### Mean Squared Error")
        st.write("Mean Squared Error (MSE) measures the average of the squared differences between the predicted and actual values. A lower value indicates a better model fit.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import mean_squared_error

        # Assuming y_test and y_pred are already defined
        mse = mean_squared_error(y_test, y_pred)
        print("Mean Squared Error:", mse)
        """) 

    elif option == "Root Mean Squared Error":
        # Display the explanation and code block in Streamlit
        st.write("### Root Mean Squared Error")
        st.write("Root Mean Squared Error is the square root of MSE, providing an error metric in the same unit as the target variable.")
        st.write("**Code:**")
        st.code("""
        import numpy as np

        # Assuming y_test and y_pred are already defined
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print("Root Mean Squared Error:", rmse)
        """)

    elif option == "Explained Variance Score":
        # Display the explanation and code block in Streamlit
        st.write("### Explained Variance Score")
        st.write("Explained Variance Score measures the proportion of the variance in the predicted data that can be explained by the model. Higher values indicate better performance.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import explained_variance_score

        # Assuming y_test and y_pred are already defined
        evs = explained_variance_score(y_test, y_pred)
        print("Explained Variance Score:", evs)
        """)

    elif option == "Huber Loss":
        # Display the explanation and code block in Streamlit
        st.write("### Huber Loss")
        st.write("Huber Loss is a combination of Mean Squared Error and Mean Absolute Error, less sensitive to outliers than MSE.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        # Assuming y_test and y_pred are already defined
        huber_loss = np.mean(np.where(np.abs(y_test - y_pred) < 1, 0.5 * (y_test - y_pred) ** 2, np.abs(y_test - y_pred) - 0.5))
        print("Huber Loss:", huber_loss)
        """)

    elif option == "Poisson Loss":
        # Display the explanation and code block in Streamlit
        st.write("### Poisson Loss")
        st.write("Poisson Loss is used for count data, appropriate when the target variable is a count.")
        st.code("""
        from sklearn.metrics import mean_poisson_deviance

        # Assuming y_test and y_pred are already defined
        poisson_loss = mean_poisson_deviance(y_test, y_pred)
        print("Poisson Loss:", poisson_loss)
        """)

    elif option == "Logarithmic Loss (Log Loss)":
        # Display the explanation and code block in Streamlit
        st.write("### Logarithmic Loss")
        st.write("Log Loss evaluates the probability output of a classification model, but it's sometimes used in regression for continuous probabilities.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import log_loss

        # Assuming y_test and y_pred are already defined
        log_loss_value = log_loss(y_test, y_pred)
        print("Logarithmic Loss:", log_loss_value)
        """)
    elif option == "Max Error":
        st.write("### Max Error")
        st.write("Max Error measures the maximum absolute difference between the predicted and actual values.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import max_error
        max_err = max_error(y_test, y_pred)
        print("Max Error:", max_err)
        """)

    elif option == "Mean Squared Log Error":
        st.write("### Mean Squared Log Error")
        st.write("Mean Squared Log Error measures the squared difference of the log-transformed values of predicted and actual values.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import mean_squared_log_error
        msle = mean_squared_log_error(y_test, y_pred)
        print("Mean Squared Log Error:", msle)
        """)

    elif option == "Log-Cosh Loss":
        st.write("### Log-Cosh Loss")
        st.write("Log-Cosh Loss is a smoother alternative to Mean Squared Error, less sensitive to outliers.")
        st.write("**Code:**")
        st.code("""
        import numpy as np
        def log_cosh(y_true, y_pred):
            return np.mean(np.log(np.cosh(y_pred - y_true)))
        loss = log_cosh(y_test, y_pred)
        print("Log-Cosh Loss:", loss)
        """)
    st.success(f"{option} model Evaluation implementation details displayed successfully!")