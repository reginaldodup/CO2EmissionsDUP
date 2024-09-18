# Introduction

This repository was created to present the CO2 Emission Project in the framework of the Data Scientist MLOPS course provided by [DataScientest](https://datascientest.com/en/). Where we completed the following trainning: 

- [Data Scientist](https://datascientest.com/en/data-scientist-course)
- [MLOPs](https://datascientest.com/en/ml-ops-course)

This repository contains the following items:

- The notebooks used on each steps of the project
- An Streamlit presentation used in the defense to present the project

## Cohort

- Clement ARNAUD - Process Engineer - (CFT TEN - PARIS)
- Diego GOMEZ-OCHOA - Process Engineer - (REFINING TEN - PARIS)
- Presheet DESHPANDE - Technical Safety & Risk Engineer - (GENESIS - LONDON)
- Reginaldo MARINHO - Process Engineer - (CFT TEN - PARIS)
- Simran MASOOD - Process Engineer - (CFT TEN - PARIS)

## Project Mentor

- Antoine TARDIVON - Data Scientist - (DataScientest)

## Data used

- [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france)
- [European Environment Agency](https://www.eea.europa.eu/en/datahub/datahubitem-view/fa8b1229-3db6-495d-b18e-9c9b3267c02b)

## Objectives

The main objective is estimating the CO2 emissions of vehicles based on their characteristics. This can be done by
approaching the problem in two ways:

- Regression Problem: Estimating the values of the CO2 emissions via Linear Regression algorithms to find a value
as precise as possible.

- Classification Problem: Grouping the CO2 emissions by ranges and trying to predict, based on the vehicle
characteristics, what group it belongs to.

# How to download and use ?

## Download and installation of requirements

* Clone the repository: ```git clone https://github.com/reginaldodup/CO2EmissionsDUP.git```

> ### Linux
>
> * Create a virtual environment: ```python3 -m venv venv```
> * Activate virtual environment: ```source venv/bin/activate```
> * Install requirements: ```pip3 install -r requirements.txt```
> 
> ### Windows
> 
> * Create a virtual environment: ```python -m venv venv```
> * Activate virtual environment: ```venv\Script\activate.bat```
> * Install requirements: ```pip install -r requirements.txt```

## Run presentation

* Change to presentation folder: ```cd presentation```
* Run presentation: ```streamlit run Intro.py```

## Run jupyterlab

* ```jupyter-lab .```

# Main Results

## Regression

![image](https://github.com/reginaldodup/CO2EmissionsDUP/blob/main/1_notebooks/_Step3_Modelling/imgs/0-Regression%20Models%20Results%20Summary.svg)

## Classification

### Simple Classification

![image](https://github.com/reginaldodup/CO2EmissionsDUP/blob/main/1_notebooks/_Step3_Modelling/imgs/1-Results%20Summary%20Simple%20Classification.svg)

### Boosting and Bagging

![image](https://github.com/reginaldodup/CO2EmissionsDUP/blob/main/1_notebooks/_Step3_Modelling/imgs/1-Results%20Summary%20Boosting%20and%20Bagging.svg)

### Grid Search

![image](https://github.com/reginaldodup/CO2EmissionsDUP/blob/main/1_notebooks/_Step3_Modelling/imgs/1-Results%20Summary%20Grid%20Search.svg)

### Voting Classifier

![image](https://github.com/reginaldodup/CO2EmissionsDUP/blob/main/1_notebooks/_Step3_Modelling/imgs/1-Voting%20Results.svg)
