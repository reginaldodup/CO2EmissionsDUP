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
            "description": """
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
#### Type of vehicle

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
        "champ_v9": {
            "name": "champ_v9",
            "description": """
#### Certification of vehicle

The champ_v9 corresponds to the certification of the vehicle. We could then
separate them into certified and uncertified classes.
""",
        },
        "date_maj": {
            "name": "date_maj",
            "description": """
#### Date of the last update.
""",
        },
        "Carrosserie": {
            "name": "Carrosserie",
            "description": """
#### Car’s body type
""",
        },
        "gamme": {
            "name": "gamme",
            "description": """
#### Range

The range of the car in term of quality (luxury car…).
""",
        },
    },
    "QUANTITATIVE": {
        "co2": {
            "name": "co2",
            "description": """
#### CO2 Emissions

CO2 emission (in g/km) of the car. For the French dataset (2012-2015), the
measure is according the NEDC norm.

This is our `target variable`. In following steps of this project, we will define
if we treat this as a regression problem or a classification problem (or both).
When treating the problem as a classification this variable will be split in
bins which represent a certain category of emissions (ex.: low, high, average,
high and very high).
""",
        },
        "puiss_admin_98": {
            "name": "puiss_admin_98",
            "description": """
#### Administrative Power

Administrative power is expressed in 'CV' (tax horsepower) and is used to
estimate the tax amount on the car during registration of renewal of the
vehicle registration document.

In France, it exists two formulas to convert the motor power (kW) to
administrative power (CV):

- Approval from January 1, 2020:

> $Admin Power (CV) = 1.34 + {\\left(1.8 \\times \\frac{Motor Power(kW)}{100}\\right)}^2 + {\\left(3.87 \\times \\frac{Motor Power(kW)}{100}\\right)}$

- Approval before December 31, 2019:

> $Admin Power (CV) = 1.34 + {\\frac{CO2 Emission (g/km)}{45}} + {\\frac{Motor Power(kW)}{40}} \\times 1.6$

There is a correlation between the target variable CO2 Emissions and this
variable. To be discussed during the next phase if this variable should be
removed or not from the dataset.
""",
        },
        "puiss_max": {
            "name": "puiss_max",
            "description": """
#### Max power

Maximum power of the motor expressed in KW.
""",
        },
        "conso_urb": {
            "name": "conso_urb",
            "description": """
#### Urban fuel consumption (in L/100km)

This consumption corresponds to drive in an urban area with an acceleration up
to 15 km/h, 30 km/h and 50 km/h. Including the most frequent stop, the urban
fuel consumption is typically the higher consumption.
""",
        },
        "conso_exurb": {
            "name": "conso_exurb",
            "description": """
#### Extra urban fuel consumption (in L/100km)

This consumption corresponds to drive in an extra urban area with a drive on
several speed levels up to 120 km/h/ It allows to optimize the driving and the
fuel consumption of the car. Therefore, this consumption is generally the lower
consumption.
""",
        },
        "conso_mixte": {
            "name": "conso_mixte",
            "description": """
#### Mixed fuel consumption (in L/100km)

This consumption includes the drive in urban and extra urban area. Therefore,
the fuel consumption is typically between the urban fuel consumption and the
extra urban fuel consumption.
""",
        },
        "hc": {
            "name": "hc",
            "description": """
#### Unburned Hydrocarbons (HC) 

Trial results measurement (g/km).
""",
        },
        "nox": {
            "name": "nox",
            "description": """
#### NOx 

Trial results measurement (g/km).
""",
        },
        "hcnox": {
            "name": "hcnox",
            "description": """
#### $HC+NOx$ 

Trial results measurement (g/km)
""",
        },
        "ptcl": {
            "name": "ptcl",
            "description": """
#### Particle 

Trial results measurement (g/km)
""",
        },
        "masse_ordma_min": {
            "name": "masse_ordma_min",
            "description": """
#### The mass in minimum walking order (kg)

It corresponds to the empty weight of the car with a gas bottle, 90% of the
fluid necessary for the car to work and one driver (75 kg).
""",
        },
        "masse_ordma_max": {
            "name": "masse_ordma_max",
            "description": """
#### The mass in maximum walking order (kg)

It corresponds to the weight that the vehicle must not exceed (include
passengers and bags) 
""",
        },
    },
}


st.write("## Categorical Variables")
with st.expander("Categorical Variables"):
    opts0 = [key for key in var_dict["CATEGORICAL"]]
    opt0 = st.selectbox("Select the variable you want to check:", opts0)
    selected_var = opt0
    st.write(var_dict["CATEGORICAL"][selected_var]["description"])

    col1, col2 = st.columns(2)
    col1.code(df[selected_var].describe())
    # col2.code(f"Var type: {df[selected_var].dtype}")
    col2.code(f"Missing values: {df[selected_var].isna().sum()}")

    l = df[selected_var].unique().tolist()
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

st.write("## Quantitative Variables")
with st.expander("Quantitative Values"):
    opts1 = [key for key in var_dict["QUANTITATIVE"]]
    opt1 = st.selectbox("Select the variable you want to check:", opts1)
    selected_var = opt1
    st.write(var_dict["QUANTITATIVE"][selected_var]["description"])

    col1, col2 = st.columns(2)
    col1.code(f"Missing values: {df[selected_var].isna().sum()}")
    col2.code(f"Var type: {df[selected_var].dtype}")

    st.code(df[selected_var].describe())
