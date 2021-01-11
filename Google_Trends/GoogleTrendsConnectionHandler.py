import urllib3
import requests
from pytrends.request import TrendReq
import json
import pandas
import string
import time


class GoogleTrendsConnectionHandler:

    def __init__(self, logger):
        self.logger = logger
        self.connection = TrendReq()
        self.proxyarr = []
        self.emptyslots = [] #Tracks empty slots in the connection dictionary
        self.connection_count = 0 #Tracks highest key in connection dict
        self.query_dict = {}
        self.results_df = pandas.DataFrame(columns=['Query', 'Country', '90 Days vs. 30 Days', '30 Days vs. 7 Days', '1 Day vs. 7 Days', 'Origin Query', 'Degrees from Origin', 'Related Query Top Index', 'Related Query Rising Index'])

    '''
    def getCountries(self): #Method not complete, array hardcoded for now
        ch = TwitterConnectionHandler(TwitterAccountManagement(WHAT IS THIS))
        country_arr = ch.generateCountryWOEIDarray()
        self.countries = country_arr
        return countries

    def addConnection(self, proxy):
        pass    #Fill this in
    '''

    def makeNewConnection(self):
        self.connection = TrendReq()
        return
  

    def getInterestOverTime(self, connection, timespan, geog, symbol):
        symbol_list = [symbol]
        #print("kw_list="+str(symbol_list))
        #print("timeframe="+timespan)
        #print("geo="+geog)
        connection.build_payload(kw_list=symbol_list, timeframe=timespan, geo=geog)
        IoT = connection.interest_over_time()
        try:
            IoTList = IoT[symbol].tolist()
        except:
            IoTList = None
        #Extract data here
        return IoTList

    def getRelatedQueries(self, connection, timespan, geog, symbol):
        wait_time = 1
        increments = 0
        while(1):
            try:
                connection.build_payload(kw_list=[symbol], timeframe=timespan, geo=geog)
                related_queries_df = connection.related_queries()
                return related_queries_df
            except Exception as e:
                print("Error", e)
                self.logger.commit(1, "GoogleTrendsConnectionHandler", "getRelatedQueries", e)
                if ("429" in str(e)):
                    time.sleep(wait_time)
                    wait_time *= 2
                if(increments >= 5):
                    self.makeNewConnection()
                    wait_time = 1
                    increments = 0
                increments += 1


    def getRelatedTopics(self, connection, timespan, geog, symbol):
        wait_time = 1
        increments = 0
        while(1):
            try:
                related_topics_df = connection.related_topics()
                return related_topics_df
            except Exception as e:
                self.logger.commit(1, "GoogleTrendsConnectionHandler", "getRelatedTopics", e)
                if ("429" in str(e)):
                    time.sleep(wait_time)
                    wait_time *= 2
                if(increments >= 5):
                    self.makeNewConnection()
                    wait_time = 1
                    increments = 0
                increments += 1


    def getRelatedList(self, connection, timespan, geog, symbol):
        related_topics_df = self.getRelatedTopics(connection, timespan, geog, symbol)
        try:
            related_topics_df[symbol]
        except:
            #symbol = symbol.translate(None, string.punctuation)
            for p in ["'", "-", ","]:
                symbol = symbol.replace(p, '')
        try:
            related_list = related_topics_df[symbol]['title'].tolist()
        except:
            related_list = None

        return related_list


    def get90v30(self, connection, country, company):
        list_3m = self.getInterestOverTime(connection, 'today 3-m', country, company)
        if list_3m != None and len(list_3m) >= 30:
            num = float(sum(list_3m[-30:]))/float(len(list_3m[-30:]))
            denom = float(sum(list_3m))/float(len(list_3m))
            ratio_90v30 = num/denom
        else:
            ratio_90v30 = 0
        return ratio_90v30

    def get30v7(self, connection, country, company):
        list_1m = self.getInterestOverTime(connection, 'today 1-m', country, company)
        if list_1m != None and len(list_1m) >= 7:
            num = float(sum(list_1m[-7:]))/float(len(list_1m[-7:]))
            denom = float(sum(list_1m))/float(len(list_1m))
            ratio_30v7 = num/denom
        else:
            ratio_30v7 = 0
        return ratio_30v7

    def get7v1(self, connection, country, company):
        list_7d = self.getInterestOverTime(connection, 'now 7-d', country, company)
        if list_7d != None and len(list_7d) >= 1:
            num = float(list_7d[-1])
            denom = float(sum(list_7d))/float(len(list_7d))
            ratio_7v1 = num/denom
        else:
            ratio_7v1 = 0
        return ratio_7v1

    def getRelatedIndices(self, connection, company): #This only works if the last query by the connection was of the company passed
        related_dict = connection.related_queries()
        try:
            print('1: ' + company)
            related_dict[company]
        except:
            for p in ["'", "-", ","]:
                company = company.replace(p, '')
                print('2: ' + company)

        try:
            related_dict[company]['top'] = sum(related_dict[company]['top']['value'])
            related_dict[company]['rising'] = sum(related_dict[company]['rising']['value'])
        except:
            related_dict = {}
            related_dict = {company:{'top':0}}
            related_dict = {company:{'rising':0}}
            print(related_dict)
        '''
        try:
            related_dict[company]['top'] = sum(related_dict[company]['top']['value'])
        except:
            related_dict = {company:{'top':0}}
            #related_dict[company]['top'] = 0
        try:
            related_dict[company]['rising'] = sum(related_dict[company]['rising']['value'])
        except:
            related_dict = {company:{'rising':0}}
            #related_dict[company]['rising'] = 0
        '''
        return related_dict


    def appendToResultsDF(self,arr):
        self.results_df = self.results_df.append(pandas.DataFrame(arr, columns=['Query', 'Country', '90 Days vs. 30 Days', '30 Days vs. 7 Days', '1 Day vs. 7 Days', 'Origin Query', 'Degrees from Origin', 'Related Query Top Index', 'Related Query Rising Index']), ignore_index = True)
        return



