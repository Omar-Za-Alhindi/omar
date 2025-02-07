import re
from NLP.Spell_Checker import opti_leven_distance as oldist
from string import capwords
from NLP.DP_connector import executeString

def removeStopwordsFromLine(text):
    STOPWORDS = ["absolute", "count", "total", "(total)","(fasting)", "(calculated)", 'h', 'l', "optimum:", "premenopausal:"]
    # ------------------modified----------------------
    tokens = text.split()
    out_text =[w for w in tokens if not w in STOPWORDS]# delete stopwords from text
    out_text = ' '.join(out_text)
    text = out_text
    return out_text

def cleanLines(text):
    out_text = ""
    lines = text.splitlines()
    for line in lines:
        out_text += cleanLineAssistant(line)
    return out_text

def cleanLineAssistant(line):
    if not isSidetitleOrComment(line):
        return removeStopwordsFromLine(line) + '\n'
    return ''

def defineOurLists():
    testWords = ["test", "tests", "testname", "parameter", "chemistry"]
    resultWords = ["result", "results"]
    prevResultWords = ["previousresult", " prv.rslt"]
    unitWords = ["unit", "units", "unite"]
    rangWords = ["range", "ranges", "ref.range", "refrange ", "referencevalues", "referencerange",
                 "normalrange", " normalranges", "normalvalue", "normal", "biologicalreferenceintervals",
                 "limit", "expectedvalues"]
    # a7yanan swa a7yanan l7al 1 column or 2 7sab el template.
    lastRes = ["lastdatedresult", "lasttest", "latestresult", "latestresults"]
    date = ["date"]
    wordsList = [testWords, resultWords, prevResultWords, unitWords, rangWords, lastRes, date]

    return wordsList


def extractHeadersRow(text, wordList):
    for subwords in wordList:
        for word in subwords:
            index = text.find(rf'{word}')
            if index != -1:
                indexFirstNewL = text[:index].rfind('\n')
                indexLastNewL = text[index:].find('\n')+index


                # print(text[indexFirstNewL+1:indexLastNewL])
                return text[indexFirstNewL+1:indexLastNewL], indexFirstNewL+1



def getColumnsHeaders(line,wordsList):
    headers = []
    length = 5
    ##### may need to fix it to take the header even if it's not in the headers list
    for header in line :
        head = ''
        mini = len(header)/2
        for subWords in wordsList:
            for word in subWords:
                dist = oldist(header, word)
                if dist < length:
                    if dist < mini:
                        mini = dist
                        # to always replace with the same word
                        head = subWords[0]
                else:
                    continue

        if head is not '':
            headers.append(head)

    return headers


def columnsHeaders(contents,wordsList, splitString):

    contents, indexFirstNewL = extractHeadersRow(contents,wordsList)

    contentslist = contents.split(splitString)

    contentslist = [re.sub(r'\s', '', word) for word in contentslist]
    # get headers
    headers = getColumnsHeaders(contentslist,wordsList)

    return headers, indexFirstNewL


def Headers(text, splitString):
    wordsList = defineOurLists()
    headersList, indexFirstNewL = columnsHeaders(text,wordsList, splitString)



    return headersList, text[indexFirstNewL:]

def isSidetitleOrComment(line):
    return not re.search(r'[0-9]', line)


def splitLists(text, headers):
    linesList = []
    for line in text.splitlines():

        tempLine = {headers[idx]: subWord for idx, subWord in enumerate(line.split(" $ "))}
        linesList.append(tempLine)

    return linesList


def getBioMarker(noSideTitlesList):
    li = []
    bye = False
    for l in noSideTitlesList:
        print(l)
        single = l.split()

        l = capwords(l)

        l = re.sub(r"([a-z])\s([A-Z])", r'\1\2', l)
        #print(l)
        l = re.sub(r'([0-9])\s*-\s*([0-9])', r'\1-\2', l)
        li.append(l)
    return li


def biomarkerDists(biomarkerName):
    mini = 15
    minIDs = []
    minStuff = []
    tempResult = executeString("select id,variablename,symbol from biomarker")
    length = len(biomarkerName)/2
    if length < 0:
        length = 0
    for r in tempResult:
        for r2 in r:
            dist = min(oldist(str(r2[2]).lower(), biomarkerName.lower()), oldist(str(r2[1]).lower(), biomarkerName.lower()))
            if dist < length:
                if dist < mini:
                    mini = dist
                    minIDs.clear()
                    minStuff.clear()
                if dist == mini:
                    minIDs.append(r2[0])
                    minStuff.append(r2)
    return minIDs, mini, minStuff


def createCouples(lines,headersList):
    unitIndex = -1
    tt = []
    #print(lines)
    i=0
    for head in headersList:
        if head != '':
            tt.append(head)
            if 'unit' in head:
                #print(i)
                unitIndex = i
            i+=1

    length = len(lines)
    # print(length)
    couples = []

    for line in range(0, length):
        #print(lines[line])
        temp = []
        i = 0


        words = lines[line].split()
        w = re.sub(r'([a-z])([A-Z])', r'\1 \2', words[0])
        # biomarkersID = executeString('select id from biomarker where lower(symbol)=\'' + (w.split())[0].lower() +'\' or lower(variablename)=\'' + (w.split())[0].lower() + '\'')
        mini = 1000
        biomarkersID = []
        for subWord in w.split():
            tempBiomarkersID, tempMin, stuff = biomarkerDists(subWord.lower())
            if tempMin < mini:
                mini = tempMin
                biomarkersID = tempBiomarkersID

        biomarkersID = set(biomarkersID)


        for word in words:
            if i > 3:
                break
            if i < 3:
                temp.append([word, tt[i]])

            if i == 3:
                word = re.sub(r'-', ' ', word)
                word = word.split()
                # print(word[0])
                #print(word)
                num1 = float(word[0])
                num2 = float(word[1])
                if num1 > num2:
                    temp.append([word[0], 'max'])
                    temp.append([word[1], 'min'])
                else:
                    temp.append([word[1], 'max'])
                    temp.append([word[0], 'min'])

            i += 1
        tempID = []
        for id in biomarkersID:
            result = executeString('select symbol from biomarkerUnit where biomarker=\'' + str(id) + '\'')
            for r in result:
                for r2 in r:

                    if str(r2[0]).lower() == temp[unitIndex][0].lower():
                        #print(str(r2[0]).lower(), temp[unitIndex][0].lower(), id)
                        tempID.append(id)
        if len(tempID) != 0:
            tempID = set(tempID)
            temp.append([tempID, 'ID'])
        else:
            temp.append([biomarkersID, 'No ID unit'])

        if(len(stuff) > 0):
            temp.append([stuff[0], 'correction'])
        couples.append(temp)

    return couples


