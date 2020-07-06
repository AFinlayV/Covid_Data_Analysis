import pandas as pd
import urllib
import matplotlib.pyplot as plt

STATE_POP_DATA='SCPRC-EST2019-18+POP-RES.csv'
STATE_ABREV='state_abrev.json'
COVID_DATA_URL='https://covidtracking.com/api/v1/states/daily.json'
COVID_OUTPUT_FILE_NAME='covid_data.json'
GET_FIELDS_STATE=['NAME', 'POPESTIMATE2019']
GET_FIELDS_COVID=['date','state','positive','negative','death']
ALL_FIELDS=['date','state','POPESTIMATE2019','positive','negative','death']
OUTPUT_LIST=['mortality %', 'death %']
STATES=['NC', 'SC', 'FL']
DEBUG = False
LOAD_NEW_DATA=False

def debug(message):
    if DEBUG == True:
        print(message)

def load_data_and_save(url, output_file_name):
    print(f'Loading data from {url} and saving to {output_file_name}...')
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    file = open(output_file_name, 'w')
    file.write(data)
    file.close()
    debug(f'Loaded data: \n {data}')
    debug(f'Data saved to \n {output_file_name}')

def parse_to_pd(data_file_name):
    print(f'Reading data from {data_file_name}...')
    data=pd.read_json(data_file_name)
    data['date']=pd.to_datetime(data['date'], format='%Y%m%d')
    state_pop=pd.read_csv(STATE_POP_DATA)
    state_abrev=pd.read_json(STATE_ABREV)
    states=pd.merge(state_abrev, state_pop, left_on="name", right_on="NAME")
    data=pd.merge(states, data.get(GET_FIELDS_COVID), left_on='abbreviation', right_on='state')
    data=data.get(ALL_FIELDS)
    debug(f'Parsed data: \n {data}')
    return data

def load_states(data):
    state_data_lst=[]
    for state in STATES:
        state_data_lst.append(state_data(data, state))
    debug(f'loaded states: \n {state_data_lst}')
    return state_data_lst

def state_data(data, state):
    state_data= data.query(f'state == "{state}"')
    debug(f'Loaded state data list ({state}): \n {state_data}')
    return state_data

def analyse(data):
    debug(type(data))
    for state in data:
        print('Calculating percentages...')
        debug(type(state))
        state['positive %'] = (state['positive'] / state['POPESTIMATE2019']) * 100
        state['negative %']  = (state['negative'] / state['POPESTIMATE2019']) * 100
        state['death %'] = (state['death'] / state['POPESTIMATE2019']) * 100
        state['mortality %'] = (state['death'] / state['positive']) * 100
        state['tested %'] = ((state['positive'] + state['negative']) / state['POPESTIMATE2019']) * 100

        debug(f'Analysed {state} data: \n {data}')
    return data

def output(data):

    print(data)

def graph(data, states):

    return data

def run():
    if LOAD_NEW_DATA == True:
        load_data_and_save(COVID_DATA_URL, COVID_OUTPUT_FILE_NAME)
    data = parse_to_pd(COVID_OUTPUT_FILE_NAME)
    data = load_states(data)
    data = analyse(data)
    output(data)
    graph(data, STATES)

run()
