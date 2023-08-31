import requests, pandas as pd,sqlite3,constants

headers = {'User-Agent': ''} #must pass a user agent in the header to retrieve data
url = "https://www.parkrun.org.uk/special-events/"

html = requests.get(url, headers=headers).content
#print (html)

df_list = pd.read_html(html)
df = df_list[0][['Event','Region']].rename(columns={'Event':'eventLongName','Region':'region'}) #we need only these two fields and lets rename them
df=df[~df["eventLongName"].str.contains(' junior', na=False)] #remove rows that contains ' junior'
print (df)


conn = sqlite3.connect(constants.databaseLocation)
df.to_sql('regions',conn,if_exists='replace',index=False)