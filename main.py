import configparser
import json

import engine
import extractor

with open('dummy.json', encoding='utf-8') as f:
    data = json.load(f)
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
engine_inst = engine.Engine(data, 1, 2)
a = engine_inst.scraping_contents()
for i in a:
    e = extractor.Extractor(data, i, config)
    e.download_file()
    e.save_meta_data()
