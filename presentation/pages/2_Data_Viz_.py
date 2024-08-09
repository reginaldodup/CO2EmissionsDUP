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

with st.expander("Data selection"):

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
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "0-AVERAGE OF CO2 EMISSION BY BRAND.pkl",
            ),
            "TYPE OF FUEL": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "2-AVERAGE OF CO2 EMISSION BY TYPE OF FUEL.pkl",
            ),
            "HYBRID": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "3-AVERAGE OF CO2 EMISSION BY HYBRID.pkl",
            ),
            "TYPE OF FUEL / HYBRID": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "3-AVERAGE OF CO2 EMISSION BY TYPE OF FUEL AND HYBRID.pkl",
            ),
            "TYPE OF GEARBOX": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "4-AVERAGE OF CO2 EMISSION BY TYPE OF GEARBOX.pkl",
            ),
            "TYPE OF GEARBOX / HYBRID": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "4-AVERAGE OF CO2 EMISSION BY TYPE OF GEARBOX AND HYBRID.pkl",
            ),
            "YEAR": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "5-AVERAGE OF CO2 EMISSION BY YEAR.pkl",
            ),
            "CARROSSERIE": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "7-CO2 EMISSIONS VS CARROSSERIE.pkl",
            ),
            "CARROSSERIE / FUEL TYPE": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "6-CO2 EMISSIONS VS CARROSSERIE AND COD_CBR.pkl",
            ),
            "GAMME": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "8-CO2 EMISSIONS VS GAMME.pkl",
            ),
        },
        "QUANTITATIVE": {
            "ADMIN POWER": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "9-CO2 EMISSIONS VS ADMIN POWER.pkl",
            ),
            "MAXIMUM POWER": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "10-CO2 EMISSIONS VS MAXIMUM POWER.pkl",
            ),
            "CONSO URB": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "11-CO2 EMISSIONS VS CONSO URB AND HYBRID.pkl",
            ),
            "CONSO EXURB": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "12-CO2 EMISSIONS VS CONSO EXURB AND HYBRID.pkl",
            ),
            "CONSO MIXTE": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "13-CO2 EMISSIONS VS CONSO MIXTE AND HYBRID.pkl",
            ),
            "CO TYPE 1": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "14-CO2 EMISSIONS VS CO TYPE 1 AND HYBRID.pkl",
            ),
            "HC": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "15-CO2 EMISSIONS VS HC AND HYBRID.pkl",
            ),
            "NOX": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "16-CO2 EMISSIONS VS NOX AND HYBRID.pkl",
            ),
            "HCNOX": os.path.join(
                notebooks_dir,
                "_Step1-DataViz",
                "imgs",
                "17-CO2 EMISSIONS VS HCNOX AND HYBRID.pkl",
            ),
        },
    }
    with col2:
        list_of_options = [key for key in plot_dict[st.session_state.VAR_TYPE]]
        option = st.selectbox(
            "Select The Variable you want to explore:", list_of_options
        )

    st.write(f"## {option.title()}")
    with open(plot_dict[st.session_state.VAR_TYPE][option], "rb") as f:
        fig = pickle.load(f)

    st.plotly_chart(fig, use_container_width=True)


st.write("# Correlation")
st.markdown(
    """
In the section below you can see the variable coorelations in relation to our target variable `CO2 Emissions`
"""
)

with st.expander("Correlation"):
    with open(
        os.path.join(
            notebooks_dir, "_Step1-DataViz", "imgs", "11-CORRELATION MATRIX.pkl"
        ),
        "rb",
    ) as f:
        fig = pickle.load(f)
    st.plotly_chart(
        fig,
        use_container_width=True,
    )
