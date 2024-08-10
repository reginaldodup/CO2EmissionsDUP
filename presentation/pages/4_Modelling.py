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


tab1, tab2 = st.tabs(["Regression", "Classification"])
with tab1:
    st.write("# To be developped")
    
with tab2:
    st.write("# Simple models")
    with st.expander("# Simple models"):
        st.write("to be developped")

    st.write("# Boosting and Bagging")
    with st.expander("# Boosting and Bagging"):
        st.write("to be developped")


    model_dict = {
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
            "model": "Grid Search SVM.pkl",
            "fig": "1-Results Summary Grid Search.pkl",
        },
    }

    st.write("# Grid Search")
    with st.expander("Grid Search Results"):
        list_of_options = [key for key in model_dict]
        option = st.selectbox("Select the model you want to check:", list_of_options)

        # Load result Graph
        file_path = os.path.join(modelling_dir, "imgs", model_dict[option]["fig"])
        with open(file_path, "rb") as f:
            fig = pickle.load(f)
        st.plotly_chart(fig, use_container_width=True)
        # Load Model
        file_path = os.path.join(modelling_dir, "models", model_dict[option]["model"])
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        # Load Data (only test is required as train already used to fit model)
        file_path = os.path.join(modelling_dir, "data", "X_test.pkl")
        with open(file_path, "rb") as f:
            X_test = pickle.load(f)
        file_path = os.path.join(modelling_dir, "data", "y_test.pkl")
        with open(file_path, "rb") as f:
            y_test = pickle.load(f)

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

    st.write("# Voting Classifier")
    with st.expander("Grid Search Results"):
        st.write("# To be developped")
