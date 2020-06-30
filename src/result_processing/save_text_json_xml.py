import json
import dicttoxml

from xml.dom.minidom import parseString
from utils.folder_file_management import save_file


class ImportResult:

    def __init__(self):

        self.json_val = []
        self.text = ""
        self.file_path = ""
        self.file_dir = "/tmp/temp"

    def __save_text(self):

        filename_txt = self.file_path + ".txt"
        text = self.text.encode("utf-8")
        text = text.decode(encoding="utf-8")
        save_file(content=text, filename=filename_txt, method="w")

    def __save_json(self):

        filename_json = self.file_path + ".json"
        save_file(content=json.dumps(self.json_val, ensure_ascii=False), filename=filename_json, method="w")

    def __save_xml(self):

        filename_xml = self.file_path + ".xml"
        xml_data = dicttoxml.dicttoxml(self.json_val)
        xml_data = parseString(xml_data).toprettyxml()
        save_file(content=xml_data, filename=filename_xml, method="w")

    def import_result(self, ret_json, text, thresh_id):

        self.json_val = ret_json
        self.text = text
        self.file_path = self.file_dir + str(thresh_id + 1)

        self.__save_text()
        self.__save_json()
        self.__save_xml()
