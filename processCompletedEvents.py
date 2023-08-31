import requests
import pandas as pd
import sqlite3
import constants

#download personal run completion data and store in db

def getRuns(athleteNumber):
    headers = {'User-Agent': ''} #A user agent is required to access data

    url = "https://www.parkrun.org.uk/parkrunner/"+str(athleteNumber)+"/all/"

    html = requests.get(url,headers=headers).content
    df_list = pd.read_html(html) #we are interested in the final dataframe
    df = df_list[-1]\
                    .rename(columns={'Event':'event',\
                                     'Run Date':'runDate',\
                                     'Run Number':'runNumber',\
                                     'Pos':'pos',\
                                     'Time' : 'time',\
                                     'Age Grade':'ageGrade',\
                                     'PB?':'pb'\
                                     })
                                                                                         
    df['runDate'] = pd.to_datetime(df['runDate'], format = '%d/%m/%Y')
    df["ageGrade"] = df.apply(lambda row: str(row['ageGrade'][0:-1]), axis=1) #remove the final charecter from this field value (%)
    df['ageGrade'] = pd.to_numeric(df['ageGrade'])

    return df



if __name__ == '__main__':
    completedRuns = getRuns(constants.athleteId)
    conn = sqlite3.connect(constants.databaseLocation)
    completedRuns.to_sql('completedRuns',conn,if_exists='replace',index=False)