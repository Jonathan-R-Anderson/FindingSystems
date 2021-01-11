import urllib3, re, string

class EODDataConnectionHandler:
    """description of class"""
    def __init__(self):
        self.http = urllib3.PoolManager()

    def listExchanges(self):
        r = self.http.request("GET", "http://www.eoddata.com/symbols.aspx")
        if (r.status == 200):
            return re.findall(r'<option.*?value=\"(.*?)\">', str(r.data))
        else:
            return -1

    def listCompanyByExchange(self, symbol):
        results = []

        for letter in list(string.ascii_uppercase):
            #tmp_url = "http://www.eoddata.com/stocklist/"+symbol+"/"+letter+".htm?e="+symbol+"&l="+letter
            tmp_url = "http://www.eoddata.com/stocklist/"+symbol+"/"+letter+".htm"
            r = self.http.request("GET", tmp_url)
            if (r.status == 200):
                results.extend(re.findall(r'/stockquote/'+symbol+'/(.*?).htm', str(r.data)))
        return set(results)

    def getCompanyNameBySymbolAndExchange(self, exchange, company):
        r = self.http.request("GET", "http://www.eoddata.com/stockquote"+"/"+exchange+"/"+company+".htm")
        if (r.status == 200):
            return re.findall(r'<td nowrap>(.*?)</td>', str(r.data))[0]
        else:
            return -1
