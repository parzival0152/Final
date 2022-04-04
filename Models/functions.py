from itertools import groupby
import json

def parse_response(form_response):
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
                    "value":"",
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
    stats = {str(index):0 for index in range(len(stations))}
    stats["created"] = 0
    stats["completed"] = 0
    return json.dumps(template),json.dumps(stats)
    