import os
import pickle

import streamlit as st
import pandas as pd

# Configs
st.set_page_config(
    page_title = 'CO2 Emissions',
    layout = 'wide'
)
st.write('# Modelling')

model_dict = {
    'K-nearest Neighbors': {'model' : 'Grid Search KNN.pkl', 'fig' : '1-Grid Search KNN.pkl'},
    'Logistic Regression': {'model' : 'Grid Search Logistic Regression.pkl', 'fig' : '1-Grid Search Logistic Regression.pkl'},
    'Random Forest': {'model' : 'Grid Search Random Forest.pkl', 'fig' : '1-Grid Search Random Forest.pkl'},
    'SVM': {'model' : 'Grid Search SVM.pkl', 'fig' : '1-Grid Search SVM.pkl'}
}
list_of_options = [key for key in model_dict]
option = st.selectbox(
    'Select the model you want to check:',
    list_of_options
)

# Load result Graph
file_path = os.path.join('assets', '4_modelling', 'imgs', model_dict[option]['fig'])
with open(file_path, 'rb') as f:
    fig = pickle.load(f)
st.plotly_chart(fig, use_container_width=True)
# Load Model
file_path = os.path.join('assets', '4_modelling', 'models', model_dict[option]['model'])
with open(file_path, 'rb') as f:
    model = pickle.load(f)
# Load Data (only test is required as train already used to fit model)
file_path = os.path.join('assets', '4_modelling', 'data', 'X_test.pkl')
with open(file_path, 'rb') as f:
    X_test = pickle.load(f)
file_path = os.path.join('assets', '4_modelling', 'data', 'y_test.pkl')
with open(file_path, 'rb') as f:
    y_test = pickle.load(f)

# Display main results 
col1, col2, col3 = st.columns(3)
y_pred = model.predict(X_test)
cm = pd.crosstab(
    y_test, 
    y_pred,
    rownames=['real'], 
    colnames=['predicted'], 
    # normalize='columns'
)
col1.write('### Grid Parameters')
col1.write(model.param_grid)

col2.write('### Confusion Matrix')
col2.write(cm)
col2.write('Best Parameters')
col2.write(model.best_params_)

df = pd.DataFrame.from_dict(
    model.cv_results_
).loc[:,['params', 'mean_test_score']].sort_values(by='mean_test_score', ascending=False)
col3.write('### Parameters Ranking')
col3.write(df)

# st.write(dir(model))
