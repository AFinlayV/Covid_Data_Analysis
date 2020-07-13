import pandas as pd
import urllib
import matplotlib.pyplot as plt

STATE_POP_DATA='SCPRC-EST2019-18+POP-RES.csv'
STATE_ABREV='state_abrev.json'
COVID_DATA_URL='https://covidtracking.com/api/v1/states/daily.json'
COVID_OUTPUT_FILE_NAME='covid_data.json'
GET_FIELDS_STATE=['NAME', 'POPESTIMATE2019']
GET_FIELDS_COVID=['date','state','positive','negative','death', 'totalTestResults', 'positiveIncrease','negativeIncrease', 'totalTestResultsIncrease', ]
ALL_FIELDS=['date','state','POPESTIMATE2019','positive','negative','death', 'totalTestResults', 'positiveIncrease','negativeIncrease','totalTestResultsIncrease']
OUTPUT_LIST=['mortality %', 'death %']
STATES=['all']
if 'all' in STATES:
    STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
DEBUG=True
LOAD_NEW_DATA=True

def debug(message, data):
    if DEBUG == True:
        print(message, "\n-----------------------------\n", data, "\n-----------------------------\n")

def load_data_and_save(url, output_file_name):
    if LOAD_NEW_DATA == True:
        print(f'Loading data from {url} and saving to {output_file_name}...')
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        file = open(output_file_name, 'w')
        file.write(data)
        file.close()
        debug('Loaded data:' , data)
        debug('Data saved to:', output_file_name)
        data=pd.read_json(data)
        return data
    else:
        print(f'New data not loaded, reading from {output_file_name}. Set LOAD_NEW_DATA=True to load data')
        data=pd.read_json(data)
        return data




def analyse(data):

    show_info(data)
    data['date']=pd.to_datetime(data['date'], format='%Y%m%d')
    state_pop=pd.read_csv(STATE_POP_DATA)
    state_abrev=pd.read_json(STATE_ABREV)
    states=pd.merge(state_abrev, state_pop, left_on="name", right_on="NAME")
    data=pd.merge(states, data.get(GET_FIELDS_COVID), left_on='abbreviation', right_on='state')
    data=data.get(ALL_FIELDS)


    data['positive %'] = (data['positive'] / data['POPESTIMATE2019']) * 100
    data['negative %']  = (data['negative'] / data['POPESTIMATE2019']) * 100
    data['death %'] = (data['death'] / data['POPESTIMATE2019']) * 100
    data['mortality %'] = (data['death'] / data['positive']) * 100
    data['tested %'] = (data['totalTestResults'] / data['POPESTIMATE2019']) * 100
    data['positive/negative %'] = (data['positive'] / data['negative']) * 100
    data['new test positive %'] = (data['positiveIncrease'] / data['totalTestResultsIncrease']) * 100

    show_info(data)
    return data



def output(data):
    print(data)
    # graph data

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
