import streamlit as st 
def Cross_Validation(option):
    if option == 'Cross Validate':
            st.write("### Cross Validate")
            st.write("Evaluates a model using cross-validation and returns a dictionary with multiple scores.")
            st.write("**Code:**")
            st.code("""
            from sklearn.model_selection import cross_validate

            scores = cross_validate(model, X, y, cv=5, scoring=['accuracy', 'f1_weighted'])
            print("Scores:", scores)
            """)

    elif option == 'Cross Validate Predict':
        st.write("### Cross Validate Predict")
        st.write("Generates cross-validated estimates for each input data point.")
        st.write("**Code:**")
        st.code("""
        from sklearn.model_selection import cross_val_predict

        predictions = cross_val_predict(model, X, y, cv=5)
        print("Predictions:", predictions)
        """)
        from sklearn.model_selection import cross_val_predict

    elif option == 'Cross Validate Score':
        st.write("### Cross Validate Score")
        st.write("Calculates scores for a model using cross-validation.")
        st.write("**Code:**")
        st.code("""
        from sklearn.model_selection import cross_val_score

        scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        print("Scores:", scores)
        print("Mean Accuracy:", scores.mean())
        """)
    elif option == 'TunedThresholdClassifierCV':
        # Assuming you have the TunedThresholdClassifierCV defined elsewhere
        st.write("### TunedThresholdClassifierCV")
        st.write("Evaluates a model using cross-validation with custom threshold tuning.")
        st.write("**Code:**")
        st.code("""
        from some_module import TunedThresholdClassifierCV

        model = TunedThresholdClassifierCV()
        scores = cross_validate(model, X, y, cv=5, scoring=['accuracy', 'f1_weighted'])
        print("Scores:", scores)
        """)
    st.success(f"{option} model Validation implementation details displayed successfully!")
    

def Hyperparameter_Tuning(option):
    if option == 'Grid Searching':
        st.write("### Grid Searching")
        st.write("Exhaustively tests a set of hyperparameters and evaluates each combination to find the best one.")
        st.write("**Code:**")
        st.code("""
        from sklearn.model_selection import GridSearchCV
        
        param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=2)
        grid_search.fit(X, y)
        
        print("Best Parameters:", grid_search.best_params_)
        print("Grid Search Results:", grid_search.cv_results_)
        """)
        
    elif option == 'Randomized Grid Searching':
        st.write("### Randomized Grid Searching")
        st.write("Randomly samples hyperparameter values from a specified range, making it faster for large hyperparameter spaces.")
        st.write("**Code:**")
        st.code("""
        from sklearn.model_selection import RandomizedSearchCV
        from scipy.stats import randint
        
        param_dist = {
            'n_estimators': randint(10, 200),
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': randint(2, 10),
            'min_samples_leaf': randint(1, 10)
        }
        
        random_search = RandomizedSearchCV(model, param_dist, n_iter=100, cv=5, n_jobs=-1, verbose=2)
        random_search.fit(X, y)
        
        print("Best Parameters:", random_search.best_params_)
        print("Randomized Search Results:", random_search.cv_results_)
        """)
    elif option == 'Pipeline':
        # Fit Model with Pipeline
        st.info("**Fit Model With Pipeline**")
        st.write("In this section, we'll fit a model using a pipeline that combines preprocessing and classification.")
        st.write("**Code:**")
        st.code("""
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier
        
        # Create the pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Preprocessing step: Standard scaling
            ('classifier', RandomForestClassifier(n_estimators=100))  # Classification step: RandomForest
        ])
        
        # Fit the pipeline on training data
        pipeline.fit(X_train, y_train)
        
        # Make predictions
        y_pred = pipeline.predict(X_test)
        """)
        # Hyperparameter Tuning with Pipeline
        st.info("**Hyperparameter Tuning with Pipeline**")
        st.write("We can use GridSearchCV within the pipeline to perform hyperparameter tuning.")
        st.write("**Code:**")
        st.code("""
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import GridSearchCV
        
        # Define the pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Scaling
            ('classifier', model)  # Model placeholder
        ])
        
        # Define hyperparameter grid
        param_grid = {
            'classifier__n_estimators': [10, 50, 100],
            'classifier__max_depth': [None, 10, 20, 30]
        }
        
        # Perform GridSearchCV
        grid_search = GridSearchCV(pipeline, param_grid, cv=5)
        grid_search.fit(X, y)
        
        # Display best parameters and results
        print("Best Parameters:", grid_search.best_params_)
        print("Grid Search Results:", grid_search.cv_results_)
        """)
        
        # Combine Multiple Pipelines
        st.info("**Combine Multi Pipeline**")
        st.write("You can also combine multiple pipelines to create a more complex workflow, like processing different parts of the data with separate pipelines.")
        st.write("**Code:**")
        st.code("""
        from sklearn.pipeline import Pipeline,FeatureUnion
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import GridSearchCV
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImpute
        from sklearn_features.transformers import DataFrameSelector
        from sklearn.preprocessing import OneHotEncoder

        # Define separate pipelines for numerical and categorical features
        numerical_pipeline = Pipeline([
            ('selector', DataFrameSelector(columns=['numerical'])),
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_pipeline = Pipeline([
            ('selector', DataFrameSelector(columns=['categorical'])),
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder())
        ])
        
        # Combine pipelines using ColumnTransformer
        preprocessor = ColumnTransformer([
            ('numerical', numerical_pipeline, ['numerical']),
            ('categorical', categorical_pipeline, ['categorical'])
        ])
        
        # Complete pipeline combining preprocessing and classifier
        pipeline = FeatureUnion(transformer_list=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100))
        ])
        
        # Define the hyperparameter grid for GridSearchCV
        param_grid = {
            'classifier__max_depth': [None, 10, 20],
            'classifier__n_estimators': [50, 100],
        }
        
        grid_search = GridSearchCV(pipeline, param_grid, cv=5)
        grid_search.fit(X, y)
        
        # Display the best parameters and results
        print("Best Parameters:", grid_search.best_params_)
        print("Grid Search Results:", grid_search.cv_results_)
        """)
        

    st.success(f"{option} Hyperparameter Tuning implementation details displayed successfully!")