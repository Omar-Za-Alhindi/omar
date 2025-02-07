# importing executeString to run sql commands
import re
# import the fuzzywuzzy module
from fuzzywuzzy import fuzz
from NLP.DP_connector import createCheckerFile


# A more optimized version of the Levenshtein distance function using an array of previously calculated distances
def opti_leven_distance(a, b):
    # Create an empty distance matrix with dimensions len(a)+1 x len(b)+1
    dists = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]

    # a's default distances are calculated by removing each character
    for i in range(1, len(a) + 1):
        dists[i][0] = i
    # b's default distances are calulated by adding each character
    for j in range(1, len(b) + 1):
        dists[0][j] = j

    # Find the remaining distances using previous distances
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            # Calculate the substitution cost
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1

            dists[i][j] = min(
                # Removing a character from a
                dists[i - 1][j] + 1,
                # Adding a character to b
                dists[i][j - 1] + 1,
                # Substituting a character from a to b
                dists[i - 1][j - 1] + cost
            )

    return dists[-1][-1]




# correct unit to be like the data ###X109/l(10^9) to 10e9/L
def unitCorrection(text):
    # result = []
    for line in text:
        line['unit'] = re.sub(r'(X10)(()*)(([0-9])+)/l', r'10e\4/L', line['unit'])
        # result.append(line)
        # line['unit'] = 'hello'
    # return result


# correct biomarkers in case of error in reading
def biomarkerFixer(text):
    createCheckerFile('biomarker')
    myChecker = SpellCheck('NLP/biomarker.txt')
    for line in text:
        line['test'] = re.sub(r'([a-z])(\()', r'\1 \2', line['test'])
        tempLine = ''
        for word in line['test'].split(' '):
            myChecker.check(word)
            minDis = 10000
            tempCorrect = ''
            for suggest in myChecker.suggestions():
                if suggest == word:
                    tempCorrect = suggest
                    break
                tempDis = opti_leven_distance(word, suggest)
                if tempDis < minDis and tempDis < len(word) / 3:
                    minDis = tempDis
                    tempCorrect = suggest
                    print(minDis, suggest, word)

            if tempCorrect != '':
                word = tempCorrect
            if tempLine != '':
                tempLine += ' '
            tempLine += word

        line['test'] = tempLine

def rangeNormlizer(text):
    for line in text:
        line['range'] = re.sub(r'([0-9])\s*-\s*([0-9])', r'\1-\2', line['range'])

def dropLastDatedResult(text):
    for line in text:
        line.pop('lastdatedresult')


# spellcheck main class
class SpellCheck:

    # initialization method
    def __init__(self, word_dict_file='words.txt'):
        # open the dictionary file
        self.file = open(word_dict_file, 'r')

        # load the file data in a variable
        data = self.file.read()

        # store all the words in a list
        data = data.split(",")

        # change all the words to lowercase
        data = [i.lower() for i in data]

        # remove all the duplicates in the list
        data = set(data)

        # store all the words into a class variable dictionary
        self.dictionary = list(data)

    # string setter method
    def check(self, string_to_check):
        # store the string to be checked in a class variable
        self.string_to_check = string_to_check

    # this method returns the possible suggestions of the correct words
    def suggestions(self):
        # store the words of the string to be checked in a list by using a split function
        string_words = self.string_to_check.split()

        # a list to store all the possible suggestions
        suggestions = []

        # loop over the number of words in the string to be checked
        for i in range(len(string_words)):

            # loop over words in the dictionary
            for name in self.dictionary:

                # if the fuzzywuzzy returns the matched value greater than 80
                if fuzz.ratio(string_words[i].lower(), name.lower()) >= 75:
                    # append the dict word to the suggestion list
                    suggestions.append(name)

        # return the suggestions list
        return suggestions

    # this method returns the corrected string of the given input
    def correct(self):
        # store the words of the string to be checked in a list by using a split function
        string_words = self.string_to_check.split()

        # loop over the number of words in the string to be checked
        for i in range(len(string_words)):

            # initiaze a maximum probability variable to 0
            max_percent = 0
            tempName = ''

            # loop over the words in the dictionary
            for name in self.dictionary:

                # calulcate the match probability
                percent = fuzz.ratio(string_words[i].lower(), name.lower())

                percent -= abs(len(name) - len(string_words[i]))

                # if the fuzzywuzzy returns the matched value greater than 80
                if percent >= 83:

                    # if the matched probability is
                    if percent > max_percent:
                        # change the original value with the corrected matched value
                        # string_words[i] = name
                        tempName = name

                    # change the max percent to the current matched percent
                    max_percent = percent

            if tempName != '':
                string_words[i] = tempName

        # return the corrected string
        return " ".join(string_words)
