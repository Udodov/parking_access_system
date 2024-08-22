import cv2
import numpy as np
import pytesseract

from .image_processing import preprocess_image


def recognize_plate(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Предварительная обработка изображения
    preprocessed_image, gray = preprocess_image(image)

    # Поиск контуров и их сортировка по площади
    contours, _ = cv2.findContours(preprocessed_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Поиск контура номерного знака
    screenCnt = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("Номерной знак не найден")
        return ""

    # Маскирование остальной части изображения
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(image, image, mask=mask)

    # Использование Tesseract для распознавания текста
    text = pytesseract.image_to_string(new_image, config='--psm 8')
    print("Распознанный текст:", text)
    return text
