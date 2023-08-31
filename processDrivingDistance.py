#get the driving distance from 'home' for all uk events that havent yet been completed

import pandas as pd
import numpy as np
import geopy.distance
import processCompletedEvents,constants,processEvents
import sqlite3

def get_distance(start,end):
    
    #get the driving distance between two points using openmap api

    from urllib.request import urlopen
    import json

    url = "http://router.project-osrm.org/route/v1/driving/"+str(start)+';'+str(end)+"?overview=false"
    #print(url)
    response = urlopen(url)
    jsontxt = json.loads(response.read())
    #print(jsontxt)
    duration = (jsontxt['routes'][0]['legs'][0]['duration'])
    distance = (jsontxt['routes'][0]['legs'][0]['distance'])
    return (duration,distance)

runlist = processCompletedEvents.getRuns(constants.athleteId).event.drop_duplicates().to_frame() #get a list of all runs that have been completed

home = constants.home #this will be our start point

homeX = home[0] #split out the long and latitude
homeY = home[1]

ukruns = processEvents.parseEventFile().query('seriesid==1 and countryCode == 97')[['coordinates','eventShortName','longitude','latitude']] #series id = 1 non junior event, country 97 = uk
ukruns = ukruns.merge(runlist,left_on='eventShortName',right_on='event',how='left') 
not_run = ukruns.query('event!=event').drop('event',axis=1) #remove the nulls, we only want to calc distances for events we havent been to yet
not_run["straightLineDistkm"] = not_run.apply(lambda row: geopy.distance.geodesic(row.coordinates,home).km, axis=1) #get the straight line distance between each run and home in km
#not_run = not_run.query('straightLineDistkm<100')
not_run["roadDistance"] = not_run.apply(lambda row: get_distance(str(homeY) + ',' + str(homeX), str(row.longitude) + ',' + str(row.latitude)), axis=1) #get the travel time and distance
not_run["travelTimeMins"] = not_run.apply(lambda row: row.roadDistance[0]/60, axis=1) #extract the travel time
not_run["travelDistanceKM"] = not_run.apply(lambda row: row.roadDistance[1]/1000, axis=1) #extract the distance
not_run = not_run.drop(['coordinates','roadDistance'],axis=1) #drop the unneeded columns
not_run.sort_values(by=["travelTimeMins"],inplace=True) #sort out data frame
not_run.index = np.arange(1, len(not_run) + 1) #recreated the index 1,2,3,....
not_run[['straightLineDistkm','travelTimeMins', 'travelDistanceKM']] = not_run[['straightLineDistkm','travelTimeMins', 'travelDistanceKM']].round(2) #round some of the values

#print(not_run)

databaseLocation = constants.databaseLocation #store in db
conn = sqlite3.connect(databaseLocation)
not_run.to_sql('drivingDistances',conn,if_exists='replace',index=False)