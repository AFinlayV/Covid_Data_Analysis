import pandas as pd
import urllib
import matplotlib.pyplot as plt

STATE_POP_DATA='SCPRC-EST2019-18+POP-RES.csv'
STATE_ABREV='state_abrev.json'
COVID_DATA_URL='https://covidtracking.com/api/v1/states/daily.json'
COVID_OUTPUT_FILE_NAME='covid_data.json'
GET_FIELDS_STATE=['NAME', 'POPESTIMATE2019']
GET_FIELDS_COVID=['date','state','positive','negative','death', 'positiveIncrease','negativeIncrease', 'totalTestResults']
ALL_FIELDS=['date','state','POPESTIMATE2019','positive','negative','death', 'positiveIncrease','negativeIncrease','totalTestResults']
OUTPUT_LIST=['mortality %', 'death %']
STATES=['NC', 'SC']
if 'all' in STATES:
    STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
DEBUG=True
LOAD_NEW_DATA=False

class covid:
    '''
    Takes in:
    self -a pandas dataframe
    state -2 letter state abreviation
    field - column name for data to be returned

    returns:
    returns a dataframe of time series data for the requested column
    '''
    def __init__(self, state, field):
        debug('self type:', type(self))
        debug('state type:', type(state))
        debug('field type:', type(field))


        #data = self.query(f'state == "{state}"')
        #ts_data = data
        #print(type(data), type(ts_data))
        #return ts_data
    def ts(self, state, date_start, date_end, field):
        ts_data = [self, state, date_start, date_end, field]
        return ts_data

    def cur(self, state):
        cur_data = [self, state]
        return cur_data






def debug(message, data):
    if DEBUG == True:
        print(message, data)

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
    else:
        print(f'New data not loaded, reading from {output_file_name}. Set LOAD_NEW_DATA=True to load data')


def parse_to_pd(data_file_name):
    print(f'Reading data from {data_file_name}...')
    data=pd.read_json(data_file_name)
    debug('column data:', data.columns)
    data['date']=pd.to_datetime(data['date'], format='%Y%m%d')
    state_pop=pd.read_csv(STATE_POP_DATA)
    state_abrev=pd.read_json(STATE_ABREV)
    states=pd.merge(state_abrev, state_pop, left_on="name", right_on="NAME")
    data=pd.merge(states, data.get(GET_FIELDS_COVID), left_on='abbreviation', right_on='state')
    data=data.get(ALL_FIELDS)
    debug('Parsed data:', data)
    debug('columns list:', data.columns)
    return data

def load_states(data):
    print('Loading states...')
    state_data_lst=[]
    for state in STATES:
        print(state)
        state_data_lst.append(state_data(data, state))
    debug('loaded states:', state_data_lst)
    return state_data_lst

def state_data(data, state):
    state_data= data.query(f'state == "{state}"')
    debug(f'Loaded state data list({state}): \n', state_data)
    return state_data

def analyse(data):
    for state in data:
        state_name = state['state']
        print(f'Calculating percentages for {state_name}...')
        state['positive %'] = (state['positive'] / state['POPESTIMATE2019']) * 100
        state['negative %']  = (state['negative'] / state['POPESTIMATE2019']) * 100
        state['death %'] = (state['death'] / state['POPESTIMATE2019']) * 100
        state['mortality %'] = (state['death'] / state['positive']) * 100
        state['tested %'] = (state['totalTestResults'] / state['POPESTIMATE2019']) * 100
        state['positive/negative %'] = (state['positive'] / state['negative']) * 100
        state['new test positive %'] = (state['positiveIncrease'] / state['negativeIncrease']) * 100
        debug(f'Analysed {state} data:', data)
    return data

def output(data):
    if DEBUG:
        print(type(data))
    print(data)

def graph(data, states):

    return data

def run():


    load_data_and_save(COVID_DATA_URL, COVID_OUTPUT_FILE_NAME)

    data = parse_to_pd(COVID_OUTPUT_FILE_NAME)
    debug('data after parse:', type(data))
    obj_data = covid(data)
    debug('data from object', type(obj_data))
    data = obj_data.ts('SC', '2020-03-03', '2020-07-10', 'positive')
    debug('Time series data:', data)
    data = obj_data.cur('SC')
    debug('Current data:', data)
    #print(data2)
    #data = load_states(data)
    #data = analyse(data)
    #output(data)
    #graph(data, STATES)

run()
