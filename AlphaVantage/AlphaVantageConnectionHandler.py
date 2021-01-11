import time, threading, urllib, json, datetime, random

class Timer(threading.Thread):
    def __init__(self):
        self.lock = threading.Lock()
        self.num_calls = 0
        self. max_calls = 400
        self.isDead = False
        super(Timer, self).__init__()

    def run(self):
        while(1):
            if (not self.isDead):
                with self.lock:
                    self.num_calls = 0
            else:
                break
            time.sleep(60)

    def closeThread(self):
        self.isDead = True


class AlphaVantageConnectionHandler:
    def __init__(self, apikey, logger):
        self.stopwatch = Timer()
        self.stopwatch.start()
        self.url = "https://www.alphavantage.co/query?"
        self.apikey = apikey
        self.logger = logger

    def getDateFromTimestamp(self, timestamp):
        return str(timestamp).split(" ")[0]

    def getAttribute(self, url):
        while(1):
            try:
                if (self.stopwatch.num_calls < self.stopwatch.max_calls):
                    self.stopwatch.num_calls += 1
                    with urllib.request.urlopen(url) as url:
                        data = json.loads(url.read().decode())
                        return data

            except urllib.error.HTTPError as e:
                if e.code in [429]:
                    self.logger.commit(1, "AlphaVantageConnectionHandler", "getAttribute", e.code)
                    time.sleep(random.randint(15,30))
            except Exception as e:
                self.logger.commit(2, "AlphaVantageConnectionHandler", "getAttribute", e)

    def getOBV(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=OBV&symbol="+company_symbol+"&interval=daily&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: OBV"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getOBV", e)

    def getAD(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=AD&symbol="+company_symbol+"&interval=daily&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: Chaikin A/D"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getAD", e)

    def getTRANGE(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=TRANGE&symbol="+company_symbol+"&interval=daily&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: TRANGE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getTRANGE", e)

    def getBOP(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=BOP&symbol="+company_symbol+"&interval=daily&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: BOP"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getBOP", e)

    def getSAR(self, company_symbol, acceleration, acceleration_maximum, timestamp):
        try:
            tmp_url = self.url+"function=SAR&symbol="+company_symbol+"&interval=daily&acceleration="+acceleration+"&maximum="+acceleration_maximum+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: SAR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getSAR", e)

    def getULTOSC(self, company_symbol, timestamp, timeperiod1, timeperiod2, timeperiod3):
        try:
            tmp_url = self.url+"function=ULTOSC&symbol="+company_symbol+"&interval=daily&timeperiod1="+timeperiod1+"&timeperiod2="+timeperiod2+"&timeperiod3="+timeperiod3+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ULTOSC"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getULTOSC", e)

    def getNATR(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=NATR&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: NATR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getNATR", e)

    def getATR(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=ATR&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ATR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getATR", e)

    def getMIDPRICE(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=MIDPRICE&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MIDPRICE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMIDPRICE", e)

    def getPLUS_DM(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=PLUS_DM&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictonary = {timestamp : data["Technical Analysis: PLUS_DM"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getPLUS_DM", e)

    def getMINUS_DM(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=MINUS_DM&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MINUS_DM"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMINUS_DM", e)

    def getPLUS_DI(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=PLUS_DI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: PLUS_DI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getPLUS_DI", e)

    def getMINUS_DI(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=MINUS_DI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MINUS_DI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMINUS_DI", e)

    def getDX(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=DX&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: DX"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getDX", e)

    def getMFI(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=MFI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MFI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMFI", e)

    def getAROONOSC(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=AROONOSC&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: AROONOSC"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getAROONOSC", e)

    def getCCI(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=CCI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: CCI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getCCI", e)

    def getADXR(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=ADXR&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ADXR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getADXR", e)

    def getADX(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=ADX&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ADX"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getADX", e)

    def getWILLR(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=WILLR&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: WILLR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getWILLR", e)

    def getAROON(self, company_symbol, timestamp, time_period):
        try:
            tmp_url = self.url+"function=AROON&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: AROON"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getAROON", e)

    def getADOSC(self, company_symbol, timestamp, fast_period, slow_period):
        try:
            tmp_url = self.url+"function=ADOSC&symbol="+company_symbol+"&interval=daily&fastperiod="+fast_period+"&slowperiod="+slow_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ADOSC"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getADOSC", e)

    def getSTOCHF(self, company_symbol, timestamp, fast_period, slow_period, matype):
        try:
            tmp_url = self.url+"function=STOCHF&symbol="+company_symbol+"&interval=daily&fastkperiod="+fast_period+"&fastdperiod="+slow_period+"&fastdmatype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: STOCHF"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getSTOCHF", e)

    def getHT_DCPHASE(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_DCPHASE&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_DCPHASE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_DCPHASE", e)

    def getHT_DCPERIOD(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_DCPERIOD&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_DCPERIOD"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_DCPERIOD", e)

    def getHT_TRENDMODE(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_TRENDMODE&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_TRENDMODE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_TRENDMODE", e)

    def getHT_TRENDLINE(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_TRENDLINE&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_TRENDLINE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_TRENDLINE", e)

    def getHT_SINE(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_SINE&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_SINE"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_SINE", e)

    def getHT_PHASOR(self, company_symbol, timestamp, series_type):
        try:
            tmp_url = self.url+"function=HT_PHASOR&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: HT_PHASOR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getHT_PHASOR", e)

    def getMAMA(self, company_symbol, timestamp, series_type, fast_limit, slow_limit):
        try:
            tmp_url = self.url+"function=MAMA&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&fastlimit="+fast_limit+"&slowlimit="+slow_limit+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MAMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMAMA", e)

    def getMACD(self, company_symbol, timestamp, series_type, fast_period, slow_period, signal_period):
        try:
            tmp_url = self.url+"function=MACD&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&fastperiod="+fast_period+"&slowperiod="+slow_period+"&signalperiod="+signal_period+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MACD"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMACD", e)

    def getPPO(self, company_symbol, timestamp, series_type, fast_period, slow_period, matype):
        try:
            tmp_url = self.url+"function=PPO&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&fastperiod="+fast_period+"&slowperiod="+slow_period+"&matype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: PPO"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getPPO", e)

    def getAPO(self, company_symbol, timestamp, series_type, fast_period, slow_period, matype):
        try:
            tmp_url = self.url+"function=APO&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&fastperiod="+fast_period+"&slowperiod="+slow_period+"&matype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: APO"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getAPO", e)

    def getMACDEXT(self, company_symbol, timestamp, series_type, fast_period, slow_period, signal_period, matype, slow_matype, signal_matype):
        try:
            tmp_url = self.url+"function=MACDEXT&symbol="+company_symbol+"&interval=daily&series_type="+series_type+"&fastperiod="+fast_period+"&slowperiod="+slow_period+"&signalperiod="+signal_period+"&fastmatype="+matype+"&slowmatype="+slow_matype+"&signalmatype="+signal_matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MACDEXT"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMACDEXT", e)

    def getTRIX(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=TRIX&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: TRIX"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getTRIX", e)

    def getROCR(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=ROCR&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ROCR"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getROCR", e)

    def getROC(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=ROC&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: ROC"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getROC", e)

    def getCMO(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=CMO&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: CMO"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getCMO", e)

    def getMIDPOINT(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=MIDPOINT&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MIDPOINT"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMIDPOINT", e)

    def getMOM(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=MOM&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: MOM"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getMOM", e)

    def getRSI(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=RSI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: RSI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getRSI", e)

    def getT3(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=T3&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: T3"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getT3", e)

    def getKAMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=KAMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: KAMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getKAMA", e)

    def getTRIMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=TRIMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: TRIMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getTRIMA", e)

    def getTEMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=TEMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: TEMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getTEMA", e)

    def getDEMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=DEMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: DEMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getDEMA", e)

    def getWMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=WMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: WMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getWMA", e)

    def getEMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=EMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: EMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getEMA", e)

    def getSMA(self, company_symbol, timestamp, time_period, series_type):
        try:
            tmp_url = self.url+"function=SMA&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: SMA"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getSMA", e)

    def getBBANDS(self, company_symbol, timestamp, time_period, series_type, deviation_multiplier_1, deviation_multiplier_2, matype):
        try:
            tmp_url = self.url+"function=BBANDS&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&nbdevup="+deviation_multiplier_1+"&nbdevdn="+deviation_multiplier_2+"&matype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: BBANDS"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getBBANDS", e)

    def getSTOCHRSI(self, company_symbol, timestamp, time_period, series_type, fkp, skp, matype):
        try:
            tmp_url = self.url+"function=STOCHRSI&symbol="+company_symbol+"&interval=daily&time_period="+time_period+"&series_type="+series_type+"&fastkperiod="+fkp+"&fastdperiod="+skp+"&fastdmatype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: STOCHRSI"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getSTOCHRSI", e)

    def getSTOCH(self, company_symbol, timestamp, fkp, skp, sdp, skmat, matype):
        try:
            tmp_url = self.url+"function=STOCH&symbol="+company_symbol+"&interval=daily&fastkperiod="+fkp+"&slowkperiod="+skp+"&slowdperiod="+sdp+"&slowkmatype="+skmat+"&slowdmatype="+matype+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Technical Analysis: STOCH"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getSTOCH", e)

    def getDaily(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=TIME_SERIES_DAILY&symbol="+company_symbol+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Time Series (Daily)"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getDaily", e)

    def getDailyAdjClose(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=TIME_SERIES_DAILY_ADJUSTED&symbol="+company_symbol+"&apikey="+self.apikey
            timestamp = self.getDateFromTimestamp(timestamp)
            data = self.getAttribute(tmp_url)
            final_dictionary = {timestamp : data["Time Series (Daily)"][timestamp]}
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getDailyAdjClose", e)

    def getIntraday(self, company_symbol, timestamp):
        try:
            tmp_url = self.url+"function=TIME_SERIES_INTRADAY&symbol="+company_symbol+"&interval=1min&outputsize=full&apikey="+self.apikey
            data = self.getAttribute(tmp_url)
            raw_data = data["Time Series (1min)"]
            date = timestamp.strftime('%Y-%m-%d')
            final_dictionary = {}
            for tmp_date_key in raw_data.keys():
                if (date in tmp_date_key):
                    final_dictionary[tmp_date_key] = raw_data[tmp_date_key]
            return final_dictionary
        except Exception as e:
            self.logger.commit(2, "AlphaVantageConnectionHandler", "getIntraday", e)
