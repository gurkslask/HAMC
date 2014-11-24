import os
import datetime
import sqlite3 as lite
import time
import pandas as pd
#import bokeh.plotting as pt
import json


def load_data():
    dir = 'sensors/'
    os.chdir(dir)
    tid = time.time()
    d = {}
    ds = {}
    lines = []
    for folder in os.listdir():
        d[folder] = {}
        ds[folder] = {}
        os.chdir(folder)
        for i in os.listdir():
            with open(i, 'r') as f:
                '''
                d[folder] = {
                    datetime.datetime.fromtimestamp(int(j.split('|')[0])):
                    j.split('|')[1].strip()
                    for j in f.readlines()
                }
                '''
                lines = f.readlines()
            try:
                for line in lines:
                    d[folder][datetime.datetime.fromtimestamp(int(line.split('|')[0]))] = line.split('|')[1].strip()
            except IndexError as e:
                print(e)
                pass


        os.chdir('..')

    os.chdir('..')
    os.chdir('..')
    print('it took {} sec to load data'.format(time.time()-tid))

    return d


def insert_data(d):
    name_dikt = {
        '28-00000523a1cb': 'VS1_GT1',
        '28-00000524056e': 'VS1_GT2',
        '28-0000052407e0': 'VS1_GT3',
        '28-00000523ab8e': 'SUN_GT1',
        '28-0000052361be': 'SUN_GT2'
    }

    tid = time.time()
    conn = lite.connect('/home/pi/Projects/Home-automation/data.db')
    with conn:
        cur = conn.cursor()
        for i in d.keys():
            if i in name_dikt:
                namn = name_dikt[i]
            else:
                namn = i
            print(namn)
            #cur.execute('DROP TABLE IF EXISTS ' + str(namn))
            try:
                cur.execute('select * from ' + str(namn))
            except lite.OperationalError:
                        cur.execute('CREATE TABLE ' + str(namn) + '(Time TEXT, Temp REAL)')
            for i in d:
                for j in d[i]:
                    cur.execute(
                        "INSERT INTO " + namn + " VALUES(?,?)", (j, d[i][j])
                    )

        print(
            'Det tog {} sek att lassa in data i SQL'.format(time.time()-tid)
        )


def read_data():
    tid = time.time()
    conn = lite.connect('test.db')
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM SUN_GT1")
        data = cur.fetchall()

    print('Entries: {}'.format(len(data)))
    print(
        '{} seconds to read'.format(time.time()-tid)
    )
    return data



def load_into_pandas(data):
    df = pd.DataFrame(data, columns=['time', 'Temp'])
    print(df['time'][:5])
    df['time'] = df['time'].astype('datetime64[ns]')
    df = df.sort(['time'])
    print(df['time'][:5])
    df.to_csv('panda_csv')
    return(df)


def plot(df):
    tid = time.time()
    # output to static HTML file
    pt.output_file("lines.html")
    pt.figure(x_axis_type='datetime')
    pt.line(df['time'], df['Temp'])
    print(
        '{} seconds to plot'.format(time.time()-tid)
    )

    pt.show()


def LoadAndSQL():
    dir = 'sensors/'
    os.chdir(dir)
    tid = time.time()
    d = {}
    for folder in os.listdir():
        os.chdir(folder)
        for i in os.listdir():
            d[folder] = {}
            print(i)
            with open(i, 'r') as f:
                lines = f.readlines()
            try:
                for line in lines:
                    d[folder][int(line.split('|')[0])] = line.split('|')[1].strip()
            except IndexError as e:
                print(e)
                pass
            insert_data(d)
            print('it took {} sec to load {} data'.format(time.time()-tid, folder))
            d = {}
            time.sleep(1)


        os.chdir('..')

    os.chdir('..')
    os.chdir('..')
    print('it took {} sec to load data'.format(time.time()-tid))



if __name__ == '__main__':
    #d = load_data()
    #insert_data(d)
    #data = read_data()
    #df = load_into_pandas(data)
    #plot(df)
    LoadAndSQL()
