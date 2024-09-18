import streamlit as st
import pickle
import os

import reveal_slides as rs

# Configs
st.set_page_config(page_title="CO2 Emissions", layout="wide")

sample_markdown = r"""
## CO2 Emissions

### Data Upskilling Program

PROMO 2023-2024

---
## COHORT

- Clement ARNAUD - Process Engineer - (CFT TEN - PARIS) <!-- .element: class="fragment" data-fragment-index="0" -->
- Diego GOMEZ-OCHOA - Process Engineer - (REFINING TEN - PARIS) <!-- .element: class="fragment" data-fragment-index="0" -->
- Presheet DESHPANDE - Technical Safety & Risk Engineer - (GENESIS - LONDON) <!-- .element: class="fragment" data-fragment-index="0" -->
- Reginaldo MARINHO - Process Engineer - (CFT TEN - PARIS) <!-- .element: class="fragment" data-fragment-index="0" -->
- Simran MASOOD - Process Engineer - (CFT TEN - PARIS) <!-- .element: class="fragment" data-fragment-index="0" -->

# 
# 

## PROJECT MENTOR
<!-- .element: class="fragment" data-fragment-index="1" -->
- Antoine TARDIVON - Data Scientist - (DataScientest)
<!-- .element: class="fragment" data-fragment-index="1" -->
---

## Project Steps

1. Data Vizualisation <!-- .element: class="fragment" data-fragment-index="1" -->
1. Pre-processing and Feature Engineering <!-- .element: class="fragment" data-fragment-index="2" -->
1. Modelling <!-- .element: class="fragment" data-fragment-index="3" -->

"""

st.write("# CO2 Emissions Estimation Project")

with st.expander("Intro Slides", expanded=True):

    rs.slides(
        sample_markdown,
        height=800,
        theme="white",  # ["black", "black-contrast", "blood", "dracula", "moon", "white", "white-contrast", "league", "beige", "sky", "night", "serif", "simple", "solarized"]
        config={
            "width": 1600,
            # "height": 600,
            "minScale": 0.5,
            "center": True,
            "maxScale": 1.0,
            "margin": 0.2,
            "plugins": [
                "highlight",
                "katex",
                "mathjax2",
                "mathjax3",
                "notes",
                "search",
                "zoom",
            ],
        },
        # initial_state={
        # "indexh": hslidePos,
        # "indexv": vslidePos,
        # "indexf": fragPos,
        # "paused": paused,
        # "overview": overview
        # },
        # markdown_props={"data-separator-vertical":"^--$"},
        # key="foo",
    )


# INTRODUCTION
# -------------
st.write("## Context")

with st.expander("Context"):

    st.markdown(
        """
### Context

Global transportation sector is a major contributor to greenhouse gas emissions, with passenger cars and vans responsible for
around 10% of global energy-related CO2 emissions in 2022 according to International Energy Agency (IEA). This substantial
emission rate significantly affects air quality and contributes to climate change. Therefore, identifying the vehicles emitting
the most CO2 and other pollutants is crucial for devising effective strategies to mitigate environmental impact. As automotive
technology evolves, understanding the role of technical characteristics with respect to emissions is vital for promoting the
development and adoption of cleaner and more efficient vehicles ultimately contributing to the realization of the Net Zero
Emissions goals by 2050.
"""
    )

    file_path = os.path.join(
        "assets", "0_intro", "0-World CO2 Emissions For Fuel and Land Use.pkl"
    )
    with open(file_path, "rb") as f:
        fig = pickle.load(f)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
This project explores two datasets (given below) encompassing a wide array of technical specifications of vehicles, alongside
their fuel consumption, CO2 emissions, and pollutant emissions, marketed both in France and Europe. Through the application
of Data Science and Machine Learning techniques, our objective is to explore the relationship between vehicle specifications
and emissions. By doing so, we aim to provide valuable insights that can inform decision-making processes in environmental
policy and drive advancements in automotive industry practices towards sustainable transportation solutions.
The following datasets are provided for reference:

- [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france)
- [European Environment Agency](https://www.eea.europa.eu/en/datahub/datahubitem-view/fa8b1229-3db6-495d-b18e-9c9b3267c02b)

This project employs a combination of data analysis, statistical modeling, and machine learning techniques to extract
actionable insights from the dataset. Exploratory data analysis (EDA) will uncover patterns and relationships within the data,
providing a foundational understanding of the variables at play. Feature engineering will involve transforming or selecting
relevant variables to enhance model performance. Lastly, statistical modeling techniques, such as linear regression, will help
quantify the impact of technical characteristics of vehicles on CO2 emissions. Additionally, machine learning algorithms, such
as decision trees or random forests, or ensemble learning algorithms such as Bagging and Boosting may be utilized for better
predictive performance of the model.
"""
    )


st.write("## Objective")
with st.expander("Objective"):
    st.markdown(r"""
The main objective is estimating the `CO2 emissions` of vehicles based on their characteristics.
""")
    st.image("assets\imgs\objective.svg")


# DATA SET SELECTION
# -------------
st.write('## Data Set Selection')
with st.expander("Data selection"):
    st.markdown(
        """
### Data Set Selection

To begin our metadata analysis, we have opted to start with the initial dataset sourced from 
[data.gouv.fr](https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france). Our selection of the
French dataset over the European dataset is influenced by two factors. Firstly, upon preliminary examination, we observed
that the French dataset offers a wider array of explanatory variables pertinent to the project's scope. Notably, it provides a
detailed breakdown of fuel consumption across urban, extra-urban, and mixed driving conditions, alongside comprehensive
data concerning other emissions such as NOx, CO, HC, and particulates. Additionally, the French dataset includes information
on the car's body type and range enriching the depth of our analysis.
However, it is worth noting that the European Environment Agency (EEA) dataset does contain supplementary technical
characteristics of vehicles, such as wheelbase, track width, and other dimensions, which may be of interest for future stages
of our preprocessing efforts.

Within the French dataset, our focus centered on the most recent four years, spanning from 2012 to 2015, for our preliminary
analysis. This selection was motivated by the emergence of hybrid vehicles, which began to appear prominently from 2011
onwards. To ensure that these vehicles were included in our analysis, we deemed it necessary to limit our dataset to the years
2011 and beyond. However, we made an exception for the year 2011 due to the limited availability of significant explanatory
variables, including data on NOx, CO, and HC emissions, particulate emissions, mileage, body type of the car, and vehicle mass.
Another important step of our thinking was the discover of two norms to measure the CO2 emissions: the New European
Driving cycle (NEDC) and the Worldwide Harmonized Light Vehicle (WLTP). The first one is an older way to standardized the
way to measure the CO2 emissions of a car between all the different passenger vehicles. As of 1st September 2017, a new
standard has been launched to provide more realistic measurements. It means that to have comparable values, it is not
recommended to merge older dataset dating from before 2017 with most recent dataset. For this reason, we have decided to
focus especially on dataset between 2012 and 2015 where the CO2 emissions is measured with the NEDC norm. We have also
decided to not have a too large number of years available as we expect that the technology and the legislation norms evolve
each years and may impact the prediction.

    """
    )
