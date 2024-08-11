from pathlib import Path
import os
import sys
import pickle

import streamlit as st
import pandas as pd

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

modelling_dir = os.path.join(notebooks_dir, "_Step3_Modelling")


# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")

# Load Data (only test is required as train already used to fit model)
file_path = os.path.join(modelling_dir, "data", "X_test.pkl")
with open(file_path, "rb") as f:
    X_test = pickle.load(f)
file_path = os.path.join(modelling_dir, "data", "y_test.pkl")
with open(file_path, "rb") as f:
    y_test = pickle.load(f)


tab1, tab2 = st.tabs(["Linear Regression", "Classification"])
# -----------------------------------------
# REGRESSION
# -----------------------------------------
with tab1:
    st.write("## Linear Regression Problem Definition")
    with st.expander("Definition"):
        st.markdown(
            r"""
The usual simple linear regression model is the following:

$y=β_0+β_1x+ε$  

In our case:   
* $y$ is the `CO2 emission`,  
* $x$ is a continuous, quantitative, explanatory variable,  
* $ε$ is a random error term that follows the normal distribution of zero mean and standard deviation σ.

The regression model will estimate the coefficients $β_0$ and $β_1$ with $\tilde{β}_0$ and $\tilde{β}_1$, allowing us to calculate the values $\tilde{y}=\tilde{β}_0+\tilde{β}_1x$.
 
Residues are defined by $ε = y - \tilde{y}$.

Regularized Linear Regressions are also used in this study, for details refer to Notebook MASTER_Linear Regression under _Step3_Modelling folder in our github. 
"""
        )

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

    st.write("## Regularized Linear Regression")
    with st.expander("Regularized Linear Regression"):
        st.write("to be developped")

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
