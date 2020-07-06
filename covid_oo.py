class covid_data:
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

        url = f'https://covidtracking.com/api/v1/states/daily.json'
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        file = open('covid_data_ts.json', 'w')
        file.write(data)
        file.close()

        data_ts = pd.read_json('covid_data_ts.json')
        data_ts['date'] =  pd.to_datetime(data_ts['date'], format='%Y%m%d', errors='ignore')

        data_cur = pd.read_json('covid_data_current.json')
        data_cur['date'] =  pd.to_datetime(data_cur['date'], format='%Y%m%d', errors='ignore')

        state_pop = pd.read_csv('SCPRC-EST2019-18+POP-RES.csv')
        state_abrev = pd.read_json('state_abrev.json')

        return data_ts, data_cur, state_pop, state_abrev


    def normalize(data_ts, data_cur, state_pop, state_abrev):
        #load relavent data
        pop = state_pop.get(['NAME', 'POPESTIMATE2019'])
        cur = data_cur.get(['date','state','positive','negative','death'])
        ab = state_abrev
        ts = data_ts.get(['date','state','positive','negative','death'])
        # Convert date format in daily and current data
        #ts['date'] =  pd.to_datetime(ts['date'], format='%Y%m%d', errors='ignore')


        # Merge state population data with state abreviations
        states = pd.merge(ab, pop, left_on ="name", right_on = "NAME")

        # Merge Population data into current data using state abreviation data

        cur = pd.merge(states, cur, left_on = 'abbreviation', right_on = 'state')
        cur = cur.get(['date','state','POPESTIMATE2019','positive','negative','death'])
        ts = pd.merge(states, ts, left_on = 'abbreviation', right_on = 'state')
        ts = ts.get(['date','state','POPESTIMATE2019','positive','negative','death'])
        # Merge Population data into daily data using state abreviation data

        return ts, cur


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

    def analyse_ts(ts):
        # calculate per 100k for daily values
        pos_per = ts['positive']/ts['POPESTIMATE2019']*100000
        ts['positive per 100k'] = pos_per
        neg_per = ts['negative']/ts['POPESTIMATE2019']*100000
        ts['negative per 100k'] = neg_per
        death_per = ts['death']/ts['POPESTIMATE2019']*100000
        ts['death per 100k'] = death_per
        death_per_pos = ts['death']/ts['positive']*100
        ts['mortality %'] = death_per_pos

        return ts


    def output(data_cur, data_ts):

        print(data_cur, data_ts)
        data_cur.plot.bar(x='state',y=['mortality %', 'death per 100k'], rot=0, figsize = (14, 14), colormap='Dark2')
        #plots = {data_ts['date']:(data_ts.query('state == "FL"'),data_ts.query('state == "NY"'),data_ts.query('state == "NC"'))}
        #plt.plot([data_ts.query('state == "FL"')],[data_ts.query('state == "NY"')],[data_ts.query('state == "NC"')])
        plt.show()


        return data_cur, data_ts




    def main():
        data_ts, data_cur, state_pop, state_abrev = load_data()
        ts, cur = normalize(data_ts, data_cur, state_pop, state_abrev)
        data_cur = analyse(cur)
        data_ts = analyse_ts(ts)

        output(data_cur, data_ts)


    main()
