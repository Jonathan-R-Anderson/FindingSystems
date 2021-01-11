import datetime, schedule, time, sys, threading, re

class wordThread(threading.Thread):
    def __init__(self, word, dictionary):
        self.word = word
        self.dictionary = dictionary
        self.tagged_ids = []
        super(wordThread, self).__init__()

    def run(self):
        for key in self.dictionary.keys():
            if self.word in self.dictionary[key]:
                self.tagged_ids.append(key)

class Tagger:
    def __init__(self, related_queries, companies):
        self.query_dict = self.populateQueryDict(related_queries, companies)


    def populateQueryDict(self, queries, companies):
        dict = {}
        for company in companies:
            dict[str(company[1])] = [company[0]]
        for query in queries:
            if(str(query[1]) in dict.keys()):
                dict[str(query[1])].append(query[0])
        return dict

    def getTotalLengthDict(self, dict):
        count = 0
        for key in dict.keys():
            count += len(dict[key])
        return count

    def populatedKeys(self, dict):
        count = 0
        for key in dict.keys():
            if (len(dict[key]) > 1):
                count += 1 
        return count


    def tagComment(self, comment):
        threadarray = []
        for word in re.sub('[^A-Za-z0-9]+', ' ', comment).split(" "):
                tmp_wordthread = wordThread(word, self.query_dict)
                threadarray.append(tmp_wordthread)
                tmp_wordthread.start()
        for thread in threadarray:
            thread.join()

        tagged_ids = []
        for thread in threadarray:
            for id in thread.tagged_ids:
                if id not in tagged_ids:
                    tagged_ids.append(id)
        tagged_ids = list(set(tagged_ids))
        return tagged_ids