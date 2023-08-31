#quickly ingest the events file, without county data

import sqlite3
import constants

def parseEventFile():

    import json,requests,pandas as pd 

    #Download the events.json file and store in a sqlite3 db

    headers = {'placeholder': ''} #we need to supply a header to get a response, the contents dont matter
    url = "https://images.parkrun.com/events.json"


    response = requests.get(url,headers=headers).text
    responseJson = json.loads(response)
    responseJsonNormalized = pd.json_normalize(responseJson['events']['features'])[['geometry.coordinates',\
                                                                                    'properties.eventname',\
                                                                                    'properties.EventLongName',\
                                                                                    'properties.EventShortName',\
                                                                                    'properties.countrycode',\
                                                                                    'properties.seriesid',\
                                                                                    'properties.EventLocation']] \
        .rename(columns={'properties.eventname':'eventName',\
                            'properties.EventLongName':'eventLongName',\
                            'properties.EventShortName':'eventShortName',\
                            'geometry.coordinates':'coordinates',\
                            'properties.countrycode':'countryCode',\
                            'properties.seriesid':'seriesid',\
                            'properties.EventLocation':'eventLocation'})

    #the coordinates are stored as a list, so we are going to seperate them out
    responseJsonNormalized["longitude"] = pd.to_numeric(responseJsonNormalized.apply(lambda row: str(row.coordinates[0]), axis=1))
    responseJsonNormalized["latitude"] = pd.to_numeric(responseJsonNormalized.apply(lambda row: str(row.coordinates[1]), axis=1))
    responseJsonNormalized["coordinates"] = responseJsonNormalized.apply(lambda row: str(row.latitude) + ',' +str(row.longitude), axis=1)

    return responseJsonNormalized


if __name__ == '__main__': #we dont want to run this unless we specifically run the file- eg we dont want am import to trigger below code

    databaseLocation = constants.databaseLocation
    responseJsonNormalized = parseEventFile()
    conn = sqlite3.connect(databaseLocation)
    responseJsonNormalized.to_sql('eventsBasic',conn,if_exists='replace',index=False)