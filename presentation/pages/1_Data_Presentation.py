import streamlit as st
import pandas as pd

from pathlib import Path
import os
import sys

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")
st.write("# Data Presentation")

st.write("## Variable Names")

df_info = pd.read_excel(
    os.path.join(data_dir, "0-raw", "FRANCE", "carlab-annuaire-variable.xlsx"),
    sheet_name="EN",
).fillna("-")

st.table(df_info)
