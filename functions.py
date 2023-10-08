import pickle
import base64
import googleapiclient.discovery

import constants

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def unescape(s):
    #the requests.get function will escape certain chars
    #so this will just reverse that
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace (r"\xe2\x80\x99", "'")
    return s

def sendEmail(subject,body):

    pickle_path = constants.emailPicklePath
    creds = pickle.load(open(pickle_path, 'rb'))
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)

    my_email = constants.email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'{my_email}'
    msg['To'] = f'{my_email}'
    msgPlain = body
    msg.attach(MIMEText(msgPlain, 'plain'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    message1 = body
    message = (
        service.users().messages().send(
            userId="me", body=message1).execute())
    print('Message Id: %s' % message['id'])