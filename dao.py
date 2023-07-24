from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

import model
from model import WebCrawler


class Dao:
    def __init__(self, sql_url):
        self.sql_url = sql_url
        engine = create_engine(sql_url, echo=False)
        self.Session = sessionmaker(bind=engine)

    def getting_data(self, hour):
        s = self.Session()
        data = s.query(WebCrawler)
        filtered_db = data.filter(and_(WebCrawler.use_yn == 'Y',
                                       WebCrawler.clct_cycl == hour,
                                       WebCrawler.data_orig_mid_cls_cd != '208'))
        result = [i.meta_info_conts for i in filtered_db]

        return result
