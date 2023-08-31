### Project Overview

parkrun is a free weekly timed 5km event. Hundreds of events are held all over the UK (and abroad) at 9AM every Saturday morning.

This project uses information obtained from parkrun and other sources to populate a database to show the users where events are held, travel times and distances and difficulty.

Some of the libraries employed to obtain this information include pandas, requests, numpy, re, Selector, sqlite3 to perform functions such as web scraping, regular expression data extraction, data frame manipulation and data storage.

### Files

**Sample Data** This folder contains files that are referenced in the project from the internet. In the event that the files are no longer available online, files can be located here and rehosted to allow the code to run successfully.

**constants.py** Urls for web resources can be found here. The athlete ID (provided by parkrun) and home coordinates can be modified here to personalise the experience provided by the project. We can also specify the location for the sqlite3 database.

**database.sql** Database view creation scripts, the allEvents view will be the most important window for viewing data once all datasets have been created

**function.py** Functions referenced throughout the project that can be reused in multiple places

**processCompletedEvents.py** Save a list of events that the athlete has completed to the database

**processCounty.py** Get local authority and county details from findthatpostcode.com for each UK event

**processDrivingDistance.py** Calculate driving times and distances to each event from the athlete's home using openstreetmap.

**processEvents.py** Process the events.json file, this creates a narrower version of the table created by processCounty.py

**processRegions.py** Each parkrun belongs to a region, this script will retrieve those regions and save the data to the database

**processSSS.py** The Standard Scratch Score (SSS) indicates the level of difficulty that an event has as calculated by an independent data scientist. This file will grab those scores and save them to the database.

