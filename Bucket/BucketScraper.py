class BucketScraper:
    def __init__(self, bucketconnectionhandler):
        self.bucketconnectionhandler = bucketconnectionhandler

    def driver(self):
        exchanges = self.bucketconnectionhandler.getExchanges()
        industries = self.bucketconnectionhandler.getIndustries()
        industries_and_subsectors = [] # array of dicts [{industry-exchange : [(symbol_1, subsector_1), (symbol_2, subsector_2)]}]
        for exchange in exchanges:
            for industry in industries:
                industries_and_subsectors.append(self.bucketconnectionhandler.getSymbolAndSubsector(exchange, industry))
        return industries_and_subsectors