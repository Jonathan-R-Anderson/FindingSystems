import requests, re

class BucketConnectionHandler:
    def __init__(self):
        self.base_url = "http://www.nasdaq.com/"

    def fetchPage(self, url):
        try:
            headers = {
                       "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                       "Accept-Encoding":"gzip, deflate",
                       "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
                       "Connection":"keep-alive",
                       "Host":"www.nasdaq.com",
                       "Referer":"http://www.nasdaq.com",
                       "Upgrade-Insecure-Requests":"1",
                       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
                        }
            response = requests.get(url, headers = headers, verify=False)
            return response.text
        except Exception as e:
            print("Exception", e)


    def getExchanges(self):
        url = self.base_url + "screening/companies-by-industry.aspx"
        data_raw = self.fetchPage(url)
        data_dirty = re.findall(r'span id=\"exchangeshowall\"(.*?)span', data_raw, re.DOTALL)[0]
        data_clean = re.findall(r'\)\"\>(.*?)\<\/a\>', data_dirty)
        return data_clean

    def getIndustries(self):
        url = self.base_url + "screening/companies-by-industry.aspx"
        data_raw = self.fetchPage(url)
        data_dirty = re.findall(r'span id=\"industryshowall\"(.*?)span', data_raw, re.DOTALL)[0]
        data_clean = re.findall(r'\(this,\'industry\',\'(.*?)\'\)\">', data_dirty)
        return data_clean

    def getPageURLS(self, text):
        data_dirty = re.findall(r'main_content_pnpageview(.*?)last', text, re.DOTALL)
        if (len(data_dirty) > 0):
            data_dirty = data_dirty[0]
            data_clean = [x for x in re.findall(r'<li><a href=\"(.*?)\" class=\"pagerlink\">', data_dirty, re.DOTALL) if "id=\"main_content" not in x]
            return data_clean
        else:
            return []

    def getSymbols(self, text):
        symbols = []
        data_dirty = re.findall(r'<h3>(.*?)</h3>', text, re.DOTALL)
        for dirty_symbol in data_dirty:
            symbol = re.findall(r'\r\n\t\t\t\t\t\t            (.*?)</a>\r\n\t\t\t\t\t', dirty_symbol)[0]
            symbols.append(symbol)
        return symbols

    def getSubsector(self, text):
        subsectors = re.findall(r'td style=\"width:105px\">(.*?)</td>', text, re.DOTALL)
        return subsectors

    def getSymbolAndSubsector(self, exchange, industry):
        urls = []
        url = self.base_url + "screening/companies-by-industry.aspx?industry=%s&exchange=%s" % (industry, exchange)
        urls.append(url)
        data_raw = self.fetchPage(url)
        page_urls_array = self.getPageURLS(data_raw)
        symbol_and_subsector = []
        for tmp_url in page_urls_array:
            urls.append(tmp_url)
        for tmp_url in urls:
            data_raw = self.fetchPage(tmp_url)
            symbols = self.getSymbols(data_raw)
            subsectors = self.getSubsector(data_raw)
            for i in range(len(symbols)):
                symbol_and_subsector.append((symbols[i], subsectors[i]))
        return {industry+"-"+exchange : symbol_and_subsector}