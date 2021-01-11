import threading, os, datetime
from tqdm import tqdm

class ExchangeThread(threading.Thread):
    def __init__(self, exchange_symbol, companies, arguments, alphavantageconnectionhandler, timestamp, databaseconnectionhandler):
        self.exchange_symbol = exchange_symbol
        self.companies = companies
        self.series_type = arguments[0]
        self.period = arguments[1]
        self.time_period = arguments[2]
        self.acceleration_maximum = arguments[3]
        self.acceleration = arguments[4]
        self.multi_time_period = arguments[5]
        self.matype = arguments[6]
        self.signal_period = arguments[7]
        self.deviation_multiplier = arguments[8]
        self.alphavantageconnectionhandler = alphavantageconnectionhandler
        self.timestamp = timestamp
        self.databaseconnectionhandler = databaseconnectionhandler
        super(ExchangeThread, self).__init__()

    def run(self):
        exchange_id = self.databaseconnectionhandler.getExchangeID(self.exchange_symbol)
        print("ExchangeThread progress bar for run for exchange:", self.exchange_symbol)
        for company_symbol in tqdm(self.companies):
            final_dictionary = self.alphavantageconnectionhandler.getIntraday(company_symbol, self.timestamp)
            company_id = self.databaseconnectionhandler.getCompanyID(exchange_id, company_symbol)
            if final_dictionary is not None:
                for date in final_dictionary.keys():
                    tmp_dict = final_dictionary[date]
                    open = tmp_dict["1. open"]
                    high = tmp_dict["2. high"]
                    low = tmp_dict["3. low"]
                    close = tmp_dict["4. close"]
                    volume = tmp_dict["5. volume"]
                    #self.databaseconnectionhandler.insertIntoCompanyValue(company_id, date, open, high, low, close, volume)
                    threading.Thread(target=self.databaseconnectionhandler.insertIntoCompanyValue, args=(company_id, date, open, high, low, close, volume,)).start()
            '''
            print(self.alphavantageconnectionhandler.getOBV(company_symbol, self.timestamp))
            print(self.alphavantageconnectionhandler.getAD(company_symbol, self.timestamp))
            print(self.alphavantageconnectionhandler.getTRANGE(company_symbol, self.timestamp))
            print(self.alphavantageconnectionhandler.getBOP(company_symbol, self.timestamp))
            print(self.alphavantageconnectionhandler.getDailyAdjClose(company_symbol, self.timestamp))
            for acceleration in self.acceleration:
                print(self.alphavantageconnectionhandler.getSAR(company_symbol, acceleration, self.acceleration_maximum, self.timestamp))
            for multi_time_period in self.multi_time_period:
                print(self.alphavantageconnectionhandler.getULTOSC(company_symbol, self.timestamp, str(multi_time_period*1), str(multi_time_period*2), str(multi_time_period*3)))
            for time_period in self.time_period:
                print(self.alphavantageconnectionhandler.getNATR(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getATR(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getMIDPRICE(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getPLUS_DM(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getMINUS_DM(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getPLUS_DI(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getMINUS_DI(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getDX(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getMFI(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getAROONOSC(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getCCI(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getADXR(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getADX(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getWILLR(company_symbol, self.timestamp, time_period))
                print(self.alphavantageconnectionhandler.getAROON(company_symbol, self.timestamp, time_period))
            for fast_period in self.period:
                for slow_period in self.period:
                    print(self.alphavantageconnectionhandler.getADOSC(company_symbol, self.timestamp, fast_period, slow_period))
                    for matype in self.matype:
                        print(self.alphavantageconnectionhandler.getSTOCHF(company_symbol, self.timestamp, fast_period, slow_period, matype))
            for series_type in self.series_type:
                print(self.alphavantageconnectionhandler.getHT_DCPHASE(company_symbol, self.timestamp, series_type))
                print(self.alphavantageconnectionhandler.getHT_DCPERIOD(company_symbol, self.timestamp, series_type))
                print(self.alphavantageconnectionhandler.getHT_TRENDMODE(company_symbol, self.timestamp, series_type))
                print(self.alphavantageconnectionhandler.getHT_TRENDLINE(company_symbol, self.timestamp, series_type))
                print(self.alphavantageconnectionhandler.getHT_SINE(company_symbol, self.timestamp, series_type))
                print(self.alphavantageconnectionhandler.getHT_PHASOR(company_symbol, self.timestamp, series_type))
                for fast_limit in self.acceleration:
                    for slow_limit in self.acceleration:
                        print(self.alphavantageconnectionhandler.getMAMA(company_symbol, self.timestamp, series_type, fast_limit, slow_limit))
                for fast_period in self.period:
                    for slow_period in self.period:
                        print(self.alphavantageconnectionhandler.getMACD(company_symbol, self.timestamp, series_type, fast_period, slow_period, self.signal_period))
                        for matype in self.matype:
                            print(self.alphavantageconnectionhandler.getPPO(company_symbol, self.timestamp, series_type, fast_period, slow_period, matype))
                            print(self.alphavantageconnectionhandler.getAPO(company_symbol, self.timestamp, series_type, fast_period, slow_period, matype))
                            for slow_matype in self.matype:
                                for signal_matype in self.matype:
                                    print(self.alphavantageconnectionhandler.getMACDEXT(company_symbol, self.timestamp, series_type, fast_period, slow_period, self.signal_period, matype, slow_matype, signal_matype))
                for time_period in self.time_period:
                    print(self.alphavantageconnectionhandler.getTRIX(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getROCR(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getROC(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getCMO(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getMIDPOINT(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getMOM(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getRSI(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getT3(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getKAMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getTRIMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getTEMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getDEMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getWMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getEMA(company_symbol, self.timestamp, time_period, series_type))
                    print(self.alphavantageconnectionhandler.getSMA(company_symbol, self.timestamp, time_period, series_type))
                    for matype in self.matype:
                        print(self.alphavantageconnectionhandler.getBBANDS(company_symbol, self.timestamp, time_period, series_type, self.deviation_multiplier, self.deviation_multiplier, matype))
                        for fkp in self.period:
                            for skp in self.period:
                                print(self.alphavantageconnectionhandler.getSTOCHRSI(company_symbol, self.timestamp, time_period, series_type, fkp, skp, matype))
                                for sdp in self.period:
                                    for skmat in self.matype:
                                        print(self.alphavantageconnectionhandler.getSTOCH(company_symbol, self.timestamp, fkp, skp, sdp, skmat, matype))
            '''
            #break # DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE 



class AlphaVantageScraper:
    def __init__(self, timestamp, alphavantageconnectionhandler, eoddataconnectionhandler, databaseconnectionhandler):
        self.alphavantageconnectionhandler = alphavantageconnectionhandler
        self.eoddataconnectionhandler = eoddataconnectionhandler
        self.timestamp = timestamp
        self.databaseconnectionhandler = databaseconnectionhandler

    def xfrange(self, start, stop, step):
        i = 0
        while start + i * step < stop:
            yield start + i * step
            i += 1

    def generateArguments(self):
        series_type = ["close", "open", "high", "low"]
        period = [str(num) for num in list(range(1, 11)) if num % 3 == 0]
        time_period = [str(num) for num in list(range(60, 200)) if num % 50 == 0]
        acceleration_maximum = "0.99"
        acceleration = [str(num) for num in list(self.xfrange(0.1, 0.99, .30))]
        multi_time_period = [str(num) for num in list(range(1, 7)) if num % 2 == 0]
        matype = [str(num) for num in list(range(8)) if num % 4 == 0]
        signal_period = "9"
        deviation_multiplier = "2"
        return series_type, period, time_period, acceleration_maximum, acceleration, multi_time_period, matype, signal_period, deviation_multiplier


    def getProcessIDS(self):
        pwd = os.getcwd()
        filePath = os.path.join(pwd, "processIDS", "processIDS-alphavantage.txt")
        open(filePath, "w+").close()

        with open(filePath, "w+") as f:
            f.write(str(os.getpid()))

    def driver(self):
        self.getProcessIDS()
        exchange_list = self.eoddataconnectionhandler.listExchanges()
        companies_by_exchange = [companies for companies in [self.eoddataconnectionhandler.listCompanyByExchange(exchange) for exchange in exchange_list]]
        arguments = self.generateArguments()
        exchange_threads = []
        for i in range(len(exchange_list)):
            exchange = exchange_list[i]
            companies = companies_by_exchange[i]
            exchange_thread = ExchangeThread(exchange, companies, arguments, self.alphavantageconnectionhandler, self.timestamp, self.databaseconnectionhandler)
            exchange_threads.append(exchange_thread)
            #break #  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE  DELETE DELETE 
        
        print("AlphaVantageScraper progress bar for driver (start thread) for exchanges")
        for thread in tqdm(exchange_threads):
            thread.start()
        print("AlphaVantageScraper progress bar for driver (join thread) for exchanges")
        for thread in tqdm(exchange_threads):
            thread.join()
        self.alphavantageconnectionhandler.stopwatch.closeThread()