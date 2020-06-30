import os
import threading

from google.cloud import storage
from settings import BUCKET, ROOT_DIR, BUCKET_PREFIX, THREADING_NUMBER
from src.google_ocr_api.ocr2text import ProcessOCR

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(ROOT_DIR, 'credential',
                                                            'vaulted-acolyte-260903-b4141e76ec6c.json')
os.environ['GOOGLE_PRODUCT'] = 'My First Project'


class StorageData:

    def __init__(self):

        self.process_ocr = ProcessOCR()
        self.saved_file_list = []
        self.bucket = None
        self.data_index = 0
        self.file_list = []
        self.output_file_list = []
        self.ret_file = []
        self.file_dir = "/tmp/temp"
        self.image_download_dir = "/tmp"
        self.progress = 'Init'
        self.state = 0

    def __get_cloud_file_list(self, dir_url):

        gcs = storage.Client()
        self.bucket = gcs.get_bucket(BUCKET)
        prefix = BUCKET_PREFIX + dir_url
        bucket_iterator = self.bucket.list_blobs(prefix=prefix)

        file_list = []
        for resource in bucket_iterator:
            file_list.append(resource)

        return file_list

    def perform_multi_threading(self, dir_url):

        self.file_list = self.__get_cloud_file_list(dir_url=dir_url)
        output_file_blob_list = self.__get_cloud_file_list(dir_url='output/' + dir_url)
        self.output_file_list = [x.name for x in output_file_blob_list]

        threads = list()
        for i in range(THREADING_NUMBER):
            t = threading.Thread(target=self.process_cloud_data, args=(i,))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        return self.ret_file

    def process_cloud_data(self, thread_id, dir_url):

        self.progress = 'Processing'
        self.file_list = self.__get_cloud_file_list(dir_url=dir_url)
        output_file_blob_list = self.__get_cloud_file_list(dir_url='output/' + dir_url)
        self.output_file_list = [x.name for x in output_file_blob_list]

        file_number = len(self.file_list)
        while self.data_index != file_number:
            cloud_file_path_txt = ""
            self.state = int((self.data_index + 1) * 100 / file_number)
            print(self.state)
            try:
                cloud_image_blob = self.file_list[self.data_index]
                self.data_index += 1

                cloud_image_name = cloud_image_blob.name
                cloud_file_txt = cloud_image_name[6:-4] + ".txt"
                cloud_file_json = cloud_image_name[6:-4] + ".json"
                cloud_file_xml = cloud_image_name[6:-4] + ".xml"

                txt_file = self.file_dir + str(thread_id + 1) + ".txt"
                xml_file = self.file_dir + str(thread_id + 1) + ".xml"
                json_file = self.file_dir + str(thread_id + 1) + ".json"

                cloud_file_path_txt = BUCKET_PREFIX + 'output/' + cloud_file_txt
                cloud_file_path_xml = BUCKET_PREFIX + 'output/' + cloud_file_xml
                cloud_file_path_json = BUCKET_PREFIX + 'output/' + cloud_file_json
                if cloud_file_path_txt not in self.output_file_list or \
                        cloud_file_path_xml not in self.output_file_list or \
                        cloud_file_path_json not in self.output_file_list:

                    blob = self.bucket.blob(cloud_image_name)
                    image_download_path = os.path.join(self.image_download_dir, "temp_{}.jpg".format(thread_id + 1))
                    blob.download_to_filename(image_download_path)
                    self.process_ocr.process_ocr_cloud_data(image_path=image_download_path, thread_id=thread_id)

                    self.upload_file_to_cloud(blob_names=[cloud_file_txt, cloud_file_xml, cloud_file_json],
                                              path_to_files=[txt_file, xml_file, json_file])
                    self.ret_file.append(cloud_image_name)

            except Exception as e:
                print(cloud_file_path_txt, e)

        self.progress = 'Finished'
        self.state = 0
        self.ret_file = []
        self.data_index = 0

    def upload_file_to_cloud(self, blob_names, path_to_files):

        for blob_name, path_to_file in zip(blob_names, path_to_files):

            blob_name = BUCKET_PREFIX + "output/" + blob_name
            blob = self.bucket.blob(blob_name)
            if ".txt" in path_to_file:
                blob.upload_from_filename(path_to_file, content_type='text/html; charset=utf-8')
            else:
                blob.upload_from_filename(path_to_file)

