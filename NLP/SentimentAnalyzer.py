from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


class SentimentAnalyzer:

    def __init__(self):
        self.intensityAnalyzer = SentimentIntensityAnalyzer()
        self.sentiment_dict = self.loadDictionary()

    def loadDictionary(self):
        word_dict = {}

        with open("NRC-Emotion-Lexicon-Wordlevel-v0.92", "r") as f:
            lines = f.readlines()
            count = 0
            for line in lines:
                line_array = line.split("\t")
                line_array[2] = line_array[2].rstrip()
                if (count % 10 == 0):
                    word_dict[line_array[0]] = [int(line_array[2])]
                else:
                    word_dict[line_array[0]].append(int(line_array[2]))
                count += 1 

        def removekey(d, key):
            r = dict(d)
            del r[key]
            return r

        for key in word_dict.keys():
            if sum(word_dict[key]) == 0:
                 word_dict = removekey(word_dict, key)

        return word_dict

    def getPolarity(self, comment):
        polarity = self.intensityAnalyzer.polarity_scores(comment)
        return polarity


    def getSentimentValues(self, comment):
        sentiment = [0]*10
        for key in self.sentiment_dict.keys():
            for word in comment.split(" "):
                #print("CHECKING WORD", word)
                #print("KEY IS ", key)
                if key == word:
                    for i in range(10):
                        sentiment[i] += self.sentiment_dict[key][i]
        return sentiment

    def displaySentiment(self, sentiment):
        emotions = ["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative", "Positive", "Sadness", "Surprise", "Trust"]
        for i in range(len(sentiment)):
            print(emotions[i] + ": " + str(sentiment[i]))

    #dict looks like {"<coment1>" : [company_id_1_1, company_id_1_i], ... "<commentn>": [company_id_n_1, ..., company_id_n_j]}
    def generateDictofAverageSentiments(self, _dict):
        avg_sentiment_dict = {}
        count_dict = {}
        for key in _dict.keys():
            cur_sentiment = self.getSentimentValues(key)
            for id in _dict[key]:
                if(str(id) in avg_sentiment_dict.keys()):
                    count_dict[str(id)] += 1
                    avg_sentiment_dict[str(id)] = list(np.add(np.asarray(avg_sentiment_dict[str(id)]), np.asarray(cur_sentiment)))
                else:
                    count_dict[str(id)] = 1
                    avg_sentiment_dict[str(id)] = cur_sentiment
        for key in avg_sentiment_dict:
            avg_sentiment_dict[key] = list(np.true_divide(np.asarray(avg_sentiment_dict[key]),np.asarray(count_dict[key])))
        return avg_sentiment_dict

    def driver(self):

        kim_sample_text = "I love seeing Kanye open up to David Letterman during their episode taping for My Next Guest, and now you can see the great conversation on @Netflix. All episodes are streaming today. #MyNextGuest"
        kierkegaard_sample_text = "Relax. The yawning vacuum of disappointment that is New Year�s Eve will make your mediocre Christmas seem outstanding zip"

        kim_polarity = self.getPolarity(kim_sample_text)
        kierkegaard_polarity = self.getPolarity(kierkegaard_sample_text)

        print("KIM POLARITY")
        print(kim_polarity)

        for i in range(5):
            print()

        print("KIERKEGAARD POLARITY")
        print(kierkegaard_polarity)

        for i in range(5):
            print()

        kim_sentiment = self.getSentimentValues(kim_sample_text)
        kierkegaard_sentiment = self.getSentimentValues(kierkegaard_sample_text)

        print("KIM SENTIMENT")
        self.displaySentiment(kim_sentiment)

        for i in range(5):
            print()

        print("KIERKEGAARD SENTIMENT")
        self.displaySentiment(kierkegaard_sentiment)