import threading, re
from tqdm import tqdm

class fetchingURL(threading.Thread):
    def __init__(self, bowconnectionhandler, url, company_id, exchange_id):
        self.bowconnectionhandler = bowconnectionhandler
        self.company_id = company_id
        self.exchange_id = exchange_id
        self.url = url
        self.text = ""
        super(fetchingURL, self).__init__()

    def run(self):
        self.text = self.bowconnectionhandler.getTextFromURL(self.url)

class ML_Scraper:
    def __init__(self, bowconnectionhandler, bowscraper, databaseconnectionhandler, eodconnectionhandler):
        self.bowconnectionhandler = bowconnectionhandler
        self.bowscraper = bowscraper
        self.databaseconnectionhandler = databaseconnectionhandler
        self.eodconnectionhandler = eodconnectionhandler

    def getCompaniesByExchange(self, exchange):
        companies = []
        for symbol in self.eodconnectionhandler.listCompanyByExchange(exchange):
            exchange_id = self.databaseconnectionhandler.getExchangeID(exchange)
            company_name = self.databaseconnectionhandler.getCompanyNameBySymbolAndExchange(exchange_id, symbol)
            if (company_name is None):
                company_name = self.eodconnectionhandler.getCompanyNameBySymbolAndExchange(exchange, symbol)
                self.databaseconnectionhandler.updateCompanyNameIntoCompany(company_name, exchange_id, symbol)

            companies.append((company_name, symbol))                
        return companies

    def getCompanyNameListSymbolsAndExchange(self): # should multithread this method to speed it up
        company_names_symbols_list_and_exchange = []
        #exchanges = self.eodconnectionhandler.listExchanges()
        exchanges = ["NYSE"]
        print("ML_Scraper progress bar for getCompanyNameListSymbolsAndExchange")
        for exchange in tqdm(exchanges):
            companies_and_symbols = self.getCompaniesByExchange(exchange) # (company_name, symbol)
            for company_and_symbol in companies_and_symbols:
                company_symbol = company_and_symbol[1]
                company_name = company_and_symbol[0]
                company_name = re.sub(r'\W+', ' ', company_name).rstrip()
                company_names_symbols_list_and_exchange.append((company_name, company_symbol, exchange))
        return company_names_symbols_list_and_exchange

    def getMean(self, values):
        return sum(values)/len(values) 

    def getStandardDeviation(self, values):
        mean = self.getMean(values)
        subtract_mean_square_result = [(x-mean)**2 for x in values]
        mean_of_squared_differences = sum(subtract_mean_square_result)/len(subtract_mean_square_result)
        standard_deviation = mean_of_squared_differences**(1/2)
        return standard_deviation


    '''
        Tries to get as close to 50th percentile as possible
    '''
    def pruneBagOfWords(self, bag_of_words):
        original_len = len(bag_of_words)
        last_value = 0
        while (len(bag_of_words)/original_len > .5): # 50th percentile
            if (last_value == len(bag_of_words)/original_len):
                break
            else:
                last_value = len(bag_of_words)/original_len
            idf_array = [x[1] for x in bag_of_words]
            idf_standard_deviation = self.getStandardDeviation(idf_array)
            idf_mean = self.getMean(idf_array)
            bag_of_words = [(x[0],x[1]) for x in bag_of_words if x[1] >= idf_mean-idf_standard_deviation*2]
        return bag_of_words

    def driver(self):
        #max_results = 1000
        max_results = 10 # delete this
        #company_names_symbols_list_and_exchange = self.getCompanyNameListSymbolsAndExchange() #(company_name, company_symbol, exchange))
        company_names_symbols_list_and_exchange = self.getCompanyNameListSymbolsAndExchange()[:20] # delete this
        bag_of_words = self.databaseconnectionhandler.getAllWordList()
        if (bag_of_words is None):
            bag_of_words = self.bowscraper.driver()
        bag_of_words = self.pruneBagOfWords(bag_of_words)
        print("How many words in the bag of words after pruning?", len(bag_of_words))
        start = 0
        stop = start+max_results

        text_company_id_exchange_id_array = [] # array of tuples (text, company_id, exchange_id)
        fetchURL_threads = []
        print("ML_Scraper progress bar for driver (company name symbol exchange)")
        for company_name_symbol_exchange in tqdm(company_names_symbols_list_and_exchange):
            company_name = company_name_symbol_exchange[0]
            company_symbol = company_name_symbol_exchange[1]
            exchange = company_name_symbol_exchange[2]
            exchange_id = self.databaseconnectionhandler.getExchangeID(exchange)
            company_id = self.databaseconnectionhandler.getCompanyID(exchange_id, company_symbol)
            bag_of_words_count = int(self.databaseconnectionhandler.getBagCount(company_id, exchange_id))
            print("here")
            if (bag_of_words_count < max_results):
                urls = self.bowconnectionhandler.getURLSForCompany(max_results+10, company_name, start, stop)
                print("there")
                for url in urls:
                    print("everywhere", len(urls))
                    fetchURL_thread = fetchingURL(self.bowconnectionhandler, url, company_id, exchange_id)
                    fetchURL_threads.append(fetchURL_thread)

        new_fetchURL_threads = []
        print("ML_Scraper progress bar for driver (starting threads)")
        for thread in tqdm(fetchURL_threads):
            url = thread.url
            text = self.databaseconnectionhandler.getTextFromArticle(url)
            if (text is None):
                new_fetchURL_threads.append(thread)
                thread.start()
            else:
                text_company_id_exchange_id_array.append((text, thread.company_id, thread.exchange_id))

        print("ML_Scraper progress bar for driver (joining threads)")
        for thread in tqdm(new_fetchURL_threads):
            thread.join()
            text = thread.text.encode("utf-8")
            url = thread.url
            text_company_id_exchange_id_array.append((text, thread.company_id, thread.exchange_id))
            self.databaseconnectionhandler.insertTextIntoArticle(url, text)

        print("ML_Scraper progress bar for driver (inserting BagOfWords)")
        for tuple in tqdm(text_company_id_exchange_id_array):
            text = tuple[0]
            company_id = tuple[1]
            exchange_id = tuple[2]
            tmp_words = text.split(" ")
            tmp_dict = {}
            bag_id = self.databaseconnectionhandler.getBagId(company_id, exchange_id)
            if (bag_id is None):
                bag_id = self.databaseconnectionhandler.insertIntoBag(company_id, exchange_id)
            for word in tmp_words:
                if word in bag_of_words:
                    if word not in tmp_dict.keys():
                        tmp_dict[word] = 1
                    else:
                        tmp_dict[word] += 1
            for word in tmp_dict.keys():
                if (self.databaseconnectionhandler.isInBagOfWord(bag_id, word)):
                    self.databaseconnectionhandler.updateBagOfWords(bag_id, word, tmp_dict[word])
                else:
                    self.databaseconnectionhandler.insertIntoBagOfWords(bag_id, word, tmp_dict[word])