import os
import pytesseract
from PIL import Image

try:
    print("Начало выполнения скрипта")
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Получаем путь к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Поднимаемся на уровень выше к корневой директории проекта
    root_dir = os.path.dirname(script_dir)
    
    # Составляем путь к изображению
    image_path = os.path.join(root_dir, 'images', 'a700_37.jpg')
    
    print(f"Путь к изображению: {image_path}")
    print("Попытка открыть изображение")
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл изображения не найден по пути: {image_path}")
    
    image = Image.open(image_path)
    
    print("Изображение открыто успешно")
    print("Попытка распознать текст")
    
    text = pytesseract.image_to_string(image, lang='rus')
    
    print("Текст распознан")
    print(f"Распознанный текст: {text}")

except FileNotFoundError as e:
    print(f"Ошибка: {str(e)}")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

print("Конец выполнения скрипта")
