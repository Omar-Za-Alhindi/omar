import cv2
import numpy as np
import pytesseract
import os
import re
from OCR import Split



# used in reading images in a folder, to read them in numerical order
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])

    return parts


# read all images in a folder, returns a list containing those images
def load_images_from_folder(folder):
    images = []
    for filename in sorted(os.listdir(folder), key=numericalSort):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)

    return images


# parameters: one image
def smallImagesPreprocessing(img):
    img = cv2.resize(img, None, fx=3, fy=3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


# remove new lines in croped image and replace it with "_", returns the text after modification
def removeNewLines(text):
    text = re.sub("\n+", "_", text)

    return text


# returns if the line have empty cells or not
def empty(line, columnsNumber):
    s = re.findall('empty', line)
    if len(s) >= columnsNumber-1:
        return True


# returns arranged OCR output
# parameters: list of cropped images
def OCRreading(imgs, columnsNumber):
    OCRoutput = ""
    line = ""
    if Split.template == 'S':
        line = 'test $ result $ unit $ range\n'
    for idx, frame in enumerate(imgs, 1):
        # preproccess image
        frame = smallImagesPreprocessing(frame)

        # reading image
        OCR = pytesseract.image_to_string(frame)

        # remove new lines
        OCR = removeNewLines(OCR)

        OCR = unwantedNewLinesCI(OCR)

        print(OCR)



        # put a new line after each row, write empty in empty images, put "$" between images to know where to separate columns
        if idx % columnsNumber == 0:
            if OCR == "":
                line = line + "empty" + "\n"
            else:
                line = line + OCR + "\n"
            if not empty(line, columnsNumber):
                OCRoutput = OCRoutput + line
            line = ""
        else:
            if OCR == "":
                line = line + "empty" + " $ "
            else:
                line = line + OCR + " $ "

    return OCRoutput


# to save OCR output
# parameters: path where to save text file (write file name .txt at the end of the path)
def saveText(text, path):
    File_object = open(path, "w")
    File_object.write(text)


# call every thing needed for reading text from cropped images folder, returns arranged OCR output
# parameters: path of the cropped images folder
def OCRforCroppedImages(path):
    # necessarily for tesseract to work
    pytesseract.pytesseract.tesseract_cmd = "D:\\tesseract\\tesseract.exe"

    # changed based on columns from falioun
    columnsNumber = Split.column_number

    # reading cropped images and get text
    imgs = load_images_from_folder(path)
    OCRoutput = OCRreading(imgs, columnsNumber)

    # save the output in a text file
    # saveText(OCRoutput,"D:\\5th Year\Second Semester\Senior Project\\testImages\Data\\newData\\2\OCRoutput.txt")

    return OCRoutput


def unwantedNewLinesCI(text):
    bb1 = False
    bb2 = False
    text = re.split(r"_", text)
    temp = ""
    #print(text)
    for idx, elem in enumerate(text):
        b1 = re.match(r".*?\(.+?\)", elem)
        if b1:
            bb1 = True
            stop = idx
        b2 = re.match(r".*?\d{2}\/\d{2}\/\d{4}", elem)
        if b2:
            bb2 = True
            stop = idx
    if bb1 or bb2:
        #print("TRUE")
        text = temp.join([str(elem) for elem in text[:stop+1]])
    else:
        text = str(text[0])
    return text


if __name__ == '__main__':
    print(OCRforCroppedImages("D:\\5th Year\Second Semester\Senior Project\\testImages\Data\\newData\\2"))
