import configparser
import json

import dao
from duplicate_reducer import Reducer
import engine
import extractor
from config import search_db_uri
from send_to_nifi import Sender

dao = dao.Dao(search_db_uri)
dbs = dao.getting_data('24h')
for db_single in dbs:
    data = json.loads(db_single)
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    engine_inst = engine.Engine(data, 1, 10)
    r = Reducer('./offset')
    a = engine_inst.scraping_contents(r)
    for i in a:
        e = extractor.Extractor(data, i, config)
        identifier = e.get_extracted_identifier()
        e.download_file()
        e.save_meta_data()
        s = Sender(config)
        file_path = e.get_extracted_file_path()
        result = e.get_extracted_result()
        zip_id = result['id']
        s.zip_files(zip_id, file_path)
        r.duplicate_writer(identifier)
