from itertools import groupby
import json
from EmailSubsystem.EmailSender import send_email

def create_stats(template_data):
    stations = len(template_data["stations"])
    stats = {"created":0}
    stats |= {f"Stage #{index}":0 for index in range(stations)}
    stats["completed"] = 0
    stats["failed"] = 0
    return json.dumps(stats)


def complition_email_send(user):
    username = user.fullname
    email = user.email
    subject = 'An update about one of your documents'
    msg = f'''
        Hello {username}, a document that you have created has been completed.\n
        Please take your time to check it out in our system.
    '''
    send_email(email,msg,subject)

def fail_email_send(user):
    username = user.fullname
    email = user.email
    subject = 'An update about one of your documents'
    msg = f'''
        Hello {username}, a document that you have created has been rejected along the way.\n
        Please take your time to check it out in our system.
    '''
    send_email(email,msg,subject)