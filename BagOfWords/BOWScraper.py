import re, random, threading, math, nltk, asyncio
from nltk.corpus import reuters
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import defaultdict
from tqdm import tqdm


class fetchingURL(threading.Thread):
    def __init__(self, bowconnectionhandler, url):
        self.bowconnectionhandler = bowconnectionhandler
        self.url = url
        self.text = ""
        super(fetchingURL, self).__init__()

    def run(self):
        self.text = self.bowconnectionhandler.getTextFromURL(self.url)


class BOWScraper:
    def __init__(self, bowconnectionhandler, eodconnectionhandler, databaseconnectionhandler):
        self.bowconnectionhandler = bowconnectionhandler
        self.eodconnectionhandler = eodconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler
        self.stop_words = stopwords.words('english') + list(punctuation)

    def getCompaniesByExchange(self, exchange):
        companies = []
        for symbol in self.eodconnectionhandler.listCompanyByExchange(exchange):
            exchange_id = self.databaseconnectionhandler.getExchangeID(exchange)
            company_name = self.databaseconnectionhandler.getCompanyNameBySymbolAndExchange(exchange_id, symbol)
            if (company_name is None):
                company_name = self.eodconnectionhandler.getCompanyNameBySymbolAndExchange(exchange, symbol)
                self.databaseconnectionhandler.updateCompanyNameIntoCompany(company_name, exchange_id, symbol)

            companies.append(company_name)                
        return companies

    def tokenize(self, text):
        words = word_tokenize(text)
        words = [w.lower() for w in words]
        return [w for w in words if w not in self.stop_words and not w.isdigit()]

    def getMean(self, values):
        return sum(values)/len(values) 

    def getStandardDeviation(self, values):
        mean = self.getMean(values)
        subtract_mean_square_result = [(x-mean)**2 for x in values]
        mean_of_squared_differences = sum(subtract_mean_square_result)/len(subtract_mean_square_result)
        standard_deviation = mean_of_squared_differences**(1/2)
        return standard_deviation

    def getCompanyNameList(self):
        company_name_list = []
        #exchanges = self.eodconnectionhandler.listExchanges()
        exchanges = ["NYSE"]
        print("BOWScraper progress bar for getCompanyNameList")
        for exchange in tqdm(exchanges):
            companies_names = self.getCompaniesByExchange(exchange)
            for company_name in companies_names:
                company_name = re.sub(r'\W+', ' ', company_name).rstrip()
                company_name_list.append(company_name)
        return company_name_list

    def driver(self): # multithread driver so that all iterations happen at one time
        company_name_list = self.getCompanyNameList()
        random.shuffle(company_name_list)
        start = 0
        stop = start+3
        text_array = [] # [this is one string, then here is another, then another string is here]
        fetchURL_threads = []
        print("BOWScraper progress bar for driver (creating threads)")
        company_name_list = company_name_list[:20] # delete this
        print("company name list", company_name_list)
        for company_name in tqdm(company_name_list):
            urls = self.bowconnectionhandler.getURLSForCompany(10, company_name, start, stop)
            for url in urls:
                fetchURL_thread = fetchingURL(self.bowconnectionhandler, url)
                fetchURL_threads.append(fetchURL_thread)

        new_fetchURL_threads = []
        print("BOWScraper progress bar for driver (starting threads)")
        for thread in tqdm(fetchURL_threads):
            url = thread.url
            text = self.databaseconnectionhandler.getTextFromArticle(url)
            if (text is None):
                new_fetchURL_threads.append(thread)
                thread.start()
            else:
                text_array.append(text)

        print("BOWScraper progress bar for driver (joining threads)")
        for thread in tqdm(new_fetchURL_threads):
            thread.join()
            url = thread.url
            text = thread.text
            text_array.append(text)
            self.databaseconnectionhandler.insertTextIntoArticle(url, text.encode('utf-8', 'ignore'))

        vocabulary = set()
        for string in text_array:
            words = self.tokenize(string)
            vocabulary.update(words)

        vocabulary = list(vocabulary)
        word_index = {w: idx for idx, w in enumerate(vocabulary)}
 
        VOCABULARY_SIZE = len(vocabulary)
        DOCUMENTS_COUNT = len(text_array)
 
        word_idf = defaultdict(lambda: 0)
        for string in text_array:
            words = set(self.tokenize(string))
            for word in words:
                word_idf[word] += 1
 

        for word in vocabulary:
            word_idf[word] = math.log(DOCUMENTS_COUNT / float(1 + word_idf[word]))


        idf_array = []
        for word in vocabulary:
            idf_array.append(word_idf[word])

        idf_standard_deviation = self.getStandardDeviation(idf_array)
        idf_mean = self.getMean(idf_array)
        bag_of_words = [(x,word_idf[x]) for x in word_idf.keys()] # need to verify this is what we want

        print("How many words in the bag of words?", len(bag_of_words))

        for tuple in bag_of_words:
            self.databaseconnectionhandler.insertIntoWordList(tuple[0].encode('utf-8', 'ignore'), tuple[1])

        return bag_of_words