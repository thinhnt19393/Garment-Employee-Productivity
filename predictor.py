import streamlit as st
import numpy as np
import pandas as pd
import pickle

pipe = pickle.load(open('pipeline.sav', 'rb'))

st.title('Garment Worker Productivity Prediction')
st.image("""https://imagev3.vietnamplus.vn/w1000/Uploaded/2024/bokttj/2023_12_10/ttxvn-det-may-viet-nam-1-9433.jpg""", width=700)
st.header('Enter the characteristics of the worker:')

quarter = st.selectbox('Quarter:', ['Quarter1', 'Quarter2', 'Quarter3', 'Quarter4', 'Quarter5'])
department = st.selectbox('Department:', ['finishing', 'sewing'])
day = st.selectbox('Day:', ['Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday'])
team = st.selectbox('Team:', ['Team1', 'Team2', 'Team3', 'Team4', 'Team5', 'Team6', 'Team7', 'Team8', 'Team9', 'Team10',
                              'Team11', 'Team12'])
targeted_productivity = st.number_input('Targeted Productivity:', min_value=0.1, max_value=0.8, value=0.70)
smv = st.number_input('Standard Minute Value:', min_value=0, max_value=55, value=21)
wip = st.number_input('Work in Progress:', min_value=0, max_value=23122, value=1393)
over_time = st.number_input('Amount of Overtime (min):', min_value=0, max_value=25920, value=0)
incentive = st.number_input('Amount of Financial Incentive (BDP):', min_value=0, max_value=3600, value=0)
idle_time = st.number_input('Idle Time:', min_value=0, max_value=300, value=0)
idle_men = st.number_input('Idle Men:', min_value=0, max_value=45, value=0)
no_of_style_change = st.number_input('Number of Style Changes:', min_value=0, max_value=2, value=0)
no_of_workers = st.number_input('Number of Workers:', min_value=2, max_value=89, value=52)

if st.button('Predict Productivity'):
    X = [[quarter, department, day, team, targeted_productivity, smv, wip, over_time, incentive, idle_time, idle_men, no_of_style_change, no_of_workers]]
    X = np.array(X, dtype='object')
    pdt = pipe.predict(X)[0]
    st.success(f'The predicted productivity of the workers is {pdt:.4f} ')
