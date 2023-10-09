#scan a selection of a urls, if any new data appears report back to user via email

import requests
import pandas
import sqlite3
from parsel import Selector

import constants
import functions

headers = {'User-Agent': ''} #passing user agent is required to access html

def processEventPages():

    #list the urls that we are interested in
    url = ['https://wiki.parkrun.com/index.php/Category:Channel_Islands_Events',
        'https://wiki.parkrun.com/index.php/Category:East_Midlands_Events',
        'https://wiki.parkrun.com/index.php/Category:East_of_England_Events',
        'https://wiki.parkrun.com/index.php/Category:Falkland_Islands_Events',
        'https://wiki.parkrun.com/index.php/Category:Greater_London_Events',
        'https://wiki.parkrun.com/index.php/Category:North_East_England_Events',
        'https://wiki.parkrun.com/index.php/Category:North_West_England_Events',
        'https://wiki.parkrun.com/index.php/Category:Northern_Ireland_Events',
        'https://wiki.parkrun.com/index.php/Category:Scotland_Events',
        'https://wiki.parkrun.com/index.php/Category:South_East_England_Events',
        'https://wiki.parkrun.com/index.php/Category:South_West_England_Events',
        'https://wiki.parkrun.com/index.php/Category:Wales_Events',
        'https://wiki.parkrun.com/index.php/Category:West_Midlands_Events',
        'https://wiki.parkrun.com/index.php/Category:Yorkshire_and_the_Humber_Events']

    list = []

    for x in url: #for each url

        html = requests.get(x,headers=headers).content #get the html

        sel = Selector(str(html)) #create a selector object from the html

        extracted = sel.xpath('//*/div[@class="mw-content-ltr"]//*/a/text()') 
        #extract the bits we are interested in, in this case find each div element with the specified class
        #and pull out the url text

        for x in extracted: #add each bit we extracted to our empty list
            list.append(x.extract())

    list = [ functions.unescape(x) for x in list if "junior parkrun" not in x]  
    #we get some funny replacements when we work this way eg ' gets replaced with "\xe2\x80\x99" 
    #so we will deal with that, and also remove and junior parkruns, which we arent intereste in

    list.sort() #not necersary but made it easier for me when debugging to find values

    #print (list)

    df = pandas.DataFrame(list) #put the list into pandas - main reason: I like pandas's method for saving data to a db
    df.columns = ['eventName'] #name the data frame column

    #print (df)

    databaseLocation = constants.databaseLocation
    conn = sqlite3.connect(databaseLocation)

    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count FROM sqlite_master WHERE type='table' AND name='previousEvents'")
    #we are going to pull a value out of the db rather than execute a series of commands so we use execute
    
    prevTableCount = cursor.fetchall()
    #store the result of the query

    cursor.execute("SELECT count(*) as count FROM sqlite_master WHERE type='table' AND name='currentEvents'")
    currentTableCount = cursor.fetchall()

    #print(prevTableCount[0][0])
      
    if currentTableCount[0][0] > 0:
        cursor.executescript("DROP TABLE IF EXISTS previousEvents; CREATE TABLE  previousEvents AS  SELECT * FROM currentEvents;")
        #copy the current table to become the previous tale

    df.to_sql('currentEvents',conn,if_exists='replace',index=False)
    #upload the data frame to your database
    
    if prevTableCount[0][0] > 0: #run these commands if the previousEvents table exists
        #cursor.executescript("delete from previousEvents where eventname IN ('Wythenshawe parkrun','Wyre Forest parkrun');")
        #used for testing code so there will always be a new Event to report
        #We are not fetching values back, we are running a script so we use executescript rather than execute
        cursor.execute('select EventName from currentEvents EXCEPT select EventName from previousEvents')
        #sql query to identify any new events
        records = cursor.fetchall()
        #print (records)
    
        if len(records) > 0:

            emailBody = ''

            for x in records: #for each new event
                print (x[0])
                emailBody += x[0] + ', ' #construct an email body
                
            #print (emailBody[:-2])
            functions.sendEmail('New parkruns',emailBody[:-2]) #send the email
        
if __name__ == '__main__':
    processEventPages()