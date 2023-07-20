import os


class Extractor:
    def __init__(self, data_dict, config):
        self.data_dict = data_dict
        self.config = config

    def download_file(self):
        url = self.data_dict['url']
        save_path = self.config['scraping']['save_path']
        total_path = os.path.join(save_path, "dir")

        os.makedirs(total_path, exist_ok=True)
