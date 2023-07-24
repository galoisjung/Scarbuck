from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WebCrawler(Base):
    __bind_key__ = 'search'
    __table_args__ = {"schema": "search"}
    __tablename__ = 'aif_web_clct_trgt_admn'
    web_clct_trgt_id = Column(Integer, primary_key=True)
    data_orig_big_cls_cd = Column(String(30))
    data_orig_mid_cls_cd = Column(String(30))
    data_orig_sm_cls_cd = Column(String(30))
    menu_cd = Column(String(30))
    tmplt_cd = Column(String(30))
    clct_cycl = Column(String(30))
    use_yn = Column(String(1), server_default='Y')
    rcnt_clct_dttm = Column(TIMESTAMP, default=func.timezone('UTC', func.now()))
    rcnt_clct_rslt = Column(String(4000))
    meta_info_conts = Column(String(4000))
    chrg_clerk_nm = Column(String(100))
