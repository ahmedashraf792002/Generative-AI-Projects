import streamlit as st

def Classification_models(option):
    if option == "Logistic Regression":
        st.write("### Logistic Regression")
        st.write("Logistic Regression is a linear model for binary classification tasks.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import LogisticRegression

                model = LogisticRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`solver`: Algorithm to use in the optimization process.\n`C`: Regularization strength.")

    elif option == "K-Nearest Neighbors (KNN) Classifier":
        st.write("### K-Nearest Neighbors (KNN) Classifier")
        st.write("KNN is a non-parametric classifier that uses a distance metric to classify data.")
        st.write("**Code:**")
        st.code("""
                from sklearn.neighbors import KNeighborsClassifier

                model = KNeighborsClassifier(n_neighbors=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`n_neighbors`: Number of neighbors to use.\n`weights`: Weight function used in prediction.")

    elif option == "Support Vector Machine (SVM) Classifier":
        st.write("### Support Vector Machine (SVM) Classifier")
        st.write("SVM is a powerful classifier for both linear and non-linear data.")
        st.write("**Code:**")
        st.code("""
                from sklearn.svm import SVC

                model = SVC(kernel='linear')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`kernel`: Type of kernel to use.\n`C`: Regularization parameter.")

    elif option == "Decision Tree Classifier":
        st.write("### Decision Tree Classifier")
        st.write("A decision tree is a tree-like structure that splits data based on feature values.")
        st.write("**Code:**")
        st.code("""
                from sklearn.tree import DecisionTreeClassifier

                model = DecisionTreeClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`max_depth`: Maximum depth of the tree.\n`min_samples_split`: Minimum samples required to split a node.")

    elif option == "Random Forest Classifier":
        st.write("### Random Forest Classifier")
        st.write("Random Forest is an ensemble method that uses multiple decision trees.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import RandomForestClassifier

                model = RandomForestClassifier(n_estimators=100)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of trees in the forest.\n`max_depth`: Maximum depth of each tree.")

    elif option == "Gradient Boosting Classifier":
        st.write("### Gradient Boosting Classifier")
        st.write("Gradient Boosting builds trees sequentially, where each tree corrects the errors of the previous one.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import GradientBoostingClassifier

                model = GradientBoostingClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of boosting stages.\n`learning_rate`: Step size at each iteration.")

    elif option == "XGBoost Classifier":
        st.write("### XGBoost Classifier")
        st.write("XGBoost is an optimized gradient boosting algorithm designed for performance.")
        st.write("**Code:**")
        st.code("""
                from xgboost import XGBClassifier

                model = XGBClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`learning_rate`: Step size for each boosting round.\n`n_estimators`: Number of boosting rounds.")

    elif option == "LightGBM (LGBM) Classifier":
        st.write("### LightGBM (LGBM) Classifier")
        st.write("LightGBM is an efficient gradient boosting framework with faster training.")
        st.write("**Code:**")
        st.code("""
                from lightgbm import LGBMClassifier

                model = LGBMClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`num_leaves`: Maximum number of leaves in one tree.\n`n_estimators`: Number of boosting rounds.")

    elif option == "CatBoost Classifier":
        st.write("### CatBoost Classifier")
        st.write("CatBoost is a gradient boosting library designed for categorical feature handling.")
        st.write("**Code:**")
        st.code("""
                from catboost import CatBoostClassifier

                model = CatBoostClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`iterations`: Number of boosting iterations.\n`learning_rate`: Step size at each iteration.")

    # Naive Bayes classifiers
    elif option == "Gaussian Naive Bayes Classifier":
        st.write("### Gaussian Naive Bayes")
        st.write("Gaussian Naive Bayes is used for classification tasks with continuous data that follows a normal distribution.")
        st.write("**Code:**")
        st.code("""
                from sklearn.naive_bayes import GaussianNB
                model = GaussianNB()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`var_smoothing`: Portion of the largest variance added to the variance.")

    elif option == "Multinomial Naive Bayes Classifier":
        st.write("### Multinomial Naive Bayes")
        st.write("Multinomial Naive Bayes is suitable for classification with discrete counts (e.g., text classification).")
        st.write("**Code:**")
        st.code("""
                from sklearn.naive_bayes import MultinomialNB
                model = MultinomialNB()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Smoothing parameter.\n`fit_prior`: Whether to learn class prior probabilities.")

    elif option == "Bernoulli Naive Bayes Classifier":
        st.write("### Bernoulli Naive Bayes")
        st.write("Bernoulli Naive Bayes is used for binary/boolean features (e.g., presence or absence of a word in text).")
        st.write("**Code:**")
        st.code("""
                from sklearn.naive_bayes import BernoulliNB
                model = BernoulliNB()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Smoothing parameter.\n`binarize`: Threshold for binarizing the feature values.")

    elif option == "Multilayer Perceptron (MLP) Classifier":
        st.write("### Multilayer Perceptron (MLP) Classifier")
        st.write("MLP is a type of neural network model that can learn complex patterns.")
        st.write("**Code:**")
        st.code("""
                from sklearn.neural_network import MLPClassifier

                model = MLPClassifier(hidden_layer_sizes=(100,))
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`hidden_layer_sizes`: Number of neurons in the hidden layers.\n`activation`: Activation function.")
    elif option == "AdaBoost Classifier":
        st.write("### AdaBoost Classifier")
        st.write("AdaBoost is an ensemble method that combines weak learners to improve the overall model performance.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import AdaBoostClassifier
                model = AdaBoostClassifier(n_estimators=50)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: The number of base estimators.\n`learning_rate`: The learning rate shrinks the contribution of each classifier.")

    elif option == "Stacking Classifier":
        st.write("### Stacking Classifier")
        st.write("Stacking combines predictions of multiple models to improve the accuracy by training a meta-model.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import StackingClassifier
                from sklearn.linear_model import LogisticRegression
                from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
                
                base_learners = [
                    ('rf', RandomForestClassifier(n_estimators=100)),
                    ('gb', GradientBoostingClassifier(n_estimators=100))
                ]
                model = StackingClassifier(estimators=base_learners, final_estimator=LogisticRegression())
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`estimators`: A list of base learners.\n`final_estimator`: The final classifier that aggregates predictions from base learners.")

    elif option == "Voting Classifier":
        st.write("### Voting Classifier")
        st.write("Voting Classifier combines multiple models by voting (majority or weighted) on the class prediction.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import VotingClassifier
                from sklearn.linear_model import LogisticRegression
                from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
                
                model = VotingClassifier(estimators=[
                    ('lr', LogisticRegression()),
                    ('rf', RandomForestClassifier(n_estimators=100)),
                    ('gb', GradientBoostingClassifier(n_estimators=100))
                ], voting='hard')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`voting`: The voting strategy ('hard' or 'soft').\n`estimators`: A list of base classifiers.")

    elif option == "ExtraTrees Classifier":
        st.write("### ExtraTrees Classifier")
        st.write("ExtraTrees is an ensemble method similar to Random Forest but it uses a more randomized approach to create decision trees.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import ExtraTreesClassifier
                model = ExtraTreesClassifier(n_estimators=100)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`n_estimators`: Number of trees in the forest.\n`max_depth`: Maximum depth of each tree.")

    elif option == "Linear Discriminant Analysis (LDA)":
        st.write("### Linear Discriminant Analysis (LDA)")
        st.write("LDA is a linear classifier used for dimensionality reduction and classification.")
        st.write("**Code:**")
        st.code("""
                from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
                model = LinearDiscriminantAnalysis()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`solver`: Algorithm used for optimization.\n`priors`: Class prior probabilities.")

    elif option == "Quadratic Discriminant Analysis (QDA)":
        st.write("### Quadratic Discriminant Analysis (QDA)")
        st.write("QDA is similar to LDA but assumes that each class has its own covariance matrix.")
        st.write("**Code:**")
        st.code("""
                from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
                model = QuadraticDiscriminantAnalysis()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`reg_param`: Regularization parameter.\n`priors`: Class prior probabilities.")

    elif option == "Ridge Classifier":
        st.write("### Ridge Classifier")
        st.write("Ridge Classifier uses regularization to prevent overfitting by penalizing large coefficients in the model.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import RidgeClassifier
                model = RidgeClassifier(alpha=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")

    elif option == "SGD Classifier (Stochastic Gradient Descent)":
        st.write("### SGD Classifier (Stochastic Gradient Descent)")
        st.write("SGD is an optimization technique used for training large-scale linear classifiers.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import SGDClassifier
                model = SGDClassifier(loss='log', max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`loss`: The loss function to use.\n`max_iter`: The maximum number of iterations for optimization.")
    elif option == "OneVsRest Classifier":
        st.write("### OneVsRest Classifier")
        st.write("OneVsRest transforms the multi-class problem into multiple binary classification problems.")
        st.write("**Code:**")
        st.code("""
                from sklearn.multiclass import OneVsRestClassifier
                from sklearn.linear_model import LogisticRegression
                
                model = OneVsRestClassifier(LogisticRegression())
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`estimator`: The base classifier to use for each binary classification.")

    elif option == "Bagging Classifier":
        st.write("### Bagging Classifier")
        st.write("Bagging Classifier is an ensemble method that builds multiple models and combines their results to improve the overall performance.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import BaggingClassifier
                from sklearn.tree import DecisionTreeClassifier
                
                model = BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=50)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`base_estimator`: The model used to generate individual predictions.\n`n_estimators`: The number of models to combine.")

    elif option == "Histogram-based Gradient Boosting Classifier":
        st.write("### Histogram-based Gradient Boosting Classifier")
        st.write("A faster variant of gradient boosting, especially for large datasets.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import HistGradientBoostingClassifier
                
                model = HistGradientBoostingClassifier(max_iter=100)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: The number of boosting iterations.\n`learning_rate`: The learning rate for boosting.")

    elif option == "Isotonic Regression":
        st.write("### Isotonic Regression")
        st.write("Isotonic regression is used for fitting non-decreasing regression models, but can also be used for classification tasks.")
        st.write("**Code:**")
        st.code("""
                from sklearn.isotonic import IsotonicRegression
                
                model = IsotonicRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`increasing`: Whether to constrain the regression to be increasing.")

    elif option == "Huber Classifier":
        st.write("### Huber Classifier")
        st.write("Huber Classifier is used for robust regression and classification tasks, especially when there are outliers in the data.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import HuberClassifier
                
                model = HuberClassifier()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`epsilon`: The threshold for classifying outliers.\n`alpha`: The regularization strength.")

    elif option == "Nearest Centroid Classifier":
        st.write("### Nearest Centroid Classifier")
        st.write("This classifier predicts the class of a data point based on the nearest centroid.")
        st.write("**Code:**")
        st.code("""
                from sklearn.neighbors import NearestCentroid
                
                model = NearestCentroid()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`metric`: The distance metric to use.\n`shrink_threshold`: Threshold for shrinking the centroid.")

    elif option == "Passive-Aggressive Classifier":
        st.write("### Passive-Aggressive Classifier")
        st.write("A linear classifier that is efficient and works well for large-scale data and online learning.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import PassiveAggressiveClassifier
                
                model = PassiveAggressiveClassifier(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum number of iterations.\n`C`: Regularization strength.")

    elif option == "Perceptron Classifier":
        st.write("### Perceptron Classifier")
        st.write("Perceptron is a simple neural network model used for classification tasks.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import Perceptron
                
                model = Perceptron()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`max_iter`: Maximum number of iterations.\n`eta0`: Learning rate.")

    elif option == "Logistic RegressionCV":
        st.write("### Logistic RegressionCV")
        st.write("Logistic Regression with built-in cross-validation to automatically select the best regularization parameter.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import LogisticRegressionCV
                
                model = LogisticRegressionCV(cv=5, max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`cv`: Number of cross-validation folds.\n`max_iter`: Maximum number of iterations.")

    elif option == "RidgeClassifierCV":
        st.write("### Ridge ClassifierCV")
        st.write("Ridge Classifier with built-in cross-validation to automatically select the best regularization parameter.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import RidgeClassifierCV
                
                model = RidgeClassifierCV(cv=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`cv`: Number of cross-validation folds.")

    elif option == "Lasso Classifier":
        st.write("### Lasso Classifier")
        st.write("Lasso Classifier applies L1 regularization to the logistic regression model to prevent overfitting.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import Lasso
                
                model = Lasso(alpha=1.0)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.")

    elif option == "ElasticNet Classifier":
        st.write("### ElasticNet Classifier")
        st.write("ElasticNet is a linear classifier that combines both L1 and L2 regularization.")
        st.write("**Code:**")
        st.code("""
                from sklearn.linear_model import ElasticNet
                
                model = ElasticNet(alpha=1.0, l1_ratio=0.5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`alpha`: Regularization strength.\n`l1_ratio`: The ratio between L1 and L2 regularization.")

    elif option == "QDA (Quadratic Discriminant Analysis)":
        st.write("### Quadratic Discriminant Analysis (QDA)")
        st.write("QDA assumes that each class has its own covariance matrix, unlike LDA (Linear Discriminant Analysis) which assumes a shared covariance matrix.")
        st.write("**Code:**")
        st.code("""
                from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
                
                model = QuadraticDiscriminantAnalysis()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`priors`: The class prior probabilities.\n`reg_param`: Regularization parameter.")

    elif option == "RandomPatches Classifier":
        st.write("### RandomPatches Classifier")
        st.write("RandomPatches generates random patches from the training data and uses them to train a classifier.")
        st.write("**Code:**")
        st.code("""
                from sklearn.ensemble import RandomPatchesClassifier
                from sklearn.tree import DecisionTreeClassifier
                
                model = RandomPatchesClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=10)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
        """)
        st.info("**Hyperparameters:**")
        st.write("`base_estimator`: The classifier used to train on random subsets.\n`n_estimators`: Number of estimators to use.")
        
    st.success(f"{option} model implementation details displayed successfully!")


def Classification_Check(option):
    if option == "Accuracy Score":
        st.write("### Accuracy Score")
        st.write("Accuracy Score is the proportion of correctly predicted instances out of the total instances.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import accuracy_score

        # Assuming y_test and y_pred are already defined
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy Score:", accuracy)
        """)

    elif option == "Recall Score":
        st.write("### Recall Score")
        st.write("Recall (True Positive Rate) is the proportion of actual positives that were correctly identified.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import recall_score

        # Assuming y_test and y_pred are already defined
        recall = recall_score(y_test, y_pred, average='binary')
        print("Recall Score:", recall)
        """)

    elif option == "Precision Score":
        st.write("### Precision Score")
        st.write("Precision is the proportion of positive predictions that are actually correct.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import precision_score

        # Assuming y_test and y_pred are already defined
        precision = precision_score(y_test, y_pred, average='binary')
        print("Precision Score:", precision)
        """)

    elif option == "F1 Score":
        st.write("### F1 Score")
        st.write("F1 Score is the harmonic mean of Precision and Recall. It balances the two metrics.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import f1_score

        # Assuming y_test and y_pred are already defined
        f1 = f1_score(y_test, y_pred, average='binary')
        print("F1 Score:", f1)
        """)
    elif option == "Precision-Recall Curve":
        st.write("### Precision-Recall Curve")
        st.write("The Precision-Recall Curve shows the trade-off between precision and recall for different thresholds.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import precision_recall_curve
        import matplotlib.pyplot as plt

        # Assuming y_test and y_pred_proba are already defined
        precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
        plt.plot(recall, precision)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.show()
        """)

    elif option == "Precision-Recall-F1 Score Support":
        st.write("### Precision-Recall-F1 Score Support")
        st.write("The `precision_recall_fscore_support` function provides precision, recall, F1-score, and support for each class.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import precision_recall_fscore_support

        # Assuming y_test and y_pred are already defined
        precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)
        print("Support:", support)
        """)

    elif option == "Zero-One Loss":
        st.write("### Zero-One Loss")
        st.write("Zero-One Loss calculates the fraction of predictions that do not match the true labels. It is useful for multi-class problems.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import zero_one_loss

        # Assuming y_test and y_pred are already defined
        zero_one = zero_one_loss(y_test, y_pred)
        print("Zero-One Loss:", zero_one)
        """)


    elif option == "Confusion Matrix":
        st.write("### Confusion Matrix")
        st.write("The confusion matrix displays the count of actual vs predicted classifications.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import confusion_matrix

        # Assuming y_test and y_pred are already defined
        cm = confusion_matrix(y_test, y_pred)
        print("Confusion Matrix:\n", cm)
        """)

    elif option == "Classification Report":
        st.write("### Classification Report")
        st.write("The classification report provides key metrics like precision, recall, and F1 score for each class.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import classification_report

        # Assuming y_test and y_pred are already defined
        report = classification_report(y_test, y_pred)
        print("Classification Report:\n", report)
        """)

    elif option == "AUC":
        st.write("### AUC")
        st.write("AUC (Area Under the Curve) measures the area under the ROC curve, indicating the model's ability to distinguish between classes.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import roc_auc_score

        # Assuming y_test and y_pred_proba are already defined
        auc = roc_auc_score(y_test, y_pred_proba)
        print("AUC:", auc)
        """)

    elif option == "ROC Curve":
        st.write("### ROC Curve")
        st.write("The ROC Curve plots the True Positive Rate against the False Positive Rate at various threshold settings.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import roc_curve
        import matplotlib.pyplot as plt

        # Assuming y_test and y_pred_proba are already defined
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        plt.plot(fpr, tpr)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.show()
        """)

    elif option == "ROC AUC Score":
        st.write("### ROC AUC Score")
        st.write("The ROC AUC Score provides a single metric that combines the performance of a model across all thresholds.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import roc_auc_score

        # Assuming y_test and y_pred_proba are already defined
        auc_score = roc_auc_score(y_test, y_pred_proba)
        print("ROC AUC Score:", auc_score)
        """)

    elif option == "Log Loss":
        st.write("### Log Loss")
        st.write("Log Loss evaluates the performance of a classification model where the output is a probability value between 0 and 1.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import log_loss

        # Assuming y_test and y_pred_proba are already defined
        loss = log_loss(y_test, y_pred_proba)
        print("Log Loss:", loss)
        """)

    elif option == "Matthews Correlation Coefficient (MCC)":
        st.write("### Matthews Correlation Coefficient (MCC)")
        st.write("MCC is a measure of the quality of binary (two-class) classifications. It takes into account true and false positives and negatives.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import matthews_corrcoef

        # Assuming y_test and y_pred are already defined
        mcc = matthews_corrcoef(y_test, y_pred)
        print("Matthews Correlation Coefficient:", mcc)
        """)

    elif option == "Cohen’s Kappa":
        st.write("### Cohen’s Kappa")
        st.write("Cohen's Kappa measures inter-rater agreement and is useful for categorical classifications.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import cohen_kappa_score

        # Assuming y_test and y_pred are already defined
        kappa = cohen_kappa_score(y_test, y_pred)
        print("Cohen's Kappa:", kappa)
        """)

    elif option == "Brier Score":
        st.write("### Brier Score")
        st.write("The Brier Score measures the mean squared error between predicted probabilities and the actual binary outcomes.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import brier_score_loss

        # Assuming y_test and y_pred_proba are already defined
        brier_score = brier_score_loss(y_test, y_pred_proba)
        print("Brier Score:", brier_score)
        """)

    elif option == "Balanced Accuracy":
        st.write("### Balanced Accuracy")
        st.write("Balanced Accuracy calculates the average of recall obtained on each class, which is useful for imbalanced datasets.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import balanced_accuracy_score

        # Assuming y_test and y_pred are already defined
        balanced_acc = balanced_accuracy_score(y_test, y_pred)
        print("Balanced Accuracy:", balanced_acc)
        """)

    elif option == "Hamming Loss":
        st.write("### Hamming Loss")
        st.write("Hamming Loss calculates the fraction of incorrect labels to the total number of labels.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import hamming_loss

        # Assuming y_test and y_pred are already defined
        hamming = hamming_loss(y_test, y_pred)
        print("Hamming Loss:", hamming)
        """)

    elif option == "Top-k Accuracy":
        st.write("### Top-k Accuracy")
        st.write("Top-k Accuracy measures the proportion of times the true label is within the top-k predicted labels.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import top_k_accuracy_score

        # Assuming y_test and y_pred_proba are already defined
        top_k_acc = top_k_accuracy_score(y_test, y_pred_proba, k=3)
        print("Top-k Accuracy:", top_k_acc)
        """)

    elif option == "Specificity":
        st.write("### Specificity")
        st.write("Specificity (True Negative Rate) measures the proportion of actual negatives that were correctly identified.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import recall_score

        # Assuming y_test and y_pred are already defined
        specificity = recall_score(y_test, y_pred, average='binary', pos_label=0)
        print("Specificity:", specificity)
        """)

    elif option == "True Positive Rate (TPR)":
        st.write("### True Positive Rate (TPR)")
        st.write("True Positive Rate (Recall) is the proportion of actual positives that were correctly identified.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import recall_score

        # Assuming y_test and y_pred are already defined
        tpr = recall_score(y_test, y_pred, average='binary')
        print("True Positive Rate (TPR):", tpr)
        """)

    elif option == "False Positive Rate (FPR)":
        st.write("### False Positive Rate (FPR)")
        st.write("False Positive Rate measures the proportion of actual negatives that were incorrectly classified as positive.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import confusion_matrix

        # Assuming y_test and y_pred are already defined
        cm = confusion_matrix(y_test, y_pred)
        fpr = cm[0, 1] / (cm[0, 1] + cm[0, 0])
        print("False Positive Rate (FPR):", fpr)
        """)

    elif option == "False Discovery Rate (FDR)":
        st.write("### False Discovery Rate (FDR)")
        st.write("False Discovery Rate measures the proportion of positive predictions that were incorrectly classified.")
        st.write("**Code:**")
        st.code("""
        from sklearn.metrics import confusion_matrix

        # Assuming y_test and y_pred are already defined
        cm = confusion_matrix(y_test, y_pred)
        fdr = cm[0, 1] / (cm[0, 1] + cm[1, 1])
        print("False Discovery Rate (FDR):", fdr)
        """)

    st.success(f"{option} model Evaluation implementation details displayed successfully!")
