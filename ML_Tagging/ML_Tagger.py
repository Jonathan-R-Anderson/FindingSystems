import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import numpy as np
import time


class ML_Tagger:
    def __init__(self, databaseconnectionhandler, mlscraper):
        self.databaseconnectionhandler = databaseconnectionhandler
        self.mlscraper = mlscraper

    def train(self):
        stemmer = LancasterStemmer()
        training_data = []
        all_results = self.databaseconnectionhandler.getAllResultsFromTags()
        for result in all_results:
            document_id = result[0]
            company_id = result[1]
            comment = self.databaseconnectionhandler.getComment(document_id)
            training_data.append({"class":company_id, "sentence":comment})
        words = []
        classes = []
        documents = []
        ignore_words = ['?'] # idk if we want just this, maybe add more special characters
        # loop through each sentence in our training data
        for pattern in training_data:
            w = nltk.word_tokenize(pattern['sentence'])
            # add to our word list
            words.extend(w)
            # add to documents in our corpus
            documents.append((w, pattern['class']))
            # add to our classes list
            if pattern['class'] not in classes:
                classes.append(pattern['class'])

        words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
        words = list(set(words))

        # remove duplicates

        classes = list(set(classes))

        print (len(documents), "documents")
        print (len(classes), "classes", classes)
        print (len(words), "unique stemmed words", words)

        training = []
        output = []
        # create an empty array for our output
        output_empty = [0] * len(classes)

        # training set, bag of words for each sentence
        for doc in documents:
            # initialize our bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # stem each word
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            # create our bag of words array
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            training.append(bag)
            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            output.append(output_row)
        
        return output

    def driver(self):
        # following instructions from: https://machinelearnings.co/text-classification-using-neural-networks-f5cd7b8765c6
        self.mlscraper.driver()



