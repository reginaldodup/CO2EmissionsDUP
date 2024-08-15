import streamlit as st
import pandas as pd

from pathlib import Path
import os
import sys

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir
from co2emissions.utils import list_to_cols

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")
st.write("# Data Presentation")

# df_info = pd.read_excel(
#     os.path.join(data_dir, "0-raw", "FRANCE", "carlab-annuaire-variable.xlsx"),
#     sheet_name="EN",
# ).fillna("-")
# 
# st.table(df_info)
df = pd.read_csv(os.path.join(data_dir, "0-raw", "FRANCE", "data_merged.csv"))

var_dict = {
    "CATEGORICAL": {
        "lib_mrq_utac": {
            "name": "lib_mrq_utac",
            "description" : """
#### Brand

The brand of the car manufacturer (the real brand of the car is indicated and
not the group of manufacturers i.e Peugeot is indicated and not the PSA group
which regroup different brands like Peugeot, Citroën, etc…)
""",
        },
        "lib_mod_doss": {
            "name": "lib_mod_doss",
            "description": """
#### File name
The file name of the car.
""",
        },
        "lib_mod": {
            "name": "lib_mod",
            "description": """
#### Business name

The business name of the car: The manufacturer chooses the business name which
will be written on the vehicle registration document. In the dataset, the file
name of the car can be identical to the business name but can also be slightly
different (i.e. for the same car: lib_mod_doss name = AR8C SPIDER and lib_mod =
8C SPIDER)
""",
        },
        "dscom": {
            "name": "dscom",
            "description": """
#### Commercial Designation 

It regroups different information about the car model i.e. : 3008 1.6 THP
(156ch) BVM6 "3008" is the business name of the car "1.6" is the volume of all
engine cylinders, here it's 1.6 liters or 1600 cm3 "THP" is a name of a motor
brand (Turbo High Pressure) "(156ch)" is the power of an engine "BVM6" means 6
speed manual gearbox.
""",
        },
        "cnit": {
            "name": "cnit",
            "description": """
#### National Type Identification Code (CNIT) 

Is a number attributed to all the cars. This number is mandatory to register
the vehicle and is written on the vehicle registration document. It is a
sequence of 15 characters (i.e. "M10ALFVP0000324").
""",
        },
        "tvv": {
            "name": "tvv",
            "description": """
#### Variant-Variant (TVV) or the Mines type 

It corresponds to an alphanumeric sequence (i.e. KW01B5B) which is specific to
each manufacturer and allow to identify the specific finishing of a car. The
manufacturer provides a unique identifier for each type, version, and variant
of a car. It means that all identical models have the same Variant-Variant
numbers. The TVV is divided in 3 main information:

- The type which regroups all the identical information on some technical points.
- The variant if the car has different model.
- The version which gives the different finishing of a car.
""",
        },
        "cod_cbr": {
            "name": "cod_cbr",
            "description": """
#### Type of fuel

`GO`: Diesel; `ES`: Gasoline; `EH`: Non-plug-in hybrid vehicle; `GN/ES`: Natural
Gas/Gasoline; `GH`: Non-plug-in electric diesel; `ES/GP`: Gasoline/liquefied
petroleum gas; `EL`: Electric; `GN`: Gas Natural; `EE`: Gasoline electricity plug-in
hybrid; `FE`: E85 super-ethanol; `GL`: Diesel plug-in electricity.
""",
        },
        "hybride": {
            "name": "hybride",
            "description": """
Information to identify hybrid vehicles.
""",
        },
        "typ_boite_nb_rapp": {
            "name": "typ_boite_nb_rapp",
            "description": """
#### Type of Gearbox and number of reports
The type of gearbox (first letter) and the number of reports (the following
number) i.e. 'M 6' means Manual Gearbox and 6 reports.
""",
        },
        "": {
            "name": "",
            "description": """""",
        },
        "": {
            "name": "",
            "description": """""",
        },
    },
    "QUANTITATIVE": {
        "ADMIN POWER": {
            "name": "",
            "description": """""",
        },
        "MAXIMUM POWER": {
            "name": "",
            "description": """""",
        },
        "CONSO URB": {
            "name": "",
            "description": """""",
        },
        "CONSO EXURB": {
            "name": "",
            "description": """""",
        },
        "CONSO MIXTE": {
            "name": "",
            "description": """""",
        },
        "CO TYPE 1": {
            "name": "",
            "description": """""",
        },
        "HC": {
            "name": "",
            "description": """""",
        },
        "NOX": {
            "name": "",
            "description": """""",
        },
        "HCNOX": {},
    },
}



st.write("## Quantitative Values")
with st.expander("Quantitative Values"):
    selected_var = "typ_boite_nb_rapp"
    st.write(var_dict['CATEGORICAL'][selected_var]['description'])

    col1, col2 = st.columns(2)
    col1.code(f"Missing values: {df[selected_var].isna().sum()}")
    col2.code(f"Var type: {df[selected_var].dtype}")

    l = df[selected_var].unique()
    st.write(f"#### Unique Values: `{len(l)}`")
    if len(l) > 600:
        col1, col2 = st.columns(2)
        col1.write("##### Head")
        col1.write(df[selected_var].head())
        col2.write("##### Tail")
        col2.write(df[selected_var].tail())
    elif len(l) <= 10:
        st.code(df[selected_var].value_counts())
    else:
        st.code(list_to_cols(l, 5))
