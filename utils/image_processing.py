import cv2
import numpy as np


def process_image(frame):

    kernel = np.ones((5, 5), np.uint8)
    image_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # threshed_image = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 11)

    # bitwise_not_image = cv2.bitwise_not(threshed_image)
    # blur_image = cv2.GaussianBlur(bitwise_not_image, (9, 9), 0)
    # edged_image = cv2.Canny(blur_image, 0, 100)
    dilated_image = cv2.dilate(frame.copy(), kernel, iterations=2)
    cv2.imshow("dilated image", dilated_image)
    cv2.waitKey()
    # eroded_image = cv2.erode(dilated_image, kernel=np.ones((3, 3), np.uint8))
    contour_image, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contour_image, key=cv2.contourArea, reverse=True)
    for cnt in sorted_contours:

        area = cv2.contourArea(cnt)
        if area <= 500:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(image_bgr, [cnt], 0, (0, 255, 0), 1)
        cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.imshow("object detection", image_bgr)
        cv2.waitKey()

    # closing_image = cv2.morphologyEx(threshed_image, cv2.MORPH_OPEN, kernel=kernel, iterations=1)
    cv2.imshow("origin image", frame)
    # cv2.imshow("edged image", edged_image)
    # cv2.imshow("eroded image", eroded_image)
    cv2.waitKey()
