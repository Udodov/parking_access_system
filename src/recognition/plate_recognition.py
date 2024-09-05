import cv2
import numpy as np
import pytesseract
from ultralytics import YOLO

from .image_processing import preprocess_image

# Загрузка модели YOLOv8 из директории models
model_path = "models/yolov8s.pt"
model = YOLO(model_path)


def recognize_plate_from_frame(frame):
    # Предварительная обработка кадра (если требуется)
    preprocessed_frame, gray = preprocess_image(frame)

    # Применение YOLO для поиска номерного знака
    results = model(preprocessed_frame)

    # Анализ результатов детекции
    class_ids = []
    confidences = []
    boxes = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Получаем координаты бокса
            confidence = box.conf[0]
            class_id = int(box.cls[0])

            if confidence > 0.5:  # Порог уверенности
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Нахождение наибольшего по площади бокса (предполагаем, что это номерной знак)
    if len(boxes) > 0:
        max_index = np.argmax(confidences)
        x, y, w, h = boxes[max_index]
        plate_image = frame[y : y + h, x : x + w]

        # Использование Tesseract для распознавания текста
        text = pytesseract.image_to_string(plate_image, config="--psm 8")
        print("Распознанный текст:", text)
        return text

    return None


def process_video_stream():
    # Захват видео с камеры (0 - индекс камеры по умолчанию)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Распознавание номерного знака на текущем кадре
        text = recognize_plate_from_frame(frame)

        # Отображение кадра с распознанным текстом (если есть)
        if text:
            cv2.putText(
                frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

        cv2.imshow("Video", frame)

        # Выход из цикла по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
