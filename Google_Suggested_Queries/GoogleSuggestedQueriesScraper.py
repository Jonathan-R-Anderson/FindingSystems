import threading, string, re, time, gensim
from nltk.data import find
from tqdm import tqdm
import numpy as np
from scipy.spatial import distance
from kneed import KneeLocator

class Query(threading.Thread):
    def __init__(self, query, company_id, exchange_id, googlesuggestedqueriesconnectionhandler, buckets_scores, databaseconnectionhandler, model):
        self.company_id = company_id
        self.exchange_id = exchange_id
        self.query = query
        self.googlesuggestedqueriesconnectionhandler = googlesuggestedqueriesconnectionhandler
        self.buckets_scores = buckets_scores # array of dicts [{industry-exchange : [(symbol_1, subsector_1, [scores, for,every,index]), (symbol_2, subsector_2,  [scores, for,every,index])]}, {"subsector"-subsector_name : [query_centroid, query_mean, query_stddev]}]
        self.databaseconnectionhandler = databaseconnectionhandler
        self.model = model
        self.results_queue = []
        self.results_array = []
        self.final_results_array = None
        super(Query, self).__init__()

    def getLocationOfQuery(self, query):
        locations = []
        query = re.sub(r"[,.;@#?!&$]+", ' ', query)
        query = re.sub(' +', ' ',query)
        for word in query.split(" "):
            try:
                locations.append(self.model[word])
            except Exception as e:
                pass

        if (len(locations) == 0):
            return None

        else:
            return np.mean(np.asarray(locations),axis=0)

    def run(self):
        current_index = 0
        alphabet_array = list(string.ascii_lowercase)
        alphabet_array.insert(0, " ")
        self.results_queue.append(self.query)
        number_of_results = 0
        max_results = 1000

        exchange_symbol = self.databaseconnectionhandler.getExchangeSymbol(self.exchange_id)
        company_symbol = self.databaseconnectionhandler.getCompanySymbol(self.company_id)
        '''
        while(number_of_results < 5000):
            #print("running query")
            if (current_index == len(self.results_queue)): # ran out of results
                break
            query = re.sub('\W+',' ', self.results_queue[current_index]).replace(" ", "+")
            for entry in alphabet_array:
                tmp_query = "%s+%s" % (query,entry)
                tmp_query = tmp_query.replace("+ ", "") # fixes the first bug of having a white space
                url = self.googlesuggestedqueriesconnectionhandler.generateURL(tmp_query)
                results = self.googlesuggestedqueriesconnectionhandler.getTextFromURL(url)
                print("results", results)
                if (len(results) > 0):
                    self.results_array.append(results)
                    [self.results_queue.append(result) for result in results]
                    number_of_results += len(results)

            current_index += 1
            '''



        company_centroid = None
        company_subsector = None
        company_industry = None
        query_centroid = None
        query_mean = None
        query_stddev = None
        subsector_centroid = None
        subsector_mean = None
        subsector_stddev = None
        industry_centroid = None
        industry_mean = None
        industry_stddev = None
        for _dict in self.buckets_scores:
            for key in _dict.keys():
                if ("subsector" not in key):
                    if (key.split("-")[1] == exchange_symbol):
                        for _tuple in _dict[key]:
                            if(_tuple[0] == company_symbol):
                                company_subsector = _tuple[1]
                                company_centroid  = _tuple[2]
                                company_industry = key.split("-")[0]
                else:
                    if (key.split("-")[1] == company_subsector or key.split("-")[1] == company_industry):
                        values = _dict[key]
                        query_centroid = values[0]
                        query_mean = values[1]
                        query_stddev = values[2]

            keys = list(_dict.keys())
            key = keys[0]
            if (key.split("-")[0] == "subsector"):
                if (key.split("-")[1] == company_subsector):
                    subsector_centroid = _dict[key][0]
                    subsector_mean = _dict[key][1]
                    subsector_stddev = _dict[key][2]

                if(key.split("-")[1] == company_industry):
                    industry_centroid = _dict[key][0]
                    industry_mean = _dict[key][1]
                    industry_stddev = _dict[key][2]


        # subsector centroid is now the mean of industry and subsector centroid
        tmp_centroid_array = []
        if (subsector_centroid is not None):
            tmp_centroid_array.append(subsector_centroid)
        if (industry_centroid is not None):
            tmp_centroid_array.append(industry_centroid)

        tmp_centroid_array = np.asarray(tmp_centroid_array)
        #subsector_centroid = None
        if (len(tmp_centroid_array) != 0):
            subsector_centroid = np.mean(tmp_centroid_array, axis=0)

        def getDistanceFromCentroid(centroid, the_string):
            the_string = the_string.strip()
            word_arr = the_string.split()
            distances_arr = []
            for w in word_arr:
                w_loc = self.getLocationOfQuery(w)
                if(w_loc is not None):
                    distances_arr.append(distance.euclidean(w_loc, centroid))
            distances_arr = np.asarray(distances_arr)
            if(len(distances_arr) != 0):
                avg_distance = np.mean(distances_arr)
            return avg_distance

        results_array_with_distances = []
        if (query_centroid is not None and query_mean is not None and query_stddev is not None):
            for query in self.results_array:
                location_mean = getLocationOfQuery(query)
                distance_from_centroid = distance.euclidean(subsector_centroid_centroid, location_mean)
                results_array_with_distances.append((query, distance_from_centroid))


        if(subsector_centroid is not None):
            while(number_of_results < max_results):
                if (current_index == len(self.results_queue)): # ran out of results
                    break
                query = re.sub('\W+',' ', self.results_queue[current_index]).replace(" ", "+")
                for entry in alphabet_array:
                    results_with_distances = []
                    tmp_query = "%s+%s" % (query,entry)
                    tmp_query = tmp_query.replace("+ ", "") # fixes the first bug of having a white space
                    url = self.googlesuggestedqueriesconnectionhandler.generateURL(tmp_query)
                    results = self.googlesuggestedqueriesconnectionhandler.getTextFromURL(url)
                    dists = []
                    for result in results:
                        tmp_dist = getDistanceFromCentroid(subsector_centroid, result)
                        results_with_distances.append((result, tmp_dist))
                        if(tmp_dist is not None):
                            dists.append(tmp_dist)
                    if(len(dists)>0):
                        seventieth_percentile = np.percentile(np.asarray(dists), [70])[0]
                    tmp_results = []
                    for result in results_with_distances:
                        #if(result[1] is None or result[1] > seventieth_percentile):
                        if(result[1] is None or result[1] <= seventieth_percentile):
                            tmp_results.append(result[0])
                    results = tmp_results
                    #print("results (centroid is not none)", results)
                    if (len(results) > 0):
                        self.results_array.append(results)
                        [self.results_queue.append(result) for result in results]
                        number_of_results += len(results)

                current_index += 1

        else:
            while(number_of_results < max_results):
                if (current_index == len(self.results_queue)): # ran out of results
                    break
                query = re.sub('\W+',' ', self.results_queue[current_index]).replace(" ", "+")
                for entry in alphabet_array:
                    tmp_query = "%s+%s" % (query,entry)
                    tmp_query = tmp_query.replace("+ ", "") # fixes the first bug of having a white space
                    url = self.googlesuggestedqueriesconnectionhandler.generateURL(tmp_query)
                    results = self.googlesuggestedqueriesconnectionhandler.getTextFromURL(url)
                    #print("results (centroid is none)", results)
                    if (len(results) > 0):
                        self.results_array.append(results)
                        [self.results_queue.append(result) for result in results]
                        number_of_results += len(results)

                current_index += 1


        self.final_results_array = self.results_array


class ProxyThread(threading.Thread):
    def __init__(self, googlesuggestedqueriesconnectionhandler, databaseconnectionhandler, queries, buckets_scores, model):
        self.googlesuggestedqueriesconnectionhandler = googlesuggestedqueriesconnectionhandler
        self.databaseconnectionhandler = databaseconnectionhandler
        self.queries = queries
        self.buckets_scores = buckets_scores
        self.model = model
        super(ProxyThread, self).__init__()


    def run(self):
        thread_array = []
        for id_exchange_id_company_name in self.queries:
            company_id = id_exchange_id_company_name[0]
            exchange_id = id_exchange_id_company_name[1]
            company_name = id_exchange_id_company_name[2]
            tmp_thread = Query(company_name, company_id, exchange_id, self.googlesuggestedqueriesconnectionhandler, self.buckets_scores, self.databaseconnectionhandler, self.model)
            thread_array.append(tmp_thread)

        print("Starting threads in GoogleSuggestedQueriesScraper (driver)")
        for thread in tqdm(thread_array):
        #for thread in thread_array:
            thread.start()
            thread.join()
            self.databaseconnectionhandler.insertIntoSuggestedQueries(thread.query, thread.company_id)
            for result in thread.final_results_array:
                self.databaseconnectionhandler.insertIntoSuggestedQueries(result, thread.company_id)


class GoogleSuggestedQueriesScraper:
    def __init__(self, googlesuggestedqueriesconnectionhandlerarray, databaseconnectionhandler, buckets_scores):
        self.googlesuggestedqueriesconnectionhandlerarray = googlesuggestedqueriesconnectionhandlerarray
        self.databaseconnectionhandler = databaseconnectionhandler
        self.buckets_scores = buckets_scores # array of dicts [{industry-exchange : [(symbol_1, subsector_1, [scores, for,every,index]), (symbol_2, subsector_2,  [scores, for,every,index])]}]

    def driver(self):
        queries = self.databaseconnectionhandler.getIDExchangeIDAndCompanyNameFromCompany()
        threads_per_proxy = int(len(queries)/len(self.googlesuggestedqueriesconnectionhandlerarray))
        if (threads_per_proxy == 0):
            threads_per_proxy = 1
        proxythread_array = []
        googlesuggestedqueriesconnectionhandler_index = 0
        word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
        model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)


        for i in range(0, len(queries), threads_per_proxy):
            r = range(min(threads_per_proxy, len(queries) - i))
            tmp_queries = []
            for j in r:
                tmp_queries.append(queries[i+j])

            tmp_pt = ProxyThread(self.googlesuggestedqueriesconnectionhandlerarray[googlesuggestedqueriesconnectionhandler_index], self.databaseconnectionhandler, tmp_queries, self.buckets_scores, model)
            proxythread_array.append(tmp_pt)
            if (googlesuggestedqueriesconnectionhandler_index == len(self.googlesuggestedqueriesconnectionhandlerarray)-1):
                googlesuggestedqueriesconnectionhandler_index = 0
            else:
                googlesuggestedqueriesconnectionhandler_index += 1

        for pt in proxythread_array:
            pt.start()
        for pt in proxythread_array:
            pt.join()
