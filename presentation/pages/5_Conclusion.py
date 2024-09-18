import streamlit as st
import pickle

from pathlib import Path
import os
import sys

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")
st.write("# Results Summary")
st.write(
    "Check out our [GitHub](https://github.com/reginaldodup/CO2EmissionsDUP/tree/main)"
)

st.write("## Regression")

with open(
    os.path.join(
        notebooks_dir,
        "_Step3_Modelling",
        "imgs",
        "0-Regression Models Results Summary.pkl",
    ),
    "rb",
) as f:
    fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)

st.write("## Classification")

st.write("### Simple Classification")

with open(
    os.path.join(
        notebooks_dir,
        "_Step3_Modelling",
        "imgs",
        "1-Results Summary Simple Classification.pkl",
    ),
    "rb",
) as f:
    fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)

st.write("### Boosting and Bagging")

with open(
    os.path.join(
        notebooks_dir,
        "_Step3_Modelling",
        "imgs",
        "1-Results Summary Boosting and Bagging.pkl",
    ),
    "rb",
) as f:
    fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)

st.write("### Grid Search")

with open(
    os.path.join(
        notebooks_dir, "_Step3_Modelling", "imgs", "1-Results Summary Grid Search.pkl"
    ),
    "rb",
) as f:
    fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)

st.write("### Voting Classifier")

with open(
    os.path.join(notebooks_dir, "_Step3_Modelling", "imgs", "1-Voting Results.pkl"),
    "rb",
) as f:
    fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)
