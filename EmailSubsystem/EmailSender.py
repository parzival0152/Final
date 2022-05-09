import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#The mail addresses and password
sender_address = 'ilay.tzu@gmail.com'
sender_pass = 'gcyyaigaiiubncxi'

def send_email(receiver_address:str , msg:str) -> None:
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Schedualed update about your pending documents'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(msg, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    try:
        session.sendmail(sender_address, receiver_address, text)
    finally:
        session.quit()
    print(f'Mail Sent to {receiver_address}')