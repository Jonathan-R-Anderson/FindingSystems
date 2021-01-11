import re, threading, os

class NewsScraper:
    def __init__(self, timestamp, newsconnectionhandler, databaseconnectionhandler):
        self.timestamp = timestamp
        self.newsconnectionhandler = newsconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler

    '''
    def getTextFromURL(self, url):
        text = re.sub('[^A-Za-z0-9]+', ' ', self.newsconnectionhandler.getTextFromURL(url).lower()).split(" ")
        word_dict = {}
        for word in text:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word] += 1
        date = int(self.timestamp.timestamp())
        final_dictionary = {date : word_dict}
        self.databaseconnectionhandler.insertWordIntowordcount("news", final_dictionary)
    '''

    def getTextFromURL(self, url):
        text = self.newsconnectionhandler.getTextFromURL(url).lower()
        date = datetime.datetime.fromtimestamp(self.timestamp.timestamp()).strftime('%Y-%m-%d %H:%M:%S')

        final_dictionary = {date : text} 
        self.databaseconnectionhandler.insertWordIntowordcount("news", final_dictionary)

    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-news.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def driver(self):
        self.getProcessIDS()
        sources = self.newsconnectionhandler.getSources()
        article_urls = self.newsconnectionhandler.getEverything(sources,self.timestamp)
        url_threads = []
        for url in article_urls:
            url_thread = threading.Thread(target=self.getTextFromURL, args=(url,))
            url_threads.append(url_thread)
        for thread in url_threads:
            thread.start()
