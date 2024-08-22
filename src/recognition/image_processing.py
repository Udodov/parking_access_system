import cv2


def preprocess_image(image):
    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение размытия для уменьшения шума
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)

    # Выделение границ с помощью Canny
    edged = cv2.Canny(blurred, 30, 200)

    return edged, gray
