import pandas as pd
import urllib.request as urllib
import matplotlib.pyplot as plt

import pdb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

STATE_POP_DATA='SCPRC-EST2019-18+POP-RES.csv'
STATE_ABREV='state_abrev.json'
COVID_DATA_URL='https://covidtracking.com/api/v1/states/daily.json'
COVID_OUTPUT_FILE_NAME='covid_data.json'
GET_FIELDS_STATE=['NAME', 'POPESTIMATE2019']
GET_FIELDS_COVID=['date','state','positive','negative','death', 'totalTestResults', 'positiveIncrease','negativeIncrease', 'totalTestResultsIncrease', ]
ALL_FIELDS=['date','state','POPESTIMATE2019','positive','negative','death', 'totalTestResults', 'positiveIncrease','negativeIncrease','totalTestResultsIncrease']
OUTPUT_LIST=['mortality %', 'death %']
STATES=['NC', 'NY', 'FL']
if 'all' in STATES:
    STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
DEBUG=False
LOAD_NEW_DATA=False


def debug(message, data):
    if DEBUG == True:
        print(message, "\n-----------------------------\n", data, "\n-----------------------------\n")

def load_data_and_save(url, output_file_name):
    if LOAD_NEW_DATA == True:
        print(f'Loading data from {url} and saving to {output_file_name}...')
        uh = urllib.urlopen(url)
        data = uh.read().decode()
        file = open(output_file_name, 'w')
        file.write(data)
        file.close()
        debug('Loaded data:', data)
        debug('Data saved to:', output_file_name)
        data=pd.read_json(data)
        return data
    else:
        print(f'New data not loaded, reading from {output_file_name}. Set LOAD_NEW_DATA=True to load data')
        data=pd.read_json(output_file_name)
        return data


def analyse(data):

    show_info(data)

    data['date']=pd.to_datetime(data['date'], format='%Y%m%d')
    state_pop=pd.read_csv(STATE_POP_DATA)
    state_abrev=pd.read_json(STATE_ABREV)
    states=pd.merge(state_abrev, state_pop, left_on="name", right_on="NAME")
    data=pd.merge(states, data.get(GET_FIELDS_COVID), left_on='abbreviation', right_on='state')
    data=data.get(ALL_FIELDS)
    #pdb.settrace()
    data['positive_per_cent'] = (data['positive'] / data['POPESTIMATE2019']) * 100
    data['negative_per_cent']  = (data['negative'] / data['POPESTIMATE2019']) * 100
    data['positive_increase_per_cent'] = (data['positiveIncrease'] / data['POPESTIMATE2019']) * 100
    data['death_per_cent'] = (data['death'] / data['POPESTIMATE2019']) * 100
    data['mortality_per_cent'] = (data['death'] / data['positive']) * 100
    data['tested_per_cent'] = (data['totalTestResults'] / data['POPESTIMATE2019']) * 100
    data['positive_negative_per_cent'] = (data['positive'] / data['negative']) * 100
    data['new_test_positive_per_cent'] = (data['positiveIncrease'] / data['totalTestResultsIncrease']) * 100

    show_info(data)

    return data



def output(data):
    debug("output data", data)
    # graph data
    fig, ax = plt.subplots()
    for state in STATES:
        ax.plot(data[data.state == state].date, data[data.state == state].positive_increase_per_cent.rolling(7).mean(), label = state)
    ax.set(title='Positive increase as % of population (rolling 7 day average)')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.legend()
    plt.show()

def show_info(data):
    debug('column data:', data.columns)
    debug('data types:', data.dtypes)
    debug('DataFrame size:', data.size)
    debug('DataFrame shape:', data.shape)

def run():


    raw_data = load_data_and_save(COVID_DATA_URL, COVID_OUTPUT_FILE_NAME)
    data_clean = analyse(raw_data)
    output(data_clean)

run()
