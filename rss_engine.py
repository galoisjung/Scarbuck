class rss_engine:
    def __init__(self, json_data):
        self.db_data = json_data

    def scraping_contents(self):
        result = []
        common_data = self.db_data['common_data']
        meta_data = self.db_data['meta_data']
        url = common_data['url']
        headers = {'User-agent': 'Mozilla/5.0'}

        