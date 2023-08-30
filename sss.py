headers = {'placeholder': ''} #we need to supply a header to get a response, the contents dont matter

import requests, pandas as pd,re
import constants
from scrapy import Selector

url = constants.powerOften
html = requests.get(url, headers=headers).text

sel = Selector( text = html )
divs = sel.xpath( '//span[@id="cphBody_lblBody"]/p[6]' ).extract() #pull the data from the span element where id = cphBody_lblBody, then look to the 6th p element from that block

dict = {} #create a dictionary to output the data to

for x in divs[0].splitlines():#we are going to process each line of text
    try:
        matches = re.findall(r'\d+\s(\D+)\s(-?\d+.\d)',x) #look for the following  "one or more digits followed by a space, capture the next set of non-digit chars followed by a space, then capture the next numerber which contains a decimal point and may be negative"
        #print (matches[0][0],matches[0][1])
        event = matches[0][0] #grab the event name
        sss = matches[0][1] #grab the sss - standard scratch score value
        dict[event] = sss #add the data to a dictionary
    except Exception as error: #not all lines contain regex matches and so no data to store
        print (error)

print (dict)    