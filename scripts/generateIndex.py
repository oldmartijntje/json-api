import os
import subprocess
import datetime
import json
import tkinter as tk
from tkinter.messagebox import showerror




title = 'OldMartijntje\'s Static API'

def createSettingsJson():
    settings = {}
    settings['title'] = 'OldMartijntje\'s Static API'
    settings['startingFolder'] = './docs'
    settings['webPath'] = 'https://api.oldmartijntje.nl'
    settings['websiteIcon'] = 'https://api.oldmartijntje.nl/api/oldmartijntje.nl/assets/images/mii.png'
    settings['embedImage'] = 'https://api.oldmartijntje.nl/api/oldmartijntje.nl/assets/images/mii.png'
    settings['embedTitle'] = 'api.oldmartijntje.nl'
    settings['embedDescription'] = 'OldMartijntje\'s API.'
    settings['commitOnRun'] = True
    settings['alwaysDefaultStyles'] = True
    settings['alwaysDefaultJavascript'] = True
    settings['footer'] = '''
    <h2>OldMartijntje &copy;</h2>
    <a href="https://oldmartijntje.nl">My Website</a>
    <a href="https://docs.oldmartijntje.nl">My Digital Garden</a>
    <p>Generated this index with <a href="https://github.com/oldmartijntje/json-api/blob/main/scripts/generateIndex.py">a python script</a></p>
    '''

    with open('./settings.json', 'w') as file:
        json.dump(settings, file, indent=4)
    
def loadSetting(settingsDict, key):
    try:
        return settingsDict[key]
    except:
        showerror('Error', 'The settings.json file is missing the ' + key + ' key. Please fill it in.')
        # open the folder in the file explorer
        os.system('explorer /select,settings.json')
        exit()

def loadStyling():
    try:
        if loadSetting(settings, 'alwaysDefaultStyles'):
            raise Exception
        styles = open('./styles.css', 'r').read()
    except:
        styles = '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #3c3c3c;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100svh;
    width: 100vw;
}

a, a:visited {
    color: #67acf8;
}

footer {
    width: calc(100% - 2rem);
    background-color: #1f1f1f;
    padding: 1rem;
    text-align: center;
    height: 12rem;
}

.buttons {
    display: flex;
    justify-content: start;
    gap: 1rem;
}

#title {
    word-wrap: break-word;
}

#indexName {
    text-decoration: underline;
}

header {
    width: calc(100% - 2rem);
    background-color: #1f1f1f;
    padding: 1rem;
}

.fileLine {
    display: flex;
    justify-content: space-between;
}

.fileLine * {
    overflow: hidden;
    word-wrap: break-word;
    flex: 1 1 20%;
}

.fileLine *:first-child {
    flex: 2 1 40%;
}  

.content {
    margin: 1rem;
    flex-grow: 1;
    overflow-y: scroll;
}

@media only screen and (max-width: 800px) {
    .fileLine {
        gap: 0.5rem;
    }

    .modifiedDate {
        display: none;
    }

}

'''
        with open('./styles.css', 'w') as file:
            file.write(styles)
            file.close()
    return styles

def loadJavascript():
    try:
        if loadSetting(settings, 'alwaysDefaultJavascript'):
            raise Exception
        javascript = open('./scripts.js', 'r').read()
    except:
        javascript = '''
        function timeSince(date) {
            const seconds = Math.floor((new Date() - date) / 1000);
            let interval = Math.floor(seconds / 31536000);

            if (interval >= 1) {
                return interval + " year" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 2592000);
            if (interval >= 1) {
                return interval + " month" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                return interval + " day" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 3600);
            if (interval >= 1) {
                return interval + " hour" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 60);
            if (interval >= 1) {
                return interval + " minute" + (interval > 1 ? "s" : "");
            }
            return Math.floor(seconds) + " second" + (seconds > 1 ? "s" : "");
        }

        function updateTimeSince() {
            const elements = document.querySelectorAll('.time-since');
            elements.forEach(element => {
                const datetimeString = element.getAttribute('data-value');
                const datetime = new Date(datetimeString);
                element.textContent = timeSince(datetime) + " ago";
            });
        }

        // Initial update
        updateTimeSince();

        // Update every minute
        setInterval(updateTimeSince, 60000);
        '''
        with open('./scripts.js', 'w') as file:
            file.write(javascript)
            file.close()
    return javascript

def loadSettingsJson():
    try:
        with open('./settings.json') as file:
            settings = json.load(file)
    except:
        settings = createSettingsJson()

        showerror('Error', 'No settings.json file found. A new one has been created. Please fill in the settings.')
        # open the folder in the file explorer
        os.system('explorer /select,settings.json')
        exit()

    return settings

def list_files_and_folders(directory):
    # Get list of all files and folders in the directory
    contents = os.listdir(directory)
    
    # Separate files and folders
    files = []
    folders = []
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            files.append({'name': item, 'size': os.path.getsize(item_path), 'lastModified': os.path.getmtime(item_path), 'type': item.split('.')[-1]})
        elif os.path.isdir(item_path):
            folders.append({'name': item, 'childrenAmount': len(os.listdir(item_path)), 'lastModified': os.path.getmtime(item_path)})
    return files, folders

def createHTML(files, folders, filePath):
    # Create the HTML content
    header = '<header>\n'
    header += '<h1 id="title">Index of <span id="indexName">' + ignoreBasePathInWebPath(filePath, settings) + '</span></h1>\n'
    header += '<div class="buttons">\n'
    if (filePath != startingPos):
        header += '<strong><a href="../index.html">[parent directory]</a></strong>\n'
        header += f'<strong><a href="{loadSetting(settings, 'webPath')}">[homepage]</a></strong>\n'
    header += '<strong><a href="./index.json">[json index]</a></strong>\n'
    header += '</div>\n'
    header += '</header>\n'
    content = ''
    for folder in folders:
        if folder == folders[0]:
            content += f'<h2>Folders ({len(folders)})</h2>\n'
            content += '<ul>\n'
        content += '<li class="fileLine"><strong><a href="./'+folder['name']+'/index.html">./' +folder['name'] + '</a></strong>'
        content += '<span class="childrenAmount" title="Amount of children">' + str(folder['childrenAmount']-2) + ' Items </span>'
        content += '<span class="time-since" data-value="' + str(datetime.datetime.fromtimestamp(folder['lastModified']).isoformat()) + '"></span>'
        content += '<span class="modifiedDate" title="Last Modified">' + str(datetime.datetime.fromtimestamp(folder['lastModified']).strftime('%d/%m/%y %H:%M%p')) + '</span>'
        content += '</li>\n'
        if folder == folders[-1]:
            content += '</ul>\n'
    for file in files:
        if file == files[0] and len(files) > 2:
            content += f'<h2>Files ({len(files)-2})</h2>\n'
            content += '<ul>\n'
        if file['name'] != 'index.html' and file['name'] != 'index.json':
            content += '<li class="fileLine"><a href="./' + file['name'] + '">' + file['name'] + '</a>'
            content += '<span class="size" title="File Size">' + str(fileSizeCalculator(file['size'])) + '</span>'
            content += '<span class="time-since" data-value="' + str(datetime.datetime.fromtimestamp(file['lastModified']).isoformat()) + '"></span>'
            content += '<span class="modifiedDate" title="Last Modified">' + str(datetime.datetime.fromtimestamp(file['lastModified']).strftime('%d/%m/%y %H:%M%p')) + '</span>'
            content += '</li>\n'
        if file == files[-1]:
            content += '</ul>\n'
    content += '</ul>'
    
    return header, content

def fileSizeCalculator(size):
    if size < 1000:
        return str(size) + ' bytes'
    elif size < 1000000:
        return str(size/1000) + ' KB'
    elif size < 1000000000:
        return str(size/1000000) + ' MB'
    elif size < 1000000000000:
        return str(size/1000000000) + ' GB'
    elif size < 1000000000000000:
        return str(size/1000000000000) + ' TB'
    else:
        return str(size) + ' bytes'

def createJson(files, folders, filePath):
    # Create the JSON content
    jsonFile = {}
    jsonFile['path'] = ignoreBasePathInWebPath(filePath, settings)
    jsonFile['folders'] = []
    jsonFile['files'] = []
    if (filePath != startingPos):
        jsonFile['parent'] = '../index.json'
    for folder in folders:
        jsonFile['folders'].append(folder)
    for file in files:
        jsonFile['files'].append(file)
    
    return jsonFile

def saveJson(content, filePath):
    # Save the JSON content to a file
    json.dump(content, open(filePath + '/index.json', 'w'), indent=4)


def ignoreBasePathInWebPath(filePath, settings):
    webPathPatst = filePath.split(loadSetting(settings, 'startingFolder'))
    if len(webPathPatst) > 1:
        webPath = webPathPatst[1]
    else:
        webPath = ""
    webPath = loadSetting(settings, 'webPath') + webPath
    return webPath


def saveHTML(header, content, filePath, files, folders):
    webPathPatst = filePath.split('./docs/')
    if len(webPathPatst) > 1:
        webPath = webPathPatst[1]
    else:
        webPath = ""
    webPath = loadSetting(settings, 'webPath') + webPath
    start = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="{loadSetting(settings, 'websiteIcon')}">
    <title>{title}</title>
    <meta property="og:title" content="{loadSetting(settings, 'embedTitle')}">
    <meta property="og:description" content="{loadSetting(settings, 'embedDescription')} View this folder: &quot;{ignoreBasePathInWebPath(filePath, settings)}&quot;\nIt contains {len(files)-2} files and {len(folders)} folders.">
    <meta property="og:image" content="{loadSetting(settings, 'embedImage')}">
    <meta property="og:url" content="{webPath}">
    <meta property="og:type" content="website">
</head>
<style>
    {styling}
</style>

<body>
'''
    
    middle = f'''<div class="content">
    '''

    end = f'''</div>
    <footer>
        {loadSetting(settings, 'footer')}
        <p>Last updated: {str(datetime.datetime.now().strftime('%d/%m/%y %H:%M%p'))}</p>
    </footer>
    <script>
    {javascript}
    </script>
</body>

</html>'''
    # Save the HTML content to a file
    with open(filePath + '/index.html', 'w') as file:
        file.write(start + header + middle + content + end)

def findIndented(folders, currentPath, files):
    header, content = createHTML(files, folders, currentPath)
    saveHTML(header, content, currentPath, files, folders)
    json = createJson(files, folders, currentPath)
    saveJson(json, currentPath)
    for x in range(len(folders)):
        if folders[x]['name'] == 'node_modules':
            folders.pop(x)
        else:
            newPath = currentPath + '/' + folders[x]['name']
            files, subfolders = list_files_and_folders(newPath)
            findIndented(subfolders, newPath, files)
    

settings = loadSettingsJson()
styling = loadStyling()
javascript = loadJavascript()

startingPos = loadSetting(settings, 'startingFolder')
try:
    files, folders = list_files_and_folders(startingPos)
except:
    files, folders = list_files_and_folders('.'+ startingPos)

findIndented(folders, startingPos, files)

if loadSetting(settings, 'commitOnRun'):

    # commit using subprocess
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Updating Data.'])
    subprocess.run(['git', 'push'])
