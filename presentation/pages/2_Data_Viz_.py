import streamlit as st
import pickle

from pathlib import Path
import os
import sys

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")
st.write("# Data Vizualisation")

st.markdown(
    """
## Individual data Vizualsation

In the section below you can choose the variable you want to explore in relation to our target variable `CO2 Emissions`
"""
)

col1, col2 = st.columns(2)

if "VAR_TYPE" not in st.session_state:
    st.session_state.VAR_TYPE = "CATEGORICAL"

with col1:
    st.radio(
        "Select The Type of Variable you want to visualise:",
        key="VAR_TYPE",
        options=["CATEGORICAL", "QUANTITATIVE"],
    )

# Dictionary with all the plot as a pickle file
plot_dict = {
    "CATEGORICAL": {
        "BRAND": os.path.join(
            "assets", "2_dataviz", "0-AVERAGE OF CO2 EMISSION BY BRAND.pkl"
        ),
        "TYPE OF FUEL": os.path.join(
            "assets", "2_dataviz", "2-AVERAGE OF CO2 EMISSION BY TYPE OF FUEL.pkl"
        ),
        "HYBRID": os.path.join(
            "assets", "2_dataviz", "3-AVERAGE OF CO2 EMISSION BY HYBRID.pkl"
        ),
        "TYPE OF FUEL / HYBRID": os.path.join(
            "assets",
            "2_dataviz",
            "3-AVERAGE OF CO2 EMISSION BY TYPE OF FUEL AND HYBRID.pkl",
        ),
        "TYPE OF GEARBOX": os.path.join(
            "assets", "2_dataviz", "4-AVERAGE OF CO2 EMISSION BY TYPE OF GEARBOX.pkl"
        ),
        "TYPE OF GEARBOX / HYBRID": os.path.join(
            "assets",
            "2_dataviz",
            "4-AVERAGE OF CO2 EMISSION BY TYPE OF GEARBOX AND HYBRID.pkl",
        ),
        "YEAR": os.path.join(
            "assets", "2_dataviz", "5-AVERAGE OF CO2 EMISSION BY YEAR.pkl"
        ),
        "CARROSSERIE": os.path.join(
            "assets", "2_dataviz", "6-CO2 EMISSIONS VS CARROSSERIE.pkl"
        ),
        "CARROSSERIE / FUEL TYPE": os.path.join(
            "assets", "2_dataviz", "6-CO2 EMISSIONS VS CARROSSERIE AND FUEL TYPE.pkl"
        ),
    },
    "QUANTITATIVE": {"MAX POWER": None},
}
with col2:
    list_of_options = [key for key in plot_dict[st.session_state.VAR_TYPE]]
    option = st.selectbox("Select The Variable you want to explore:", list_of_options)


st.write(f"## {option.title()}")
with open(plot_dict[st.session_state.VAR_TYPE][option], "rb") as f:
    fig = pickle.load(f)


st.plotly_chart(fig, use_container_width=True)
