import configparser
import json

import engine

with open('dummy.json', encoding='utf-8') as f:
    data = json.load(f)
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


engine_inst = engine.Engine(data, 517)
a = engine_inst.scraping_contents()
print(a)