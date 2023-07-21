import json
import os
import urllib.request as req


class Extractor:
    def __init__(self, json_data, data_dict, config):
        self.db_data = json_data
        self.data_dict = data_dict
        self.config = config
        self.file_path = None
        self.identifier = None

    def download_file(self):
        url = self.data_dict['inside_url']
        save_path = self.config['scraping']['save_path']
        common_data = self.db_data['common_data']
        identifier = self.data_dict['identifier']
        self.identifier = identifier
        file_path = os.path.join('fcms',
                                 common_data['l_cd'],
                                 common_data['m_cd'],
                                 common_data['s_cd'],
                                 common_data['menu_cd'],
                                 str(identifier))
        self.file_path = file_path
        self.data_dict['attach_file'] = []
        # 나중에 count 수정 필요, 경로 관련 정리 필요.
        for count, file_url in enumerate(self.data_dict['download']):
            result = dict()
            ext, real_ext = self.extract_extension(file_url[1])
            total_path = file_path + '/' + ext
            os.makedirs(save_path + '/' + total_path, exist_ok=True)
            download_url = url + file_url[1]
            file_id = identifier + '-' + str(count) + "." + real_ext
            final_path = total_path + '/' + file_id
            req.urlretrieve(download_url, save_path + '/' + final_path)
            result['file_name'] = file_url[0]
            result['file_id'] = file_id
            result['file_path'] = final_path
            result['file_size'] = os.path.getsize(save_path + '/' + final_path)
            self.data_dict['attach_file'].append(result)

    def extract_extension(self, file_name):
        ext = file_name.split('.')[-1].lower()
        real_ext = ext
        if ext == "jpg" or ext == "png":
            ext = "img"
        elif ext != "pdf":
            ext = "doc"

        return ext, real_ext

    def save_meta_data(self):
        result = dict()
        save_path = self.config['scraping']['save_path']
        common_data = self.db_data['common_data']
        result['id'] = "fcms_" + common_data['s_cd'] + "_" + common_data['menu_cd'] + "_" + str(self.identifier)
        result['biz_l_cd'] = ""
        result['biz_m_cd'] = ""
        result['biz_s_cd'] = ""
        result['data_src_l_cd'] = common_data['l_cd']
        result['data_src_m_cd'] = common_data['m_cd']
        result['data_src_s_cd'] = common_data['s_cd']
        result['menu_id'] = common_data['menu_cd']
        result['data_type_l_cd'] = "B001"
        result['data_type_m_cd'] = "203"
        result['data_type_s_cd'] = ""
        result["sec_cd"]: "5"
        result["url"] = self.data_dict['inside_url']
        result["etc"] = ""
        result["attach_file"] = self.data_dict['attach_file']
        result["content"] = self.data_dict['contents']
        result["title"] = self.data_dict['title']
        result["event_date"] = self.data_dict['write_date']
        result["author"] = self.data_dict['author']
        final_path = save_path + '/' + self.file_path + "/txt"
        os.makedirs(final_path, exist_ok=True)
        print(final_path)
        with open(final_path + "/meta.json", 'w') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
