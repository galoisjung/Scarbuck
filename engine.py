import json
from time import sleep

import requests as requests
from bs4 import BeautifulSoup as bs

from urllib.parse import urlparse, parse_qs
from fake_useragent import UserAgent
import hashlib

import duplicate_reducer


class Engine:
    def __init__(self, json_data, start_page, end_page=float("inf")):
        self.db_data = json_data
        self.page = start_page
        self.end_page = end_page

    def scraping_contents(self, reducer):
        result = []
        common_data = self.db_data['common_data']
        meta_data = self.db_data['meta_data']
        event_data = self.db_data['event_data']
        url = common_data['url']

        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        path = parsed_url.path
        ua = UserAgent(verify_ssl=False)
        user_agent = ua.random
        headers = {'User-agent': '{}'.format(user_agent)}

        while True:
            # params = {common_data['page_tag']: self.page}

            if event_data['page_type'] == "query":
                params[event_data['page_tag']] = [self.page]
                soup = self.get_soup(url, headers, params)
                a_tags = soup.select(common_data['detail_tag'])
            elif event_data['page_type'] == "path":
                url = scheme + '://' + netloc + path + '/' + event_data['page_tag'].format(self.page)
                print(url)
                soup = self.get_soup(url, headers)
                a_tags = soup.select(common_data['detail_tag'])
            else:
                a_tags = []
            # page detecting
            print(self.page)
            print(self.end_page)

            if not a_tags or self.page > self.end_page:
                return result
            for i in a_tags:
                data_dict = {}
                inside_url = i['href']

                if inside_url.startswith('/'):
                    p = urlparse(url)
                    inside_url = p.scheme + "://" + p.netloc + inside_url

                if common_data['identifier'] != "":
                    identifier = common_data['identifier']
                    q = urlparse(inside_url).query
                    identifier = parse_qs(q)[identifier][0]
                else:
                    b = bytes(inside_url, 'utf-8')
                    identifier = int.from_bytes(hashlib.sha256(b).digest()[:4], 'little')
                data_dict['identifier'] = identifier
                if reducer.duplicate_checker(identifier):
                    continue
                inside_soup = self.get_soup(inside_url, headers)

                title = self.tag_classifier('title_tag', inside_soup, meta_data)
                data_dict['title'] = title
                author = self.tag_classifier('author_tag', inside_soup, meta_data)
                data_dict['author'] = author
                write_date = self.tag_classifier('write_date_tag', inside_soup, meta_data)
                data_dict['write_date'] = write_date
                contents = self.tag_classifier('contents_tag', inside_soup, meta_data)
                data_dict['contents'] = contents

                if meta_data['download_tag'] != "":
                    download = []
                    download_raw = inside_soup.select(meta_data['download_tag'])
                    if download_raw:
                        for download_single in download_raw:
                            download.append((download_single.text, download_single['href']))
                    else:
                        download = []
                else:
                    download = []

                if meta_data['img_tag'] != "":
                    image_raw = inside_soup.select(meta_data['img_tag'])
                    print(image_raw)
                    if image_raw:
                        for image_single in image_raw:
                            download.append(('', image_single['src']))

                data_dict['download'] = download

                data_dict['inside_url'] = inside_url

                result.append(data_dict)
            self.page = self.page + 1

    @staticmethod
    def get_soup(url, headers, params=None):
        if params is None:
            params = {}
        respond = requests.get(url=url, headers=headers, params=params)
        if respond.status_code != 200:
            print(respond.status_code)
            raise Exception("상태코드가 200이 아닙니다.")
        soup = bs(respond.text, 'lxml')

        return soup

    @staticmethod
    def tag_classifier(tag, inside_soup, meta_data):
        if meta_data[tag] != "" and inside_soup.select(meta_data[tag]):
            result = inside_soup.select(meta_data[tag])[0].text
        else:
            result = ""

        return result
