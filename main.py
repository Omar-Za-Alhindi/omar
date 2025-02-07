import NLP
import cv2
from OCR.whiteDetection import whiteDetection
from OCR.OCRforCroppedImages import OCRforCroppedImages
from OCR import Split
import glob
import os


result = ''

def main(imageName):




    for filename in glob.glob(os.path.join("OCR/images", '*')):
        os.remove(filename)
    img = cv2.imread(imageName)
    img = whiteDetection(img)
    print(f"image : {img}")
    cv2.imwrite('OCR/hello.jpg', img)
    Split.main('OCR/hello.jpg')
    OCRoutput = OCRforCroppedImages('OCR/images')
    with open('test.txt', 'w', encoding='utf8') as f:
        f.write(OCRoutput)

    # DP_connector.connectDB('*')

    with open('test.txt', 'r', encoding='utf8') as f:
        contents = f.read()

    contents = contents.lower()

    headers, text = NLP.NLP.Headers(contents, " $ ")



    text = NLP.NLP.cleanLines(text)


    print(headers)
    print('\n\n')
    print(text)
    # print(contents)

    linesList = NLP.NLP.splitLists(text, headers)

    NLP.Spell_Checker.dropLastDatedResult(linesList)
    NLP.Spell_Checker.rangeNormlizer(linesList)


    for line in linesList:
        print(line)

    global result
    result = resultString(linesList, headers)


    return linesList, headers

def returnResult():
    return result


def resultString(result, headers):

    finalString = '{\n\n\n'
    for line in result:
        for head in headers:
            if head != 'lastdatedresult':
                finalString += '\t' + head + ' : ' + line[head] + '\n'
        finalString += '\n\n'
    finalString += '}'
    return finalString
