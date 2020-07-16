import pandas as pd
import urllib.request as urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pdb
from pandas.plotting import register_matplotlib_converters


STATE_POP_DATA='SCPRC-EST2019-18+POP-RES.csv'
STATE_ABREV='state_abrev.json'
COVID_DATA_URL='https://covidtracking.com/api/v1/states/daily.json'
COVID_OUTPUT_FILE_NAME='covid_data.json'
GET_FIELDS_STATE=['NAME', 'POPESTIMATE2019']
GET_FIELDS_COVID=['date','state','positive','negative','death', 'totalTestResults', 'deathIncrease','positiveIncrease','negativeIncrease', 'totalTestResultsIncrease', ]
ALL_FIELDS=['date','state','POPESTIMATE2019','positive','negative','death', 'totalTestResults', 'deathIncrease', 'positiveIncrease','negativeIncrease','totalTestResultsIncrease']
OUTPUT_LIST=['mortality %', 'death %']
STATES=['NC', 'SC', 'FL', 'CA', 'GA', 'VA', 'NY']
if 'all' in STATES:
    STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
DEBUG=True
SHOW_DATA=True
LOAD_NEW_DATA=True

def fancy_print(message, data):
    print(message, "\n---------------------------\n", data, "\n---------------------------\n")


def debug(message, data):
    if DEBUG:
        fancy_print(message, data)


def load_data_and_save(url, output_file_name):
    if LOAD_NEW_DATA == True:
        print(f'Loading data from {url} and saving to {output_file_name}...')
        uh = urllib.urlopen(url)
        data = uh.read().decode()
        file = open(output_file_name, 'w')
        file.write(data)
        file.close()
        debug('Loaded new raw data:', data)
        debug('Data saved to file:', output_file_name)
        data=pd.read_json(data)
        return data
    else:
        print(f'New data not loaded, reading from {output_file_name}. Set LOAD_NEW_DATA=True to load data')
        data=pd.read_json(output_file_name)
        return data


def analyse(data):

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
    data['death_per_cent'] = (data['deathIncrease'] / data['POPESTIMATE2019']) * 100
    data['mortality_per_cent'] = (data['death'] / data['positive']) * 100
    data['tested_per_cent'] = (data['totalTestResults'] / data['POPESTIMATE2019']) * 100
    data['positive_negative_per_cent'] = (data['positive'] / data['negative']) * 100
    data['new_test_positive_per_cent'] = (data['positiveIncrease'] / data['totalTestResultsIncrease']) * 100


    return data


def plot_time(data):
    # plot time series data for states in question
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    for state in STATES:
        ax1.plot(data[data.state == state].date, data[data.state == state].positive_increase_per_cent.rolling(7).mean(), label = state)
        ax2.plot(data[data.state == state].date, data[data.state == state].death_per_cent.rolling(7).mean(), label = state)

    ax1.set(title='New Covid-19 cases as % of pop (7 day average)')
    labels_x = ax1.get_xticklabels()
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=None, symbol='%', is_latex=False))
    plt.setp(labels_x, rotation=20, horizontalalignment='right')
    ax1.legend()

    ax2.set(title='New Covid-19 deaths as % of pop (7 day average)')
    labels_x = ax2.get_xticklabels()
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=None, symbol='%', is_latex=False))
    plt.setp(labels_x, rotation=20, horizontalalignment='right')
    ax2.legend()


def plot_cur(data):
    # plot current data on bar graph
    date_cur = str(data.date[0])
    cur_data = data[data.date == date_cur]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    for state in STATES:
        ax1.barh(state, cur_data.positive_increase_per_cent[data.state == state])
        ax2.barh(state, cur_data.death_per_cent[data.state == state])
    ax1.set(title=f'New Covid-19 cases as % of population for {date_cur[0:10]}')
    ax1.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=None, symbol='%', is_latex=False))
    ax2.set(title=f'New Covid-19 deaths as % of population for {date_cur[0:10]}')
    ax2.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=None, symbol='%', is_latex=False))


def output(data):
    register_matplotlib_converters()
    plot_time(data)
    plot_cur(data)
    show_info(data)
    plt.show()


def show_info(data):
    if SHOW_DATA:
        fancy_print('column data:', data.columns)
        fancy_print('data types:', data.dtypes)
        fancy_print('DataFrame size:', data.size)
        fancy_print('DataFrame shape:', data.shape)


def run():

    raw_data = load_data_and_save(COVID_DATA_URL, COVID_OUTPUT_FILE_NAME)
    data_clean = analyse(raw_data)
    output(data_clean)


run()
