import json

import requests as requests
from bs4 import BeautifulSoup as bs


class Engine:
    def __init__(self, json_data, start_page):
        self.db_data = json_data
        self.page = start_page

    def scraping_contents(self):
        result = []
        common_data = self.db_data['common_data']
        meta_data = self.db_data['meta_data']
        url = common_data['url']
        headers = {'User-agent': 'Mozilla/5.0'}

        while True:
            params = {common_data['page_tag']: self.page}
            soup = self.get_soup(url, headers, params)
            a_tags = soup.select(common_data['detail_tag'])
            if not a_tags:
                return result
            for i in a_tags:
                data_dict = {}
                inside_url = i['href']
                inside_soup = self.get_soup(inside_url, headers)

                if meta_data['title_tag'] != "":
                    title = inside_soup.select(meta_data['title_tag'])[0].text
                else:
                    title = ""
                data_dict['title'] = title
                if meta_data['author_tag'] != "":
                    author = inside_soup.select(meta_data['author_tag'])[0].text
                else:
                    author = ""
                data_dict['author'] = author
                if meta_data['download_tag'] != "":
                    download = []
                    download_raw = inside_soup.select(meta_data['download_tag'])
                    if download_raw:
                        for download_single in download_raw:
                            download.append(download_single['href'])
                    else:
                        download = []
                else:
                    download = []
                data_dict['download'] = download
                if meta_data['write_date_tag'] != "":
                    write_date = inside_soup.select(meta_data['write_date_tag'])[0].text
                else:
                    write_date = ""
                data_dict['write_date'] = write_date
                if meta_data['contents_tag'] != "":
                    contents = inside_soup.select(meta_data['contents_tag'])[0].text
                else:
                    contents = ""
                data_dict['contents'] = contents
                if meta_data['img_tag'] != "":
                    img_tag = inside_soup.select(meta_data['img_tag'])[0].text
                else:
                    img_tag = ""
                data_dict['img_tag'] = img_tag
                data_dict['url'] = inside_url

                result.append(data_dict)
            self.page = self.page + 1

    @staticmethod
    def get_soup(url, headers, params=None):
        if params is None:
            params = {}
        respond = requests.get(url=url, headers=headers, params=params)
        if respond.status_code != 200:
            raise Exception("상태코드가 200이 아닙니다.")
        soup = bs(respond.text, 'lxml')

        return soup
