import gensim, operator, threading, string, re, random
from nltk.data import find
from scipy.spatial import distance
import numpy
from tqdm import tqdm



class BucketQuery(threading.Thread):
    def __init__(self, query, googlesuggestedqueriesconnectionhandler, model):
        self.query = query
        self.googlesuggestedqueriesconnectionhandler = googlesuggestedqueriesconnectionhandler
        self.model = model
        self.results_queue = []
        self.results_array = []
        self.query_centroid = None
        self.query_mean = None
        self.query_stddev = None
        super(BucketQuery, self).__init__()

    def run(self):

        current_index = 0
        alphabet_array = list(string.ascii_lowercase)
        alphabet_array.insert(0, " ")
        self.results_queue.append(self.query)
        number_of_results = 0

        if ("/" in self.query):
            query_array = self.query.lower().split("/")
        else:
            query_array = self.query.lower().split(" ")
        for q in range(len(query_array)):
            query_array[q] = re.sub(r"[,.;@#?!&$]+", ' ', query_array[q])
            query_array[q] = re.sub(' +', ' ',query_array[q])

        tmp_query_array = []
        for i in range(len(query_array)):
            [tmp_query_array.append(q) for q in query_array[i]]
        query_array = tmp_query_array
        for i in range(len(query_array)):
            query_array[i] = query_array[i].strip()
        #print("QUERY ARRAY IS ", query_array)

        tmp_vectors = []


        for word in query_array:
            #print("about to try ",word)
            try:
                #print(self.model[word])
                tmp_vectors.append(self.model[word])
            except Exception as e:
                #print("Exception", e)
                pass
        if (len(tmp_vectors) > 0):
            query_centroid = numpy.mean(tmp_vectors, axis=0)
        else:
            query_centroid = None

        '''
        #print("QUERY CENTROID UP HERE", query_centroid)
        distances_arr = []
        if (query_centroid is not None):
            while(number_of_results < 1000):
                #print("running query")
                if (current_index == len(self.results_queue)): # ran out of results
                    #print("breaking")
                    break
                query = re.sub('\W+',' ', self.results_queue[current_index]).replace(" ", "+").lower()
                #print("the query right now is", query, "running based off of", self.query)
                tmp_subsector_sum_score = [0] * 300
                tmp_subsector_values_count = 0


                temp_vectors = []

                for word in query.split("+"):
                    try:
                        temp_vectors.append(self.model[word])
                    except Exception as e:
                        pass
                if (len(temp_vectors) > 0):
                    tmp_result_mean = numpy.mean(temp_vectors, axis=0)
                else:
                    tmp_result_mean = None

                if (tmp_result_mean is not None):
                    distances_arr.append(distance.euclidean(query_centroid, tmp_result_mean))

                for entry in alphabet_array:
                    tmp_query = "%s+%s" % (query,entry)
                    tmp_query = tmp_query.replace("+ ", "") # fixes the first bug of having a white space
                    url = self.googlesuggestedqueriesconnectionhandler.generateURL(tmp_query)
                    results = self.googlesuggestedqueriesconnectionhandler.getTextFromURL(url)
                    if (len(results) > 0):
                        self.results_array.append(results)
                        [self.results_queue.append(result) for result in results]
                        number_of_results += len(results)
                current_index += 1
    
            if(len(distances_arr) > 0):
                self.query_centroid = query_centroid
                self.query_mean = numpy.mean(distances_arr)
                self.query_stddev = numpy.std(distances_arr)

            else:
               self.query_centroid = query_centroid
               self.query_mean = None
               self.query_stddev = None
                
        else:
            self.query_centroid = None
            self.query_mean = None
            self.query_stddev = None
        '''
        self.query_centroid = query_centroid
        self.query_mean = None
        self.query_stddev = None

        



class BucketPreprocessing:
    def __init__(self, buckets, googlesuggestedqueriesconnectionhandlerarray):
        self.buckets = buckets
        self.googlesuggestedqueriesconnectionhandlerarray = googlesuggestedqueriesconnectionhandlerarray

    def driver(self):
        array_of_dicts = []
        
        centroid_mean_stddev_dict = {}



        subsector_bq_array = []
        sector_bq_array = []

        word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
        model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)
        for bucket in self.buckets:
            for key in bucket.keys():
                key_array = key.split("-")
                industry = key_array[0].replace("+", " ") # removing + from spaces
                exchange = key_array[1]
                tuple_array = bucket[key]
                tmp_dict = {}
                for _tuple in tuple_array:
                    symbol = _tuple[0]
                    subsector = _tuple[1]
                    if ("/" in subsector):
                        subsector_array = subsector.split("/")
                    else:
                        subsector_array = subsector.split(" ")
                    subsector_sum_score = [0] * 300
                    subsector_values_count = 0
                    
                    for word in subsector_array:
                        try:
                            subsector_sum_score = list(map(operator.add, model[word], subsector_sum_score))
                            subsector_values_count += 1
                        except Exception as e:
                            pass

                    if (subsector_values_count > 0): # if any of the words were in the model
                        divided_value_array = numpy.array(subsector_sum_score)/subsector_values_count
                        ie_key = industry+"-"+exchange
                        if (ie_key not in tmp_dict.keys()):
                            tmp_dict[ie_key] = []
                            tmp_dict[ie_key].append((symbol, subsector, divided_value_array))
                        else:
                            tmp_dict[ie_key].append((symbol, subsector, divided_value_array))
                    else: # subsector words were not in the model, try to use the industry in here
                        for word in industry.split(" "):
                            try:
                                subsector_sum_score = list(map(operator.add, model[word], subsector_sum_score))
                                subsector_values_count += 1
                            except Exception as e:
                                pass
                        if (subsector_values_count > 0): # if any of the words were in the model
                            divided_value_array = numpy.array(subsector_sum_score)/subsector_values_count
                            ie_key = industry+"-"+exchange
                            if (ie_key not in tmp_dict.keys()):
                                tmp_dict[ie_key] = []
                                tmp_dict[ie_key].append((symbol, subsector, divided_value_array))
                            else:
                                tmp_dict[ie_key].append((symbol, subsector, divided_value_array))    
                        else: # industry not found either, restore original tuple
                            ie_key = industry+"-"+exchange
                            if (ie_key not in tmp_dict.keys()):
                                tmp_dict[ie_key] = []
                                tmp_dict[ie_key].append((symbol, subsector))
                            else:
                                tmp_dict[ie_key].append((symbol, subsector))
                    

                       
                    if ("subsector-"+subsector not in centroid_mean_stddev_dict.keys()):
                        bq = BucketQuery(subsector, self.googlesuggestedqueriesconnectionhandlerarray[random.randint(0,14)], model)
                        subsector_bq_array.append(bq)
                        centroid_mean_stddev_dict["subsector-"+subsector] = None

                if ("subsector-"+industry not in centroid_mean_stddev_dict.keys()):
                    bq = BucketQuery(industry, self.googlesuggestedqueriesconnectionhandlerarray[random.randint(0,14)], model)
                    sector_bq_array.append(bq)
                    centroid_mean_stddev_dict["subsector-"+industry] = None

                array_of_dicts.append(tmp_dict)

        
        #for subsector_thread in subsector_bq_array:
        #    subsector_thread.start()
        #    subsector_thread.join()
        #    centroid_mean_stddev_dict["subsector-"+subsector_thread.query] = [subsector_thread.query_centroid, subsector_thread.query_mean, subsector_thread.query_stddev]


        #for sector_thread in sector_bq_array:
        #    sector_thread.start()
        #    sector_thread.join()
        #    centroid_mean_stddev_dict["subsector-"+subsector_thread.query] = [subsector_thread.query_centroid, subsector_thread.query_mean, subsector_thread.query_stddev]


        threads_per_proxy = 20
        print("subsector loop")
        for i in tqdm(range(0, len(subsector_bq_array), threads_per_proxy)):
            r = range(min(threads_per_proxy, len(subsector_bq_array) - i))
            tmp_queries = []
            for j in r:
                subsector_bq_array[i+j].start()
            for j in r:
                subsector_bq_array[i+j].join()
                centroid_mean_stddev_dict["subsector-"+subsector_bq_array[i+j].query] = [subsector_bq_array[i+j].query_centroid, subsector_bq_array[i+j].query_mean, subsector_bq_array[i+j].query_stddev]

        print("industry loop")
        for i in tqdm(range(0, len(sector_bq_array), threads_per_proxy)):
            r = range(min(threads_per_proxy, len(sector_bq_array) - i))
            tmp_queries = []
            for j in r:
                sector_bq_array[i+j].start()
            for j in r:
                sector_bq_array[i+j].join()
                centroid_mean_stddev_dict["subsector-"+sector_bq_array[i+j].query] = [sector_bq_array[i+j].query_centroid, sector_bq_array[i+j].query_mean, sector_bq_array[i+j].query_stddev]



        array_of_dicts.append(centroid_mean_stddev_dict)


        return array_of_dicts