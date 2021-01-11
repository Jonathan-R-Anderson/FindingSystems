import nltk
from autocorrect import spell
import re
import string

class NaturalLanguageProcessor:
    def __init__(self):
        pass

    def removePunctuation(self, comment):
        p = re.compile("\!|\"|\#|\$|\%|\&|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~")
        return re.sub(p, "", comment)

    def spellCorrection(self, word):
        word = re.sub(r'(.)\1+', r'\1\1', word)
        return spell(word)

    def stemWord(self, word):
        snow = nltk.stem.SnowballStemmer("english")
        return snow.stem(word)

    def driver(self, comment):
        cleanedComment = ""
        comment = self.removePunctuation(comment)
        correctSpelling = ""
        first = True
        for word in comment.split(" "):
            word = self.spellCorrection(word)
            if(first):
                correctSpelling += word
                first = False
            else:
                correctSpelling += " " + word        
        stemmed = ""
        first = True
        
        for word in correctSpelling.split(" "):
            if(first):
                first = False
                stemmed += self.stemWord(word)
            else:
                stemmed += " " + self.stemWord(word)
        return stemmed
        
        #return correctSpelling