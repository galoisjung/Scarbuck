import os
import shutil
from os.path import dirname


class Sender:
    def __init__(self, config):
        self.save_path = config['scraping']['result_path']
        self.file_path = config['scraping']['save_path']

    def zip_files(self, file_id, file_path):
        final_path = self.save_path + "/" + dirname(file_path) + '/' + file_id
        real_file_path = self.file_path + '/' + file_path
        shutil.make_archive(final_path, "zip", real_file_path)
