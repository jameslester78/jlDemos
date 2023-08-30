#quickly ingest the events file, without county data


import processEvents
import constants
import sqlite3


def getCountyData(url):

    import requests,json

    url = f"https://findthatpostcode.uk/points/{url}.json"
    html = requests.get(url).content
    d = json.loads(html)

    try:
        local_authority = d['included'][0]['attributes']['itl_name']
    except KeyError:
        local_authority  =  'unknown'  #if itl name doesnt exist then assign it 'unknown'

    try:
        county = d['included'][0]['attributes']['cty_name']
    except KeyError:
        county = 'unknown'  #if cty_name doesnt exist then assign it 'unknown'

    return (local_authority,county)




import json,pandas as pd

events = processEvents.parseEventFile()
#events = events.head(10)
events['localAuthority'] = None #create a new column, which we will populate later
events['county'] = None

for x in events.index: #each row in the df
    local_authority,county = getCountyData(events['coordinates'][x])
    events.at[x,'localAuthority'] = local_authority
    events.at[x,'county'] = county
    print (f'processed {x+1} out of {len(events.index)}') #report progres

print (events)
events.to_csv(r'C:\Users\James Lester\Documents\python\parkrun\SampleFile\pandas.txt', header=None, index=None, sep='\t')


databaseLocation = constants.databaseLocation

conn = sqlite3.connect(databaseLocation)
events.to_sql('events',conn,if_exists='replace',index=False)