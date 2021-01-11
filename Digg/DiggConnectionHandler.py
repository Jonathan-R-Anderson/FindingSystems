class DiggConnectionHandler:
    def __init__(self, logger):
        self.logger = logger
        self.base_url = "http://digg.com/api/channel/feed.json?full_text=false&format=html&position="
        self.next_position = 0
        self.slug_url = "slug="
        self.slug = ""
        #http://digg.com/api/channel/feed.json?full_text=false&format=html&position=0&slug=donaldtrump
