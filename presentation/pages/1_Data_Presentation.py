import streamlit as st
import pandas as pd
import os

# Configs
st.set_page_config(
    page_title = 'CO2 Emissions',
    layout = 'wide'
)
st.write('# Data Presentation')

st.write('## Variable Names')

df_info = pd.read_excel(
        os.path.join('assets', '1_data_presentation', 'carlab-annuaire-variable.xlsx'),
        sheet_name='EN'
).fillna('-')

st.table(df_info)

