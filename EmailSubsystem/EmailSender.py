import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from dotenv import load_dotenv

# load setting from the file called .env to the enviroment variables
load_dotenv()

#The mail addresses and password
SENDER_ADDRESS = environ['SENDER_ADDRESS']
SENDER_PASS = environ['SENDER_PASS']

def send_email(receiver_address:str , msg:str, subject:str = 'Schedualed update about your pending documents'):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver_address
    message['Subject'] =subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(msg, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(SENDER_ADDRESS, SENDER_PASS) #login with mail_id and password
    text = message.as_string()
    try:
        session.sendmail(SENDER_ADDRESS, receiver_address, text)
    finally:
        session.quit()
    print(f'Mail Sent to {receiver_address}')