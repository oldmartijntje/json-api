import os
import subprocess
import datetime
import json

title = 'OldMartijntje\'s Static API'

def list_files_and_folders(directory):
    # Get list of all files and folders in the directory
    contents = os.listdir(directory)
    
    # Separate files and folders
    files = []
    folders = []
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            files.append(item)
        elif os.path.isdir(item_path):
            folders.append(item)
    
    return files, folders

def createHTML(files, folders, filePath):
    # Create the HTML content
    content = '<h1>Index of ' + filePath + '</h1>\n'
    if (filePath != startingPos):
        content += '<strong><a href="../index.html" style="margin-bottom:1rem">[parent directory]</a></strong>\n'
    content += '<strong><a href="./index.json" style="margin-bottom:1rem">.json index</a></strong>\n'
    for folder in folders:
        if folder == folders[0]:
            content += '<h2>Folders</h2>\n'
            content += '<ul>\n'
        content += '<li><strong><a href="./'+folder+'/index.html">' + filePath + '/' +folder + '</a></strong>'
        content += '</li>\n'
        if folder == folders[-1]:
            content += '</ul>\n'
    for file in files:
        if file == files[0] and len(files) > 2:
            content += '<h2>Files</h2>\n'
            content += '<ul>\n'
        if file != 'index.html' and file != 'index.json':
            content += '<li><a href="./' + file + '">' + file + '</a></li>\n'
        if file == files[-1]:
            content += '</ul>\n'
    content += '</ul>'
    
    return content

def createJson(files, folders, filePath):
    # Create the JSON content
    jsonFile = {}
    jsonFile['path'] = filePath
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


def saveHTML(content, filePath, files, folders):
    webPathPatst = filePath.split('./docs/')
    if len(webPathPatst) > 1:
        webPath = webPathPatst[1]
    else:
        webPath = ""
    webPath = 'https://api/oldmartijntje.nl/' + webPath
    start = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta property="og:title" content="api.oldmartijntje.nl">
    <meta property="og:description" content="OldMartijntje's API. View this folder: \"{filePath}\"\nIt contains {len(files)-2} files and {len(folders)} folders.">
    <meta property="og:image" content="https://api.oldmartijntje.nl/api/oldmartijntje.nl/assets/images/mii.png">
    <meta property="og:url" content="{webPath}">
    <meta property="og:type" content="website">
</head>
<style>
    body {{
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
    }}

    a, a:visited {{
        color: #67acf8;
    }}

    footer {{
        width: calc(100% - 2rem);
        background-color: #1f1f1f;
        padding: 1rem;
        text-align: center;
        height: 12rem;
    }}

    .content {{
        margin: 1rem;
        flex-grow: 1;
        overflow-y: scroll;
    }}
</style>

<body>
<div class="content">
'''

    end = '''</div>
    <footer>
        <h2>OldMartijntje &copy;</h2>
        <a href="https://oldmartijntje.nl">My Website</a>
        <a href="https://docs.oldmartijntje.nl">My Digital Garden</a>
        <p>Generated this index with a Python script</p>
        <p>Last updated: ''' + str(datetime.datetime.now().strftime('%d/%m/%y %H:%M%p')) + '''</p>
    </footer>
</body>

</html>'''
    # Save the HTML content to a file
    with open(filePath + '/index.html', 'w') as file:
        file.write(start + content + end)

def findIndented(folders, currentPath, files):
    html = createHTML(files, folders, currentPath)
    saveHTML(html, currentPath, files, folders)
    json = createJson(files, folders, currentPath)
    saveJson(json, currentPath)
    for x in range(len(folders)):
        if folders[x] == 'node_modules':
            folders.pop(x)
        else:
            newPath = currentPath + '/' + folders[x]
            files, subfolders = list_files_and_folders(newPath)
            findIndented(subfolders, newPath, files)
    

startingPos = './docs'
try:
    files, folders = list_files_and_folders(startingPos)
except:
    files, folders = list_files_and_folders('.'+ startingPos)

findIndented(folders, startingPos, files)

# commit using subprocess
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'Updating Data.'])
subprocess.run(['git', 'push'])
