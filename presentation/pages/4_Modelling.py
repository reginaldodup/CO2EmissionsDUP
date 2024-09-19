from pathlib import Path
import os
import sys
import pickle

import streamlit as st
import pandas as pd

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

modelling_dir = os.path.join(notebooks_dir, "_Step3_Modelling")

clean_data = os.path.join(data_dir, "2-cleaned", "data_phase_2.csv")
df_clean = pd.read_csv(clean_data)

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")

# Load Data (only test is required as train already used to fit model)
file_path = os.path.join(modelling_dir, "data", "X_test.pkl")
with open(file_path, "rb") as f:
    X_test = pickle.load(f)
file_path = os.path.join(modelling_dir, "data", "y_test.pkl")
with open(file_path, "rb") as f:
    y_test = pickle.load(f)


st.write("# Modelling")
tab1, tab2 = st.tabs(["Linear Regression", "Classification"])
# -----------------------------------------
# REGRESSION
# -----------------------------------------
with tab1:
    st.write("## Problem Definition")
    with st.expander("Definition "):
        st.markdown(
            r"""
The Multiple Linear Regression consists in modelling a relation between the **target variable $y$ (CO2 emission)** and **multiple explanatory variables $x_p$**: 

$$y_i=β_0+β_1x_{i,1}+β_2x_{i,2}+⋯+β_px_{i,p}+ε_i$$

where:

* $y$ is the `CO2 emission`,  
* $x_p$ are a continuous qualitative variables,
* $β_p$ are the linear regression coefficients,
* $ε$ is a random error term that follows the normal distribution of zero mean and standard deviation σ.

The regression model will estimate the coefficients $β_p$.
 
Residues are defined by $ε = y - \tilde{y}$.

Regularized Linear Regressions are also used in this study, for details refer to Notebook MASTER_Linear Regression under _Step3_Modelling folder in our github. 
"""
        )

    st.write("## Performance Criteria")
    with st.expander("Definition"):
        st.markdown(r"""
The evaluation of the regression model is done by using 4 metrics:
                    
* Mean Squared Error (MSE):""") 
        st.latex(r'''MSE =
            \frac{1}n
            \sum
            \left(y - \hat{y}\right)^{2}
            ''')

        st.markdown(r"""* Mean Absolute Error (MAE):""") 
        st.latex(r'''MAE =
            \frac{1}n
            \sum
            \lvert(y - \hat{y}\rvert)
            ''')

        st.markdown(r"""* Root Mean Square Error (RMSE):""") 
        st.latex(r'''RMSE =
            \sqrt{
            \frac{1}n
            \sum
            \left(y - \hat{y}\right)^{2}}
            ''')
        
        st.markdown(r"""* R-squared Value""")

    st.write("## Preparation of the Dataset for the Linear Regression")
    with st.expander("Prepation of the Dataset"):
        st.markdown(r"""
        The first step consist in transforming the qualitative variables into a dummy variables to be able to use it. To do that, the function **get_dummies** is used. The function has been applied to fourth variables:
        
        * cod_cbr (type of fuel)
        * Hybrid (Yes/No)
        * Type of Gearbox
        * Number of reports on the gearbox            
                    
        This transformation allows to go from **4 categorical variables to 31 dummy variables**. After removing the target vartiables, **the dataset contains 38 variables**.

        The second step consist in separating the dataset into a training and a test set. In this case, we are not able to use **the train_test_split function** because it has no sense to use the values from the year 2015 to predict dat from earler year.
        Typically, the test set represents between 20% and 30% of the dataset. Let's observe the proportion of the year in our dataset:
                    
        """)

        df_repart = pd.DataFrame(df_clean["year"].value_counts(normalize=True))
        df_repart = df_repart.sort_values(by = ['year'])
        df_repart["proportion"] = [f"{p:.1%}" for p in df_repart.proportion]
        
        st.code(df_repart)
        st.markdown(r""" 
        
        The last year 2015 represents almost 20% of our dataset. Therefore all the data from the year 2015 is used for the test set and the others years are used for the train set.
        
        Finally, the training set and test set are standardized using **the function StandardScaler**. The scaler is fitted on the training set and then transform the training set and the test set.
                    
        """)

    simple_lr_dict = {
        "Linear Regression (Standard Scaler)": {
            "model": "0-Linear Regression (Standard Scaler).pkl",
            "fig": "0-Linear Regression (Standard Scaler).pkl",
        },
        "Linear Regression (Robust Scaler)": {
            "model": "0-Linear Regression (Robust Scaler).pkl",
            "fig": "0-Linear Regression (Robust Scaler).pkl",
        },
    }

    st.write("## Simple Linear Regression")
    with st.expander("Simple Linear Regression"):
        opts0 = [key for key in simple_lr_dict]
        opt0 = st.selectbox("Select the model you want to check:", opts0)
        # Load result Graph
        file_path = os.path.join(
            modelling_dir,
            "imgs",
            simple_lr_dict[opt0]["fig"],
        )
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Results Summary
        file_path = os.path.join(
            modelling_dir,
            "models",
            simple_lr_dict[opt0]["model"],
        )
        with open(file_path, "rb") as f:
            result = pickle.load(f)
        st.write(result)

    # Penalized Linear Regression dict
    pen_lr_dict = {
        "Lasso": {
            "model": "0-Lasso.pkl",
            "fig": "0-Lasso Regression (alpha=1).pkl",
            "result": "0-Results Lasso Regression.pkl",
        },
        "LassoCV": {
            "model": "0-LassoCV.pkl",
            "fig": "0-LassoCV (best alpha).pkl",
            "result": "0-Results LassoCV.pkl",
        },
        "RidgeCV": {
            "model": "0-RidgeCV.pkl",
            "fig": "0-Ridge Regression.pkl",
            "result": "0-Results RidgeCV.pkl",
        },
        "ElasticNetCV": {
            "model": "0-ElasticNetCV.pkl",
            "fig": "0-ElasticNetCV (best alpha).pkl",
            "result": "0-Result ElasticNetCV.pkl",
        },
        "RESULT SUMMARY": {
            "model": "0-RidgeCV.pkl",
            "fig": "0-Regression Models Results Summary.pkl",
            "result": "0-Results RidgeCV.pkl",
        },
    }

    st.write("## Regularized Linear Regression")
    with st.expander("Regularized Linear Regression"):
        opts1 = [key for key in pen_lr_dict]
        opt1 = st.selectbox("Select the model you want to check:", opts1)
        # Load result Graph
        file_path = os.path.join(
            modelling_dir,
            "imgs",
            pen_lr_dict[opt1]["fig"],
        )
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        # Params
        file_path = os.path.join(
            modelling_dir,
            "models",
            pen_lr_dict[opt1]["model"],
        )
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        col1.write("### Parameters")
        col1.write(model.get_params())
        # Results Summary
        file_path = os.path.join(
            modelling_dir,
            "models",
            pen_lr_dict[opt1]["result"],
        )
        with open(file_path, "rb") as f:
            result = pickle.load(f)
        col2.write("### Results")
        col2.write(result)
        col3.write("### Alpha")
        if opt1 == opts1[0]:
            col3.write(model.get_params()["alpha"])
        else:
            col3.write(model.alpha_)


# -----------------------------------------
# CLASSIFICATION
# -----------------------------------------
with tab2:
    st.write("## Classification Problem Definition")
    with st.expander("Definition"):
        st.markdown(
            r"""
 For this study we separate the CO2 emissions in 4 classes:
 - `0` : Low < Q1
 - `1` : Medium > Q1; <= Q2
 - `3` : High > Q2; <= Q3
 - `4` : Very High > Q3

```python
target  = pd.cut(
    target,
    bins = [0, 163, 202, 216, 572],
    labels = [0, 1, 2, 3]
)
```

 The objective of the model is then recognize each class correctly based on vehicle caracteristics.
"""
        )

    st.write("## Performance Criteria")
    with st.expander("Definition"):
        col1, col2 = st.columns(2)
        col1.markdown("""
#### Confusion Matrix
- True Positives (TP): Number of samples correctly predicted as ‘positive’. 
- False Positives (FP): Number of samples wrongly predicted as ‘positive’. 
- True Negatives (TN): Number of samples correctly predicted as ‘negative’. 
- False Negatives (FN): Number of samples wrongly predicted as ‘negative’. 

| -    | +ve  | -ve  |
| ---- | ---- | ---- |
| +ve  | TP   | FP   |
| -ve  | FN   | TN   |
        """)
        
        col2.markdown("""
#### Accuracy
The accuracy metric computes how many times a model made a correct prediction across the entire dataset. This can be a reliable metric only if the dataset is class-balanced; that is, each class of the dataset has the same number of samples.

#### Recall
Recall measures how many of the positive class samples present in the dataset were correctly identified by the model.

$$ Recall = {TP \over TP + FN} $$

#### F1 Score
The F1 score is calculated as the harmonic mean of the precision and recall scores, as shown below. It ranges from
0-100%, and a higher F1 score denotes a better-quality classifier.

$$ F1 Score = {2 \over {{1 \over Precision} + {1 \over Recall}}} $$
        """)
        col1.markdown("""
#### Precision
Precision measures how many of the “positive” predictions made by the model were correct.

$$ Precision = {TP \over TP + FP} $$

        """)
    
    simple_models_dict = {
        "Logistic Regression": {
            "model": "2-Logistic Regression.pkl",
            "fig": "1-Logistic Regression Results.pkl",
        },
        "SVM": {"model": "2-SVM.pkl", "fig": "1-SVM Results.pkl"},
        "KNN": {"model": "2-KNN.pkl", "fig": "1-KNN Results.pkl"},
        "Decision Tree Classifier": {
            "model": "2-Decision Tree Classifier.pkl",
            "fig": "1-Decision Tree Results.pkl",
        },
        "RESULTS SUMMARY": {
            "model": "2-Decision Tree Classifier.pkl",
            "fig": "1-Results Summary Simple Classification.pkl",
        },
    }

    st.write("## Simple models")
    with st.expander("Simple Models"):
        options0 = [key for key in simple_models_dict]
        option0 = st.selectbox("Select the model you want to check:", options0)

        # Load result Graph
        file_path = os.path.join(
            modelling_dir, "imgs", simple_models_dict[option0]["fig"]
        )
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Load Model
        file_path = os.path.join(
            modelling_dir, "models", simple_models_dict[option0]["model"]
        )
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        # Display main results
        col1, col2, col3 = st.columns(3)
        y_pred = model.predict(X_test)
        cm = pd.crosstab(
            y_test,
            y_pred,
            rownames=["real"],
            colnames=["predicted"],
            # normalize='columns'
        )

        col1.write("### Confusion Matrix")
        col1.write(cm)

        col2.write("### Score")
        col2.write(model.score(X_test, y_test))

    boost_bagging_models_dict = {
        "AdaBoostClassifier": {
            "model": "2-AdaBoostClassifier.pkl",
            "fig": "1-Boosting Results.pkl",
        },
        "BaggingClassifier": {
            "model": "2-BaggingClassifier.pkl",
            "fig": "1-Bagging Results.pkl",
        },
        "RESULTS SUMMARY": {
            "model": "2-AdaBoostClassifier.pkl",
            "fig": "1-Results Summary Boosting and Bagging.pkl",
        },
    }

    st.write("## Boosting and Bagging")
    with st.expander("Boosting and Bagging"):
        options1 = [key for key in boost_bagging_models_dict]
        option1 = st.selectbox("Select the model you want to check:", options1)

        # Load result Graph
        file_path = os.path.join(
            modelling_dir, "imgs", boost_bagging_models_dict[option1]["fig"]
        )
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Load Model
        file_path = os.path.join(
            modelling_dir, "models", boost_bagging_models_dict[option1]["model"]
        )
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        # Display main results
        col1, col2, col3 = st.columns(3)
        y_pred = model.predict(X_test)
        cm = pd.crosstab(
            y_test,
            y_pred,
            rownames=["real"],
            colnames=["predicted"],
            # normalize='columns'
        )

        col1.write("### Confusion Matrix")
        col1.write(cm)

        col2.write("### Score")
        col2.write(model.score(X_test, y_test))

    grid_search_models_dict = {
        "K-nearest Neighbors": {
            "model": "Grid Search KNN.pkl",
            "fig": "1-Grid Search KNN.pkl",
        },
        "Logistic Regression": {
            "model": "Grid Search Logistic Regression.pkl",
            "fig": "1-Grid Search Logistic Regression.pkl",
        },
        "Random Forest": {
            "model": "Grid Search Random Forest.pkl",
            "fig": "1-Grid Search Random Forest.pkl",
        },
        "SVM": {"model": "Grid Search SVM.pkl", "fig": "1-Grid Search SVM.pkl"},
        "RESULTS SUMMARY": {
            "model": "Grid Search Random Forest.pkl",
            "fig": "1-Results Summary Grid Search.pkl",
        },
    }

    st.write("## Grid Search")
    with st.expander("Grid Search Results"):
        list_of_options = [key for key in grid_search_models_dict]
        option = st.selectbox("Select the model you want to check:", list_of_options)

        # Load result Graph
        file_path = os.path.join(
            modelling_dir, "imgs", grid_search_models_dict[option]["fig"]
        )
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Load Model
        file_path = os.path.join(
            modelling_dir, "models", grid_search_models_dict[option]["model"]
        )
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        # Display main results
        col1, col2, col3 = st.columns(3)
        y_pred = model.predict(X_test)
        cm = pd.crosstab(
            y_test,
            y_pred,
            rownames=["real"],
            colnames=["predicted"],
            # normalize='columns'
        )
        col1.write("### Grid Parameters")
        col1.write(model.param_grid)

        col2.write("### Confusion Matrix")
        col2.write(cm)
        col2.write("Best Parameters")
        col2.write(model.best_params_)

        df = (
            pd.DataFrame.from_dict(model.cv_results_)
            .loc[:, ["params", "mean_test_score"]]
            .sort_values(by="mean_test_score", ascending=False)
        )
        col3.write("### Parameters Ranking")
        col3.write(df)

    st.write("## Voting Classifier")
    with st.expander("Grid Search Results"):
        # Load result Graph
        file_path = os.path.join(modelling_dir, "imgs", "1-Voting Results.pkl")
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Load Model
        file_path = os.path.join(modelling_dir, "models", "2-Voting Classifier.pkl")
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        # Display main results
        col1, col2, col3 = st.columns(3)
        y_pred = model.predict(X_test)
        cm = pd.crosstab(
            y_test,
            y_pred,
            rownames=["real"],
            colnames=["predicted"],
            # normalize='columns'
        )

        col1.write("### Confusion Matrix")
        col1.write(cm)

        col2.write("### Score")
        col2.write(model.score(X_test, y_test))
