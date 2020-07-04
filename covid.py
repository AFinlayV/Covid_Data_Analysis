import pandas as pd
import urllib
import matplotlib.pyplot as plt


def load_data():

    url = f'https://covidtracking.com/api/v1/states/current.json'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    file = open('covid_data_current.json', 'w')
    file.write(data)
    file.close()

    url = f'https://covidtracking.com/api/v1/states/current.json'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    file = open('covid_data_ts.json', 'w')
    file.write(data)
    file.close()

    data_cur = pd.read_json('covid_data_current.json')
    state_pop = pd.read_csv('SCPRC-EST2019-18+POP-RES.csv')
    state_abrev = pd.read_json('state_abrev.json')

    return data_cur, state_pop, state_abrev


def normalize(data_cur, state_pop, state_abrev):
    #load relavent data
    pop = state_pop.get(['NAME', 'POPESTIMATE2019'])
    cur = data_cur.get(['date','state','positive','negative','death'])
    ab = state_abrev

    # Convert date format in daily and current data
    #cur['date'] =  pd.to_datetime(cur['date'], format='%Y%m%d', errors='ignore')


    # Merge state population data with state abreviations
    states = pd.merge(ab, pop, left_on ="name", right_on = "NAME")

    # Merge Population data into current data using state abreviation data

    cur = pd.merge(states, cur, left_on = 'abbreviation', right_on = 'state')
    cur = cur.get(['date','state','POPESTIMATE2019','positive','negative','death'])
    # Merge Population data into daily data using state abreviation data

    return cur


def analyse(cur):
    # calculate per 100k for current values
    pos_per = cur['positive']/cur['POPESTIMATE2019']*100000
    cur['positive per 100k'] = pos_per
    neg_per = cur['negative']/cur['POPESTIMATE2019']*100000
    cur['negative per 100k'] = neg_per
    death_per = cur['death']/cur['POPESTIMATE2019']*100000
    cur['death per 100k'] = death_per
    death_per_pos = cur['death']/cur['positive']*100
    cur['mortality %'] = death_per_pos

    return cur


def output(data):

    print(data)
    data.plot.bar(x='state', y=['positive per 100k'], rot=0, figsize = (14, 14))
    plt.show()


    return data




def main():
    data_cur, state_pop, state_abrev = load_data()
    table = normalize(data_cur, state_pop, state_abrev)
    data = analyse(table)
    output(data)


main()
