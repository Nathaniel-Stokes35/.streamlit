import streamlit as st
import scipy.stats
import time
import pandas as pd

# Adding Stateful variables to keep a list of total expeirments over all runs
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['Run', 'Flips', 'Mean'])

# Simple Header to introduce the program
st.header('Tossing a Coin')

chart = st.line_chart([0.5])
# Function to calculate the mean and preform the flips
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        rounded_mean = round(mean, 4)
        chart.add_rows([rounded_mean])
        time.sleep(0.05)

    return rounded_mean

number_of_trials = st.slider('Number of Flips?', 1, 1000, 10)
start_button = st.button('Run')

# Showing results across all runs
st.write(st.session_state['df_experiment_results'])
# Running the experiment
if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['Run', 'Flips', 'Mean'])
        ],
        axis=0)
    st.write(f'The mean for {number_of_trials} flips was {mean}.')
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)