import streamlit as st
from streamlit_option_menu import option_menu
from helper_functions import display_dataset_info, data_cleaning, Preprocessing
from regreesion_functions import Regression_Models, Regression_Check
from classification_functions import Classification_models,Classification_Check
from cross_validation import Cross_Validation,Hyperparameter_Tuning
from unsupervised_models import unsupervised_models,Evaluation
# Set page configuration
st.set_page_config(
    page_title="Sklearn for ML",
    page_icon="🧠",
    layout="centered",
)

# Sidebar with navigation menu
with st.sidebar:
    selected = option_menu('Sklearn Content',
                           ['Dataset',
                            'Data Cleaning',
                            'Preprocessing',
                            'Regression',
                            'Regression Check',
                            'Classification',
                            'Classification Check',
                            'Cross Validation',
                            'Hyperparameter Tuning',
                            'Unsupervised Models',
                            'Unsupervised Check'],
                           default_index=0,
                           menu_icon="cast",
                           orientation="vertical",
                           styles={
                               "container": {"padding": "5px", "background-color": "#f0f2f6"},
                               "icon": {"color": "blue", "font-size": "20px"},
                               "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "padding": "10px"},
                               "nav-link-selected": {"background-color": "#3e8ef7"},
                           })

# Apply custom CSS to change selectbox color
st.markdown("""
    <style>
        /* Style the selectbox container */
        .stSelectbox {
            background-color: #e1f5fe;
            border-radius: 5px;
            color: #0277bd;  /* Color for text inside the selectbox */
        }

        /* Style the select dropdown options */
        .stSelectbox select {
            background-color: #e1f5fe;
            color: #0277bd;  /* Color for text in options */
            border: 1px solid #0288d1;
            font-family: 'Arial', sans-serif;
        }

        .stSelectbox select option {
            background-color: #b3e5fc;  /* Light blue background for options */
            color: #01579b;  /* Dark blue text color for options */
        }

        /* Highlight the selected option */
        .stSelectbox select option:checked {
            background-color: #81d4fa;  /* Lighter blue for selected option */
            color: #01579b;
        }

        /* Change color of the selected option's text */
        .stSelectbox select:focus {
            color: #0288d1;  /* Change color of text when the selectbox is focused */
        }
    </style>
""", unsafe_allow_html=True)

# Nested menu logic for Data Cleaning
if selected == 'Dataset':
    dataset_option = st.selectbox('Sklearn Dataset Options',
                                  ['Iris data', 'Digits data', 'California Housing data', 'Wine data', 'Breast cancer data', 'Diabetes data',
                                   'Sample Regression', 'Sample Classification'],
                                  index=0, key="dataset_selectbox")
    display_dataset_info(dataset_option)

elif selected == 'Data Cleaning':
    cleaning_option = st.selectbox('Data Cleaning Options',
                                   ['Handling Missing Values', 'Handling Outliers'],
                                   index=0, key="data_cleaning_selectbox")
    if cleaning_option:
        data_cleaning(cleaning_option)

elif selected == 'Preprocessing':
    preprocessing_option = st.selectbox('Preprocessing Options',
                                       ['Transform Object Columns', 'Feature Selection', 'Scaling', 'Splitting Data', 'Data Balancing'],
                                       index=0, key="preprocessing_selectbox")
    if preprocessing_option:
        Preprocessing(preprocessing_option)

elif selected == 'Regression':
    # Regression Category Selection
    regression_category = st.selectbox('Select Regression Category',
                                      ['Linear Models', 'Tree-based Models', 'Ensemble Models', 'Kernel Models', 'Other Models'],
                                      key="regression_category_selectbox")

    if regression_category == 'Linear Models':
        regression_option = st.selectbox('Linear Regression Models',
                                         ['Linear Regression', 'SGD Regression', 'Lasso', 'Ridge', 'ElasticNet', 'ElasticNetCV', 'RidgeCV', 'LassoCV'],
                                         key="linear_models_selectbox")
    
    elif regression_category == 'Tree-based Models':
        regression_option = st.selectbox('Tree-based Regression Models',
                                         ['Random Forest Regressor', 'Decision Tree Regressor', 'Extra Trees Regressor', 'Gradient Boosting Regressor',
                                          'Hist Gradient Boosting Regressor', 'Bagging Regressor', 'Stacking Regressor'],
                                         key="tree_based_models_selectbox")
    
    elif regression_category == 'Ensemble Models':
        regression_option = st.selectbox('Ensemble Regression Models',
                                         ['AdaBoost Regressor', 'XGB Regressor', 'LGBM Regressor', 'CatBoost Regressor', 'Voting Regressor'],
                                         key="ensemble_models_selectbox")

    elif regression_category == 'Kernel Models':
        regression_option = st.selectbox('Kernel Regression Models',
                                         ['SVR', 'Kernel Ridge', 'Gaussian Process Regressor'],
                                         key="kernel_models_selectbox")

    else:
        regression_option = st.selectbox('Other Regression Models',
                                         ['Isotonic Regression', 'Poisson Regressor', 'Tweedie Regressor', 'Nearest Centroid', 'LinearSVR', 
                                          'Huber Regressor', 'ARD Regression', 'Orthogonal Matching Pursuit', 'PassiveAggressive Regressor', 
                                          'Bayesian Ridge', 'Quantile Regressor', 'TheilSen Regressor', 'RANSAC Regressor', 'Logistic Regression'],
                                         key="other_models_selectbox")

    if regression_option:
        Regression_Models(regression_option)

elif selected == 'Regression Check':
    evaluation_option = st.selectbox('Evaluation Metrics',
                                    ['R2 Score', 'Mean Absolute Error', 'Mean Squared Error', 'Median Absolute Error',
                                     'Explained Variance Score', 'Max Error', 'Mean Squared Log Error',
                                     'Root Mean Squared Error', 'Huber Loss', 'Log-Cosh Loss', 'Logarithmic Loss (Log Loss)',
                                     'Poisson Loss'],
                                    index=0, key="evaluation_selectbox")
    if evaluation_option:
        Regression_Check(evaluation_option)

elif selected == 'Classification':
    classification_category = st.selectbox('Select Classification Category',
                                          ['Linear Models', 'Tree-based Models', 'Ensemble Models', 
                                           'Naive Bayes Models', 'Neural Networks', 'Other Models'],
                                          key="classification_category_selectbox")

    if classification_category == 'Linear Models':
        classification_option = st.selectbox('Linear Classification Models',
                                            ['Logistic Regression', 'Linear Discriminant Analysis (LDA)', 'Ridge Classifier', 
                                             'SGD Classifier (Stochastic Gradient Descent)'],
                                            key="linear_models_selectbox")
    
    elif classification_category == 'Tree-based Models':
        classification_option = st.selectbox('Tree-based Classification Models',
                                            ['Decision Tree Classifier', 'Random Forest Classifier', 'Gradient Boosting Classifier', 
                                             'XGBoost Classifier', 'LightGBM (LGBM) Classifier', 'CatBoost Classifier', 'ExtraTrees Classifier'],
                                            key="tree_based_models_selectbox")
    
    elif classification_category == 'Ensemble Models':
        classification_option = st.selectbox('Ensemble Classification Models',
                                            ['AdaBoost Classifier', 'Stacking Classifier', 'Voting Classifier'],
                                            key="ensemble_models_selectbox")

    elif classification_category == 'Naive Bayes Models':
        classification_option = st.selectbox('Naive Bayes Classification Models',
                                            ['Gaussian Naive Bayes Classifier', 'Multinomial Naive Bayes Classifier', 
                                             'Bernoulli Naive Bayes Classifier'],
                                            key="naive_bayes_models_selectbox")

    elif classification_category == 'Neural Networks':
        classification_option = st.selectbox('Neural Network Classification Models',
                                            ['Multilayer Perceptron (MLP) Classifier'],
                                            key="neural_networks_selectbox")

    else:
        classification_option = st.selectbox('Other Classification Models',
                                            ['OneVsRest Classifier', 'LinearSVC', 'RidgeClassifierCV', 'Quadratic Discriminant Analysis (QDA)', 
                                             'Logistic RegressionCV', 'Perceptron Classifier', 'Dummy Classifier'],
                                            key="other_classification_models_selectbox")

    if classification_option:
        Classification_models(classification_option)

elif selected == 'Classification Check':
    classification_check_option = st.selectbox('Evaluation Metrics',
                                            ['Accuracy Score', 'Recall Score', 'Precision Score', 'F1 Score',
                                             'Precision-Recall Curve', 'Precision-Recall-F1 Score Support',
                                            'Zero-One Loss','Confusion Matrix', 'Classification Report', 'AUC', 'ROC Curve', 
                                             'ROC AUC Score', 'Log Loss', 'Matthews Correlation Coefficient (MCC)',
                                             'Cohen’s Kappa', 'Brier Score', 'Balanced Accuracy', 'Hamming Loss',
                                             'Top-k Accuracy', 'Specificity', 'True Positive Rate (TPR)', 
                                             'False Positive Rate (FPR)', 'False Discovery Rate (FDR)'],
                                            index=0, key="classification_check_selectbox")
    if classification_check_option:
        Classification_Check(classification_check_option)

elif selected == 'Cross Validation':
    validation_option = st.selectbox('Cross Validation Options',
                                     ['Cross Validate', 'Cross Validate Predict', 'Cross Validate Score',"TunedThresholdClassifierCV"],
                                     index=0, key="cross_validation_selectbox")
    if validation_option:
        Cross_Validation(validation_option)
elif selected == 'Hyperparameter Tuning':
    tuning_option = st.selectbox('Hyperparameter Tuning Options',
                                 ['Grid Searching', 'Randomized Grid Searching', 'Pipeline'],
                                 index=0, key="hyperparameter_tuning_selectbox")
    if tuning_option:
        Hyperparameter_Tuning(tuning_option)
elif selected == 'Unsupervised Models':
    unsupervised_option = st.selectbox('Unsupervised Models',
                                       ['KMeans', 'MiniBatchKMeans', 'Hierarchical Clustering', 'DBSCAN',
                                        "LatentDirichletAllocation","GaussianMixture", 'Dimensionality Reduction'],
                                       index=0, key="unsupervised_models_selectbox")
    if unsupervised_option:
        unsupervised_models(unsupervised_option)
elif selected == "Unsupervised Check":
    check_option = st.selectbox('Evaluation Metrics',
                                    ['Silhouette Score', 'Davies-Bouldin Index', 'Dimensionality Reduction Evaluation'],
                                    index=0, key="unsupervised_check_selectbox")
    if check_option:
        Evaluation(check_option)