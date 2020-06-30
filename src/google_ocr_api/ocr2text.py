import cv2
import numpy as np

from settings import COLUMN_LINE_SPACE, LINE_INTERACTIONS, MAX_ROWS
from src.google_ocr_api.google_ocr import GoogleVisionAPI
from src.result_processing.save_text_json_xml import ImportResult
from utils.image_processing import process_image


def group_text_by_point(full_json_list, frame_path):

    image = cv2.imread(frame_path)
    width = image.shape[1]
    height = image.shape[0]

    empty_image = np.zeros((height, width), np.uint8)
    for page in full_json_list['fullTextAnnotation']['pages']:
        for block in page['blocks']:
            for paragraph in block['paragraphs']:
                for word in paragraph['words']:
                    for symbol in word['symbols']:

                        cen_x = 0
                        cen_y = 0
                        for i in range(4):
                            cen_x += symbol["boundingBox"]["vertices"][i]['x'] / 4.0
                            cen_y += symbol["boundingBox"]["vertices"][i]['y'] / 4.0
                        # cv2.circle(image, (int(cen_x), int(cen_y)), 2, (0, 0, 255), -1)

                        cen_x1 = symbol["boundingBox"]["vertices"][0]['x'] / 2.0 + cen_x / 2
                        cen_y1 = symbol["boundingBox"]["vertices"][0]['y'] / 2.0 + cen_y / 2

                        cen_x2 = symbol["boundingBox"]["vertices"][2]['x'] / 2.0 + cen_x / 2
                        cen_y2 = symbol["boundingBox"]["vertices"][2]['y'] / 2.0 + cen_y / 2

                        # cv2.circle(image, (int(cen_x1), int(cen_y1)), 2, (0, 0, 255), -1)
                        # cv2.circle(image, (int(cen_x2), int(cen_y2)), 2, (0, 0, 255), -1)
                        cv2.line(empty_image, (int(cen_x1), int(cen_y1)), (int(cen_x2), int(cen_y2)),
                                 (255, 255, 255), 5)

    cv2.imshow("center points", empty_image)
    cv2.waitKey(0)
    process_image(empty_image)


class ProcessOCR:

    def __init__(self):

        self.google_ocr = GoogleVisionAPI()
        self.result = ImportResult()
        self.image_rows = 1
        self.txt_json = None
        self.json_list = None
        self.json_val = None

    def __init_json(self, ret_json):

        self.json_list = ret_json['textAnnotations']

        avail_index = 0
        for i, e in reversed(list(enumerate(self.json_list))):

            if e["description"] == "Digitized":
                avail_index = i
                break

        if avail_index != 0:
            first_text = self.json_list[0]["description"]
            self.json_list[0]["description"] = first_text[:first_text.find("Digitized")]
            self.json_val = self.json_list[:avail_index]
            self.txt_json = self.json_list[1:avail_index]
        else:
            self.json_val = self.json_list
            self.txt_json = self.json_list[1:]

    def process_ocr_cloud_data(self, image_path, thread_id):

        ret_json = self.google_ocr.detect_text(path=image_path)
        self.__init_json(ret_json=ret_json)
        self.image_rows = self.get_rows()
        if self.image_rows <= MAX_ROWS * 0.7:
            ocr2text = self.json_list[0]["description"]
        else:
            ocr2text = self.group_by_column_line(frame_path=image_path)

        self.result.import_result(ret_json=self.json_val, text=ocr2text, thresh_id=thread_id)

    def get_rows(self):

        rows = 0
        if self.txt_json:
            word_y = self.txt_json[0]["boundingPoly"]["vertices"][2]["y"]
            for _json in self.txt_json[1:]:

                if abs(word_y - _json["boundingPoly"]["vertices"][2]["y"]) > 5:
                    rows += 1
                    word_y = _json["boundingPoly"]["vertices"][2]["y"]

        return rows

    def distinguish_newspaper(self):

        word_height_list = []
        word_height = abs(self.txt_json[0]["boundingPoly"]["vertices"][0]["y"] -
                          self.txt_json[0]["boundingPoly"]["vertices"][2]["y"])
        word_height_list.append(word_height)
        for _json in self.txt_json:

            json_height = abs(_json["boundingPoly"]["vertices"][0]["y"] - _json["boundingPoly"]["vertices"][2]["y"])
            if abs(word_height - json_height) > 5:
                word_height_list.append(json_height)
                word_height = json_height

        word_height_count = []
        for word_height in word_height_list:

            cnt = 0
            for _json in self.txt_json:

                json_height = abs(_json["boundingPoly"]["vertices"][0]["y"] - _json["boundingPoly"]["vertices"][2]["y"])
                if word_height == json_height:
                    cnt += 1

            word_height_count.append(cnt)

        max_word_height_index = word_height_count.index(max(word_height_count))
        scale_word_height = [int(x / word_height_list[max_word_height_index]) for x in word_height_list]

        for scales in scale_word_height:

            if scales >= 3:
                return True

        return False

    def group_by_column_line(self, frame_path):

        image = cv2.imread(frame_path)
        line_start = self.json_list[0]["boundingPoly"]["vertices"][0]["x"]
        line_end = self.json_list[0]["boundingPoly"]["vertices"][1]["x"]
        lines = np.arange(int((line_end - line_start) * 0.25), int((line_end - line_start) * 0.75),
                          COLUMN_LINE_SPACE)

        bounding_in_lines = []
        for line in lines:

            cnt_bounding = 0
            for _json in self.txt_json:

                if _json["boundingPoly"]["vertices"][0]["x"] <= line <= _json["boundingPoly"]["vertices"][1]["x"]:
                    cnt_bounding += 1

            bounding_in_lines.append(cnt_bounding)

        column_line_index = [i for i, x in enumerate(bounding_in_lines) if x <= LINE_INTERACTIONS]
        column_lines = []

        i = 0
        column_line = 0

        while i != len(column_line_index):

            if i == len(column_line_index) - 1:
                column_lines.append(lines[column_line_index[i]])
                break

            if lines[column_line_index[i + 1]] - lines[column_line_index[i]] == COLUMN_LINE_SPACE:

                column_line += lines[column_line_index[i]]
                cnt = 1

                while lines[column_line_index[i + 1]] - lines[column_line_index[i]] == COLUMN_LINE_SPACE:

                    column_line += lines[column_line_index[i + 1]]
                    cnt += 1
                    i += 1
                    if i == len(column_line_index) - 1:
                        break

                column_lines.append(int(column_line / cnt))
                column_line = 0
                i += 1

            else:

                column_lines.append(lines[column_line_index[i]])
                i += 1

        ocr2text = ""
        if len(column_lines) == 0:

            ocr2text = self.json_list[0]["description"]
        else:

            for i in range(len(column_lines) + 1):

                if i == 0:
                    x_from_coordinate = 0
                    x_to_coordinate = column_lines[0]
                elif i == len(column_lines):
                    x_from_coordinate = column_lines[i - 1]
                    x_to_coordinate = image.shape[1]
                else:
                    x_from_coordinate = column_lines[i - 1]
                    x_to_coordinate = column_lines[i]

                y_coordinate = self.txt_json[0]["boundingPoly"]["vertices"][2]["y"]
                for _json in self.txt_json:

                    if x_from_coordinate <= _json["boundingPoly"]["vertices"][2]["x"] <= x_to_coordinate:

                        if abs(_json["boundingPoly"]["vertices"][2]["y"] - y_coordinate) <= 5:

                            ocr2text += _json["description"] + " "
                        else:

                            ocr2text += "\n" + _json["description"] + " "
                            y_coordinate = _json["boundingPoly"]["vertices"][2]["y"]

                ocr2text += "\n"

        return ocr2text


if __name__ == '__main__':

    path = "/media/mensa/Data/Task/OCR_Punjabi/test_images/Books_Images_12_13 September Di Sarab Hind Inkalabi Conference_41434_16_pages_Page_0010.jpg"
    ProcessOCR().process_ocr_cloud_data(path, 0)
