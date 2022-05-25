from itertools import groupby
import json
from EmailSubsystem.EmailSender import send_email

def parse_response(form_response): # magic
    title = form_response.pop("title")
    description = form_response.pop("description")
    form_response = list(form_response.items())
    stations = []
    for stationId, fields in groupby(form_response, lambda s: s[0].partition('_')[0]):
        fields = dict([(identifier.replace(stationId+"_",""),value) for identifier,value in fields])
        name = fields.pop("Name")
        email = fields.pop("Email")
        fieldList = []
        for identifier,value in fields.items():
            if "text" in identifier:
                fieldList.append({
                    "type":"text",
                    "value":value
                })
            elif "input" in identifier:
                fieldList.append({
                    "type":"input",
                    "prompt":value,
                    "value":""
                })
            elif "image" in identifier:
                fieldList.append({
                    "type":"image",
                    "value":value
                })
        stations.append({
            "Name":name,
            "Email":email,
            "fields":fieldList
        })
    template = {
        "title":title,
        "description":description,
        "stations":stations
    }
    stats = {"created":0}
    stats |= {str(index):0 for index in range(len(stations))}
    stats["completed"] = 0
    stats["failed"] = 0
    return json.dumps(template),json.dumps(stats)
    
def complition_email_send(user) -> None:
    username = user.fullname
    email = user.email
    msg = f'''
        Hello {username}, a document that you have created has been completed.\n
        Please take your time to check it out in our system.
    '''
    send_email(email,msg)

def fail_email_send(user) -> None:
    username = user.fullname
    email = user.email
    msg = f'''
        Hello {username}, a document that you have created has been rejected along the way.\n
        Please take your time to check it out in our system.
    '''
    send_email(email,msg)