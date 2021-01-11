from GoogleTrendsConnectionHandler import GoogleTrendsConnectionHandler

from pytrends.request import TrendReq
import threading
import string
#import proxies #Right here BURT
import numpy as np
import pandas as pd
import time
import sys
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.join(dir_path)

path, file = os.path.split(pwd)

sys.path.append(os.path.join(path,"EODData"))


import EODDataConnectionHandler as EODDataConnectionHandler






class GoogleTrendsScraper:
    def __init__ (self, databaseconnectionhandler, logger):
        self.wait_time = 1
        self.eo = EODDataConnectionHandler.EODDataConnectionHandler()
        self.databaseconnectionhandler = databaseconnectionhandler
        self.logger = logger
        self.google_trends_connection_handler = GoogleTrendsConnectionHandler(self.logger)

    def getExchanges(self):
        return self.eo.listExchanges()

    def getCompaniesByExchange(self, exchange):
        companies_and_symbols = []
        for symbol in self.eo.listCompanyByExchange(exchange):
            print("processing", symbol)
            companies_and_symbols.append((self.eo.getCompanyNameBySymbolAndExchange(exchange, symbol), symbol))
        return companies_and_symbols

    def scrapeSymbol(self, company_name):
        while(1):
            print("first")
            connection = self.google_trends_connection_handler.connection #Each scraper object can hold a number of connections, for now we just use the first one
            print("second")
            related_queries_df = self.google_trends_connection_handler.getRelatedQueries(connection, 'now 7-d', 'US', company_name)
            print("third")
            related_topics_df = self.google_trends_connection_handler.getRelatedTopics(connection, 'now 7-d', 'US', company_name)
            print("fourth")
            try:
                top_queries = []
                rising_queries = []
                top_topics = []
                rising_topics = []
                #print("Top-Q")
                if (related_queries_df[company_name]['top'] is not None):
                    if (related_queries_df[company_name]['top']['query'] is not None):
                        top_queries = related_queries_df[company_name]['top']['query'].tolist()
                #print("Ris-Q")
                if (related_queries_df[company_name]['rising'] is not None):
                    if (related_queries_df[company_name]['rising']['query'] is not None):
                        rising_queries = related_queries_df[company_name]['rising']['query'].tolist()
                #print("Top-T")
                if (related_topics_df[company_name] is not None):
                    if(related_topics_df[company_name]['top'] is not None and not related_topics_df[company_name]['top'].empty):
                        if(related_topics_df[company_name]['top']['topic_title'] is not None):
                                top_topics = related_topics_df[company_name]['top']['topic_title'].tolist()
                #print("Ris-T")
                if (related_topics_df[company_name] is not None):
                    if(related_topics_df[company_name]['rising'] is not None and not related_topics_df[company_name]['rising'].empty):
                        if(related_topics_df[company_name]['rising']['topic_title'] is not None):
                            rising_topics = related_topics_df[company_name]['rising']['topic_title'].tolist()

                self.wait_time = 2
                return(top_queries, rising_queries, top_topics, rising_topics)
            except Exception as e:
                print("Error in scrapeSymbol", e)
                if ("429" or "402" or "500" in str(e)):
                    time.sleep(self.wait_time)
                    self.logger.commit(1, "GoogleTrendsScraper", "scrapeSymbol", str(e))
                    self.wait_time *= 2
                    if(self.wait_time >= 1):
                        self.google_trends_connection_handler.makeNewConnection()
                continue

    def commitToDb(self, top_queries, rising_queries, top_topics, rising_topics, exchange_id, company_id, iteration):
        for word in top_queries:
            word = word.lower()
            self.databaseconnectionhandler.updateRelatedQueries(exchange_id, company_id, word, iteration)
        for word in rising_queries:
            word = word.lower()
            self.databaseconnectionhandler.updateRelatedQueries(exchange_id, company_id, word, iteration)
        for word in top_topics:
            word = word.lower()
            self.databaseconnectionhandler.updateRelatedQueries(exchange_id, company_id, word, iteration)
        for word in rising_topics:
            word = word.lower()
            self.databaseconnectionhandler.updateRelatedQueries(exchange_id, company_id, word, iteration)

    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-google.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def populateRelatedQueries(self):
        self.getProcessIDS()
        iteration = 0
        while(1):
            exchanges = self.getExchanges()
            for exchange in exchanges:
                companies_and_symbols = self.getCompaniesByExchange(exchange) # (company_name, symbol)
                for company_and_symbol in companies_and_symbols:
                    print("company_and_symbol", company_and_symbol)
                    company_name = company_and_symbol[0]
                    company_name = re.sub(r'\W+', ' ', company_name).rstrip()
                    symbol = company_and_symbol[1]
                    exchange_id = self.databaseconnectionhandler.getExchangeID(exchange)
                    company_id = self.databaseconnectionhandler.getCompanyID(exchange_id, symbol)
                    top_queries, rising_queries, top_topics, rising_topics = self.scrapeSymbol(company_name)
                    self.commitToDb(top_queries, rising_queries, top_topics, rising_topics, exchange_id, company_id, iteration)
            iteration += 1

    def driver(self):
        threading.Thread(target=self.populateRelatedQueries).start()


