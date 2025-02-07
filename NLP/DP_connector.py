import sqlite3
import glob
import os


cursors = []

connections = []

#connect to DB
def connectDB(fileName):

    global cursors
    global connections
    cursors = []
    connections = []

    # initializing the connections and the cursors for the database
    for filename in glob.glob(os.path.join("NLP/MetadataDatabases_1.0", fileName)):
        conn = sqlite3.connect(filename)
        connections.append(conn)
        cur = conn.cursor()
        cursors.append(cur)
        conn.text_factory = lambda b: b.decode(errors='ignore')


# function to execute sql command and return the result
def executeString(s):
    result = []
    for cur in cursors:
        cur.execute(s)
        rows = cur.fetchall()
        result.append(rows)
    return result

def disconnect():
    for conn in connections:
        conn.close()

def createCheckerFile(keyName):
    words = ''

    res = executeString('select variableName from ' + keyName)

    for r in res:
        for row in r:
            line = row[0].split(' ')
            for word in line:
                words = words + word + ','

    text_file = open('NLP/' + keyName + '.txt', 'w', encoding='utf8')
    text_file.write(words)
    text_file.close()
