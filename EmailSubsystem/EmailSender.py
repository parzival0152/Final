import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#The mail addresses and password
SENDER_ADDRESS = 'ilay.tzu@gmail.com'
SENDER_PASS = 'gcyyaigaiiubncxi'

def send_email(receiver_address:str , msg:str) -> None:
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver_address
    message['Subject'] = 'Schedualed update about your pending documents'   #The subject line
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