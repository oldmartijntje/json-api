import os
import json
import datetime
import uuid

title = input("Blog title: ")
url = input("Blog URL: ")
description = input("Blog description: ")



def startup():
    path = input("Path to md file: ")
    try:
        f = open(path, "r")
        data = f.read()
        f.close()
        try:
            file = open(location, "r")
        except:
            file = open('.' + location, "r")
        jsonData = file.read()
        file.close()
        try:
            file = open(location, "w")
        except:
            file = open('.' + location, "w")
        jsonData = json.loads(jsonData)
        id = str(uuid.uuid4())
        jsonData['blogs'].append({
            "title": title,
            "url": url,
            "description": description,
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "id": id
        })
        jsonData['lastUpdate'] = datetime.datetime.now().strftime("%d/%m/%Y")
        file.write(json.dumps(jsonData, indent=4))
        file.close()
        nextPath = jsonData['fullBlogsLocation']['local']
        try:
            nextFile = open(nextPath, "r")
        except:
            nextFile = open('.' + nextPath, "r")
        jsonContent = nextFile.read()
        jsonContent = json.loads(jsonContent)
        nextFile.close()
        try:
            nextFile = open(nextPath, "w")
        except:
            nextFile = open('.' + nextPath, "w")
        jsonContent[id] = {
            "markdown": data,
            "id": id,
            "date": datetime.datetime.now().strftime("%d/%m/%Y")
        }
        nextFile.write(json.dumps(jsonContent, indent=4))
        nextFile.close()
        

    except Exception as e:
        print(e)
        startup()
location = './docs/api/globalData/myBlog.json'

startup()