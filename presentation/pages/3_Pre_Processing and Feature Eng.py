from pathlib import Path
import os
import sys
import pickle

import streamlit as st

sys.path.append(str(Path.cwd().parent))  # Path to allow importing co2emissions
from co2emissions.config import data_dir, notebooks_dir, presentation_dir

pre_processing_dir = os.path.join(notebooks_dir, "_Step2-Preprocessing")

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")
st.write("# Pre-Processing and Feature Engineering")
st.write("## Pre-Processing")
with st.expander("Pre-processing"):
    st.write("#### `tvv` trailing spaces")
    st.markdown(
        """
> ```python
> df.tvv.head(3).tolist()
> ```
> ```shell
> ['939AXN1B52C ', '939AXP1B54C ', '939AXR1B64 ']
> ```
> ```python
> df.tvv = df.tvv.str.strip()
> ```
"""
    )
    st.write("#### `cod_cbr` Fuel Type Correction")
    st.markdown(
        """
> ```python
> df[['cod_cbr', 'hybride']][(df.hybride == 'oui')].value_counts()
> ```
> ```shell
> cod_cbr  hybride
> EH       oui        1043
> GH       oui         521
> ES       oui         105
> EE       oui         104
> GO       oui          27
> GL       oui           3
> Name: count, dtype: int64
> ```
> #### `GO` Hybrid Cars
> After looking for the cars with same tvv in the FRENCH database itself, we
> realized that the GO hybrid cars are GH cars. We apply his change to our
> dataset, considering that it was wrongly entered.
> ```python
> df.loc[(df.hybride == 'oui') & (df.cod_cbr == 'GO'), 'cod_cbr'] = 'GH'
> ```
> #### `EH` Hybrid Cars
After looking for the cars with same tvv in the FRENCH database itself we found
out that most of the cars have EH fuel type records for the same tvv. When
comparing the only ‘ES’ cars (14 out of the 105 ES hybrids) with the EEA cars
with same tvv, we found that many of them are entered also with petrol fuel
type. We consider that these cars where wrongly entered, and we correct ‘ES’ to
‘EH’ for these cars.
> ```python
> df.loc[(df.hybride == 'oui') & (df.cod_cbr == 'ES'), 'cod_cbr'] = 'EH' 
> ```
"""
    )

    st.image(os.path.join(pre_processing_dir, "imgs", "cod_cbr.png"))

# FEATURE ENGINEERING
# ---
st.write("## Feature Engineering")
with st.expander("Feature Engineering"):
    st.write("#### `hcnox` Correction")
    st.markdown(
        """
> $hcnox = hc + nox$
> ```python
> df[['hc', 'nox', 'hcnox']].isna().sum()
> ```
> ```shell
> hc       122967
> nox         690
> hcnox     37328
> dtype: int64
> ```
"""
    )
    col1, col2 = st.columns(2)
    col1.markdown(
        """
```python
# Replace all NaN hcnox with the sum of hc + nox
df.loc[:,'hcnox'] = df[['hcnox']].where(
    ~((df.hcnox.isna()) & ((~df.hc.isna()) & (~df.nox.isna()))), 
    df.hc + df.nox,
    axis=0
)
```
"""
    )
    col1.markdown(
        """
```python
# Replace hcnox = nox and hc = 0 for hc = NAN and nox > hcnox
# Replace all NaN hcnox with the sum of hc + nox
df.loc[:,'hcnox'] = df[['hcnox']].where( 
    ~((df.nox > df.hcnox) & (df.hc.isna())),
    df.nox,
    axis=0
)
df.loc[:,'hc'] = df[['hc']].where(
    ~((df.nox > df.hcnox) & (df.hc.isna())),
    0,
    axis=0
)
```
"""
    )
    col2.markdown(
        """
```python
# Replace hcnox = hc + nox where hcnox < hc + nox
# Replace all NaN hcnox with the sum of hc + nox
df.loc[:,'hcnox'] = df[['hcnox']].where(
    ~((~df.hcnox.isna()) & (df.nox > df.hcnox) & ((~df.hc.isna()) & (~df.nox.isna()))), 
    df.hc + df.nox,
    axis=0
)
```
"""
    )
    col2.markdown(
        """
```python
# Replace all NaN hc with hcnox - nox
df.loc[:,'hc'] = df[['hc']].where(
    ~((df.hc.isna()) & ((~df.hcnox.isna()) & (~df.nox.isna()))), 
    df.hcnox - df.nox,
    axis=0
)
```
"""
    )
    col2.markdown(
        """
```python
# Replace all NaN nox with hcnox - hc
df.loc[:,'nox'] = df[['nox']].where(
    ~((df.nox.isna()) & ((~df.hcnox.isna()) & (~df.hc.isna()))), 
    df.hcnox - df.hc,
    axis=0
)
```
"""
    )


    st.write("#### `typ_boite_nb_rapp` Separate Gearbox and nb of Reports")
    st.markdown(
        """
> The variable typ_boite_nb_rapp is composed of two parts:
> 
> - A letter indicating the type of gearbox
> - A number indicating the number of reports
> ```python
> df.typ_boite_nb_rapp
> ```
> ```shell
> 0         M 6
> 1         M 6
> 2         M 6
>          ... 
> 159766    M 5
> 159767    M 6
> 159779    M 6
> Name: typ_boite_nb_rapp, Length: 103248, dtype: object
> ```
"""
    )
    col1, col2 = st.columns(2)
    col1.markdown(
        """
```python
# Separate Type of Gearbox
type_of_gearbox = df.typ_boite_nb_rapp.apply(lambda x: x[0])
df['type_of_gearbox'] = type_of_gearbox
```
"""
    )
    col1.image(os.path.join(pre_processing_dir, "imgs", "type_of_gearbox.png"))
    col2.markdown(
        """
```python
# Separate Number of reports
nbr_reports = df.typ_boite_nb_rapp.apply(lambda x: x[-1:])
df['nbr_reports'] = nbr_reports
```
"""
    )
    col2.image(os.path.join(pre_processing_dir, "imgs", "Number of Reports.png"))

st.write("## Final Dataset")
with st.expander("Final Dataset"):

    col1, col2 = st.columns(2)
    col1.write("#### Initial Dataset")
    col1.code("""
<class 'pandas.core.frame.DataFrame'>
Index: 159780 entries, 0 to 40051
Data columns (total 26 columns):
 #   Column             Non-Null Count   Dtype  
---  ------             --------------   -----  
 0   lib_mrq_utac       159780 non-null  object 
 1   lib_mod_doss       159780 non-null  object 
 2   lib_mod            159780 non-null  object 
 3   dscom              159780 non-null  object 
 4   tvv                159780 non-null  object 
 5   cod_cbr            159780 non-null  object 
 6   hybride            159780 non-null  object 
 7   puiss_admin_98     159780 non-null  float64
 8   puiss_max          159724 non-null  float64
 9   typ_boite_nb_rapp  159780 non-null  object 
 10  conso_urb          159543 non-null  float64
 11  conso_exurb        159543 non-null  float64
 12  conso_mixte        159622 non-null  float64
 13  co2                159622 non-null  float64
 14  co_typ_1           159090 non-null  float64
 15  hc                 36813 non-null   float64
 16  nox                159090 non-null  float64
 17  hcnox              122452 non-null  float64
 18  ptcl               150181 non-null  float64
 19  masse_ordma_min    159780 non-null  float64
 20  masse_ordma_max    159780 non-null  float64
 21  champ_v9           159595 non-null  object 
 22  date_maj           68352 non-null   object 
 23  year               159780 non-null  int64  
 24  Carrosserie        138900 non-null  object 
 25  gamme              138900 non-null  object 
dtypes: float64(13), int64(1), object(12)
memory usage: 32.9+ MB
              """)
    col2.write("#### Final Dataset")
    col2.code("""
<class 'pandas.core.frame.DataFrame'>
Index: 103248 entries, 0 to 159779
Data columns (total 14 columns):
 #   Column           Non-Null Count   Dtype  
---  ------           --------------   -----  
 0   lib_mrq_utac     103248 non-null  object 
 1   cod_cbr          103248 non-null  object 
 2   hybride          103248 non-null  object 
 3   puiss_max        103248 non-null  float64
 4   conso_mixte      103248 non-null  float64
 5   co2              103248 non-null  float64
 6   co_typ_1         103248 non-null  float64
 7   hc               103248 non-null  float64
 8   nox              103248 non-null  float64
 9   hcnox            103248 non-null  float64
 10  masse_ordma_max  103248 non-null  float64
 11  year             103248 non-null  int64  
 12  type_of_gearbox  103248 non-null  object 
 13  nbr_reports      103248 non-null  object 
dtypes: float64(8), int64(1), object(5)
memory usage: 11.8+ MB
              """)

# ADDITIONAL DTAVIZ AFTER CORRECTION
# ---
st.write("## Final Correlation Matrix")
with st.expander("Additional Dataviz"):
    st.write("#### Quantitative Variables")

    file_path = os.path.join(pre_processing_dir, "imgs", "0-CORRELATION MATRIX.pkl")
    with open(file_path, "rb") as f:
        fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)
