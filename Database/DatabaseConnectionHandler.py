import MySQLdb, time, random, datetime, sys, os
import numpy as np

sys.path.append("..")
from NLP.NaturalLanguageProcessor import NaturalLanguageProcessor
from NLP.SentimentAnalyzer import SentimentAnalyzer
dir_path = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.join(dir_path)

path, file = os.path.split(pwd)

sys.path.append(os.path.join(path,"Tagging"))

from Tagger import Tagger


class DatabaseConnectionHandler:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.tagger = Tagger(self.getAllRelatedQueries(), self.getAllCompanies())
        self.sentiment_analyzer = SentimentAnalyzer()


    def connect(self):
        while(1):
            try:
                db_connection = MySQLdb.Connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
                cursor = db_connection.cursor()
                cursor.execute("SELECT VERSION()")
                results = cursor.fetchone()
                ver = results[0]
                if (ver is None):
                    cursor.close()
                    db_connection.close()
                else:
                    return cursor, db_connection
            except Exception as e:
                if ("Too many connections" in str(e)):
                    time.sleep(random.randint(3, 10))

    def getCompanySymbol(self, company_id):
        sql_command = "select symbol from company where id=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (company_id,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getExchangeSymbol(self, exchange_id):
        sql_command = "select symbol from exchange where id=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (exchange_id,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def insertIntoSuggestedQueries(self, document, company_id):
        sql_command = "insert into suggested_queries (document, company_id) values (\"%s\", %s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (document, company_id,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def getAllWordList(self):
        sql_command = "select * from wordlist"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
            result_set[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def insertIntoWordList(self, word, idf_score):
        sql_command = "insert into wordlist (word, idf_score) values (%s, %s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (word, idf_score,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def getTextFromArticle(self, url):
        sql_command = "select text from article where url=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (url,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def insertTextIntoArticle(self, url, text):
        sql_command = "insert into article (url, text) values (%s, %s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (url, text,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def getIDExchangeIDAndCompanyNameFromCompany(self):
        sql_command = "select id, exchange_id, company_name from company"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def updateCompanyNameIntoCompany(self, company_name, exchange, symbol):
        sql_command = "update company set company_name=%s where exchange_id=%s and symbol=%s" 
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (company_name,exchange,symbol,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def getCompanyNameBySymbolAndExchange(self, exchange, symbol):
        sql_command = "select company_name from company where exchange_id=%s and symbol=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (exchange, symbol,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def updateBagOfWords(self, bag_id, word, new_count):
        old_count = 0
        sql_command = "select count from bag_of_words where bag_id='"+str(bag_id)+"' and word='"+word+"'" 
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            old_count = int(cursor.fetchone()[0])
        except Exception as e:
            old_count = 0 # this should be dead code
        cursor.close()
        db_connection.close()
        # get old count and add it to new count

        
        sql_command = "update bag_of_words set count='"+str(old_count+new_count)+"' where bag_id='"+str(bag_id)+"' and word='"+word+"'" 
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        print("updated!")

    def isInBagOfWords(self, bag_id, word):
        sql_command = "select * from bag_of_words where bag_id=%s and word=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (bag_id,word,))
            cursor.fetchone()[0]
            result_set = True
        except Exception as e:
            result_set = False
        cursor.close()
        db_connection.close()
        return result_set

    def insertIntoBagOfWords(self, bag_id, word, count):
        sql_command = "insert into bag_of_words (bag_id, word, count) values (%s, %s, %s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (bag_id, word, count,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def getBagId(self, company_id, exchange_id):
        sql_command = "select id from bag where company_id = %s and exchange_id = %s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (company_id, exchange_id,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def insertIntoBag(self, company_id, exchange_id):
        sql_command = "insert into bag (company_id, exchange_id) values (%s, %s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (company_id, exchange_id,))
        db_connection.commit()
        cursor.close()
        db_connection.close()

        return self.getBagId(company_id, exchange_id)

    def getBagCount(self, company_id, exchange_id):
        sql_command = "select count(*) from bag where company_id=%s and exchange_id=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (company_id, exchange_id,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def insertIntoError(self, level, _class, method, error, date):
        sql_command = "insert into error (level, class, method, error, date) values (%s, %s, %s, %s, %s)"
        #print("sql command", sql_command)
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command, (level, _class, method, error, date))
        db_connection.commit()
        cursor.close()
        db_connection.close()

    def insertIntoCompanyValue(self, company_id, date, open, high, low, close, volume):
        sql_command = "insert into company_value (date, open, high, low, close, volume, company_id) values ('"+date+"', '"+str(open)+"', '"+str(high)+"', '"+str(low)+"', '"+str(close)+"', '"+str(volume)+"', '"+str(company_id)+"')"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command)
        db_connection.commit()
        cursor.close()


    def populateCompany(self, exchange_id, company):
        #exchange_id = self.getExchangeID(exchange)

        def getCompanyID(exchange_id, company):
            sql_command = "select id from company where symbol='"+company+"'"+" and exchange_id='"+str(exchange_id)+"'"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command)
                result_set = cursor.fetchone()[0]
            except Exception as e:
                result_set = None
            cursor.close()
            db_connection.close()
            return result_set

        company_id = getCompanyID(exchange_id, company)
        if (company_id is None):
            #print("creating new entry")
            sql_command = "insert into company (exchange_id, symbol) values (%s, %s)"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            cursor.execute(sql_command, (str(exchange_id), company))
            db_connection.commit()
            cursor.close()
            db_connection.close()


    def getExchangeID(self, exchange):
        result_set = None
        while (result_set is None):
            try:
                sql_command = "select id from exchange where symbol='"+str(exchange)+"'"
                connection_info = self.connect()
                cursor = connection_info[0]
                db_connection = connection_info[1]
                cursor.execute(sql_command)
                result_set = cursor.fetchone()[0]
            except Exception as e:
                self.populateExchangeIDs(exchange)
                print("Error in getExchangeID", e, sql_command)
                result_set = None
        cursor.close()
        db_connection.close()
        return result_set


    def populateExchangeIDs(self, exchange):

        def getExchangeID(exchange):
            sql_command = "select id from exchange where symbol='"+str(exchange)+"'"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command)
                result_set = cursor.fetchone()[0]
            except Exception as e:
                result_set = None
            cursor.close()
            db_connection.close()
            return result_set

        exchange_id = getExchangeID(exchange)
        if (exchange_id is None):
            sql_command = "insert into exchange (symbol) values (%s)"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            cursor.execute(sql_command, (exchange,))
            db_connection.commit()
            cursor.close()
            db_connection.close()

    def getCompanyID(self, exchange_id, company):
        result_set = None
        while(result_set is None):
            try:
                sql_command = "select id from company where symbol='"+company+"'"+" and exchange_id='"+str(exchange_id)+"'"
                connection_info = self.connect()
                cursor = connection_info[0]
                db_connection = connection_info[1]
                cursor.execute(sql_command)
                result_set = cursor.fetchone()[0]
            except Exception as e:
                self.populateCompany(exchange_id, company)
                result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def updateRelatedQueries(self, exchange_id, company_id, query, iteration):        
        #nlp = NaturalLanguageProcessor()
        #query = nlp.driver(query)

        def checkQueryInRelatedQueries(exchange_id, company_id, query):
            sql_command = "select iterations_id from related_queries where exchange_id=%s and company_id=%s and query=%s"
            #print("CQ QUERY: " + sql_command)
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command, (str(exchange_id), str(company_id), str(query)))
                result_set = cursor.fetchone()[0]
            except Exception as e:
                result_set = None
            cursor.close()
            db_connection.close()
            return result_set
        
        def checkIterationInIterations(iteration_id, iteration):
            sql_command = "select iterations_id from iterations where iterations_id=%s and iterations=%s"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command, (str(iteration_id), str(iteration)))
                result_set = cursor.fetchone()[0]
            except Exception as e:
                result_set = None
            cursor.close()
            db_connection.close()
            return result_set

        def addIteration(iteration_id, iteration):
            sql_command = "insert into iterations (iterations, iterations_id) values (%s, %s)"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command, (str(iteration), str(iteration_id)))
            except Exception as e:
                pass
            db_connection.commit()
            cursor.close()
            db_connection.close()

        def addRelatedQuery(exchange_id, company_id, query):
            sql_command = "insert into related_queries (exchange_id, company_id, query) values (%s, %s, %s)"
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            try:
                cursor.execute(sql_command, (str(exchange_id), str(company_id), str(query)))
            except Exception as e:
                pass
            db_connection.commit()
            cursor.close()
            db_connection.close()

        iteration_id = checkQueryInRelatedQueries(exchange_id, company_id, query)
        #print("IF QUERY: " + str(query) + " ALREADY IN RELATED QUERIES THEN ITERATION_ID: " + str(iteration_id))

        # if there is an entry already in related_queries table
        if(iteration_id is not None):
            #If there is not already an entry for that query under this iteration
            if(checkIterationInIterations(iteration_id, iteration) is None):
                #print("QUERY: " + str(query) + " WAS IN RELATED QUERIES ... ADDING ITERATION: " + str(iteration) + " WITH ITERATION_ID: " + str(iteration_id))
                addIteration(iteration_id, iteration)
        # if there is not an entry already in related_queries table
        else:
            addRelatedQuery(exchange_id, company_id, query)
            iteration_id = checkQueryInRelatedQueries(exchange_id, company_id, query)
            #print("QUERY: " + str(query) + " WAS NOT IN RELATED QUERIES ... ADDING WITH ITERATION_ID " + str(iteration_id) + " UNDER ITERATION: " + str(iteration))
            addIteration(iteration_id, iteration)

    def companyIDAndTimeInSentiments(self, company_id, start_time, end_time):
        sql_command = "select company_id from sentiments where company_id=%s and start_time=%s and end_time=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (company_id,start_time,end_time,))
            result_set = cursor.fetchone()[0]
            result_set = True
        except Exception as e:
            result_set = False
        cursor.close()
        db_connection.close()
        return result_set

    def insertWordIntowordcount(self, source, final_dict):
        for timestamp in final_dict.keys():
            nlp = NaturalLanguageProcessor()
            #comment = nlp.driver(final_dict[timestamp]).encode("utf-8")
            comment = final_dict[timestamp].encode("utf-8")
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            sql_command = "INSERT INTO documents (source,comment,date) VALUES (%s,%s,%s)"
            #print("sql command", sql_command)
            if (len(comment) >= 65000):
                comment = comment[:65000]
            cursor.execute(sql_command, (source, comment, timestamp))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            
            comment_id = self.getIdFromComment(comment)
            comment = comment.decode("utf-8")
            tags = self.tagger.tagComment(comment)
            tagged_successfully = self.insertDocumentIDandTagIDSIntoTags(comment_id, tags)
            if (tagged_successfully):
                sentiments = self.sentiment_analyzer.getSentimentValues(comment)
                for company_id in self.getCompanyIDByDocumentID(comment_id):
                    company_id = company_id[0] # getting rid of the tuple
                    tmp_timestamp = self.convertDateTimeStringToDateTimeObject(timestamp)
                    start_time = tmp_timestamp - datetime.timedelta(minutes=tmp_timestamp.minute % 1,
                             seconds=tmp_timestamp.second,
                             microseconds=tmp_timestamp.microsecond)
                    end_time = start_time + datetime.timedelta(minutes=1)
                    if (self.companyIDAndTimeInSentiments(company_id, start_time, end_time)):
                        sentiment_averages = self.getSentimentValuesByCompanyIDAndDate(company_id, start_time, end_time)
                        print("sentiment averages", sentiment_averages)
                        average_anger = float(sentiment_averages[0])
                        average_anticipation = float(sentiment_averages[1])
                        average_disgust = float(sentiment_averages[2])
                        average_fear = float(sentiment_averages[3])
                        average_joy = float(sentiment_averages[4])
                        average_negative = float(sentiment_averages[5])
                        average_positive = float(sentiment_averages[6])
                        average_sadness = float(sentiment_averages[7])
                        average_surprise = float(sentiment_averages[8])
                        average_trust = float(sentiment_averages[9])
                        number_of_comments = int(sentiment_averages[10])

                        tmp_sentiments = np.asarray([average_anger, average_anticipation, average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, average_surprise, average_trust])
                        tmp_sentiments = np.multiply(tmp_sentiments, float(number_of_comments))
                        cur_sentiments = np.asarray([float(sentiments[0]), float(sentiments[1]), float(sentiments[2]), float(sentiments[3]), float(sentiments[4]), float(sentiments[5]), float(sentiments[6]), float(sentiments[7]), float(sentiments[8]), float(sentiments[9])])
                        new_sentiments = np.add(tmp_sentiments, cur_sentiments)
                        new_avg_sentiments = np.divide(new_sentiments, float(number_of_comments + 1))

                        random_integer = str(random.randint(0,1000)) # delete this, it's just for testing a method
                        with open("databaseconnectionhandlerstats.txt", "a+") as file:
                            file.write(random_integer + " tmp_sentiments"+str(tmp_sentiments) + "\n")
                            file.write(random_integer + " cur_sentiments"+str(cur_sentiments) + "\n")
                            file.write(random_integer + " new_sentiments"+str(new_sentiments) + "\n")
                            file.write(random_integer + " new_avg_sentiments"+str(new_avg_sentiments) + "\n")

                        new_average_anger = float(new_avg_sentiments[0])
                        new_average_anticipation = float(new_avg_sentiments[1])
                        new_average_disgust = float(new_avg_sentiments[2])
                        new_average_fear = float(new_avg_sentiments[3])
                        new_average_joy = float(new_avg_sentiments[4])
                        new_average_negative = float(new_avg_sentiments[5])
                        new_average_positive = float(new_avg_sentiments[6])
                        new_average_sadness = float(new_avg_sentiments[7])
                        new_average_surprise = float(new_avg_sentiments[8])
                        new_average_trust = float(new_avg_sentiments[9])
                        new_number_of_comments = number_of_comments + 1

                        
                        tmp_sql_command = self.updateSentiments(source, company_id, start_time, end_time, new_average_anger, new_average_anticipation, new_average_disgust, new_average_fear, new_average_joy, 
                                              new_average_negative, new_average_positive, new_average_sadness, new_average_surprise, new_average_trust, new_number_of_comments)
                        
                        with open("databaseconnectionhandlerstats.txt", "a+") as file:
                            file.write(random_integer+" tmp_sql_command " + tmp_sql_command + "\n")
                    else:
                        self.insertIntoSentiments(source, company_id, start_time, end_time, float(sentiments[0]), float(sentiments[1]), float(sentiments[2]), float(sentiments[3]), float(sentiments[4]), float(sentiments[5]), float(sentiments[6]), float(sentiments[7]), float(sentiments[8]), float(sentiments[9]), 1)
    
    def getSentimentValuesByCompanyIDAndDate(self, company_id, start_time, end_time):
        #company_id = company_id[0]
        sql_command = "select average_anger, average_anticipation, average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, average_surprise, average_trust,"
        sql_command += "number_of_comments from sentiments where company_id='" + str(company_id) + "' and start_time='" + str(start_time) + "' and end_time='" + str(end_time) + "'"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            #result_set = cursor.fetchone()[0]
            result_set = cursor.fetchone()
            #result_set = cursor.fetchall()
        except Exception as e:
           print("Error getSentimentValuesByCompanyIDAndDate", e)
           print("sql command", sql_command)
        cursor.close()
        db_connection.close()
        return result_set

    def updateSentiments(self, source, company_id, start_time, end_time, average_anger, average_anticipation, 
                             average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, 
                             average_surprise, average_trust, number_of_comments):
        sql_command = "update sentiments set average_anger='" + str(average_anger) + "', " + "average_anticipation='" +str(average_anticipation)+ "', "
        sql_command += "average_disgust='" + str(average_disgust) + "', " + "average_fear='" + str(average_fear) + "', " + "average_joy='" + str(average_joy) + "', "
        sql_command += "average_negative='" + str(average_negative) + "', " + "average_positive='" + str(average_positive) + "', " + "average_sadness='" + str(average_sadness) + "', "
        sql_command += "average_surprise='" + str(average_surprise) + "', " + "average_trust='" + str(average_trust) + "', " +"number_of_comments='"+ str(number_of_comments) +"' where company_id='" + str(company_id) + "' and start_time='"
        sql_command += str(start_time) + "' and end_time='"+str(end_time)+"' and source='"+str(source)+"'" 

        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        cursor.execute(sql_command)
        db_connection.commit()
        cursor.close()
        db_connection.close()

        return sql_command

    def convertDateTimeStringToDateTimeObject(self, timestamp):
        date_time_array =  str(timestamp).split(" ")
        date_array = [int(x) for x in date_time_array[0].split("-")]
        time_array = [int(float(x)) for x in date_time_array[1].split(":")]
        datetimestamp = datetime.datetime(date_array[0], date_array[1], date_array[2], time_array[0], time_array[1], time_array[2])
        return datetimestamp


    def insertIntoSentiments(self, source, company_id, start_time, end_time, average_anger, average_anticipation, 
                             average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, 
                             average_surprise, average_trust, number_of_comments):
        #company_id = company_id[0]
        sql_command = "insert into sentiments (source, company_id, start_time, end_time, average_anger, average_anticipation, average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, average_surprise, average_trust, number_of_comments) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            print("before commit")
            #start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
            #end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

            print("NEW COMMAND")
            new_sql = "insert into sentiments (source, company_id, start_time, end_time, average_anger, average_anticipation, average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, average_surprise, average_trust, number_of_comments) values ('"+ str(source) + "', '" + str(company_id) + "', '" + str(start_time) + "', '" + str(end_time) + "', '" + str(average_anger) + "', '" + str(average_anticipation) + "', '" + str(average_disgust) + "', '" + str(average_fear) + "', '" + str(average_joy) + "', '" + str(average_negative) + "', '" + str(average_positive) + "', '" + str(average_sadness) + "', '" +  str(average_surprise) + "', '" + str(average_trust) + "', '" + str(number_of_comments) + "')"
            '''
            cursor.execute(sql_command, (source, company_id, start_time, end_time, average_anger, average_anticipation, 
                             average_disgust, average_fear, average_joy, average_negative, average_positive, average_sadness, 
                             average_surprise, average_trust, number_of_comments,))
            '''
            cursor.execute(new_sql)
            db_connection.commit()
            print("after commit")
        except Exception as e:
            print("insertIntoSentiments Error", e)

        cursor.close()
        db_connection.close()

    def getCompanyIDByDocumentID(self, document_id):
        sql_command = "select company_id from tags where documents_id=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (document_id,))
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getAllResultsFromTags(self):
        sql_command = "select * from tags"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getAllQueries(self):
        sql_command = "select * from documents"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set        

    def getAllRelatedQueries(self):
        sql_command = "select query, company_id from related_queries"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getAllCompanies(self):
        sql_command = "select symbol, id from company"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getAllDocuments(self):
        sql_command = "select id, comment from documents"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getIdFromComment(self, comment):
        sql_command = "select id from documents where comment=%s"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command, (comment,))
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set


    def insertDocumentIDandTagIDSIntoTags(self, document_id, tag_ids):
        sql_command = "insert into tags (documents_id, company_id) values "
        for tag in tag_ids:
            sql_command += "("+str(document_id)+", "+str(tag)+"),"
        sql_command = sql_command[:-1] #Remove Final Comma
        #print("sql commnad", sql_command)
        if(len(tag_ids) > 0):
            connection_info = self.connect()
            cursor = connection_info[0]
            db_connection = connection_info[1]
            cursor.execute(sql_command)
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return True
        else:
            return False

    def getComment(self, comment_id):
        sql_command = "select comment from documents where id="+str(comment_id)
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchone()[0]
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set

    def getDocumentsCorrespondingCompanies(self):
        sql_command = "select documents.comment, tags.company_id from documents inner join tags on documents.id = tags.documents_id"
        connection_info = self.connect()
        cursor = connection_info[0]
        db_connection = connection_info[1]
        try:
            cursor.execute(sql_command)
            result_set = cursor.fetchall()
        except Exception as e:
            result_set = None
        cursor.close()
        db_connection.close()
        return result_set