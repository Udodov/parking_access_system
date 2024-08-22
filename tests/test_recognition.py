from src.recognition.plate_recognition import recognize_plate


def test_recognize_plate_valid_image():
    # Функция recognize_plate принимает изображение и возвращает номерной знак
    image_path = "tests/data/valid_plate.jpg"
    expected_plate_number = "ABC1234"

    result = recognize_plate(image_path)
    assert result == expected_plate_number, f"Expected {expected_plate_number}, but got {result}"


def test_recognize_plate_invalid_image():
    # Тестируем случай, когда изображение не содержит номерного знака
    image_path = "tests/data/no_plate.jpg"

    result = recognize_plate(image_path)
    assert result is None, f"Expected None for image without a plate, but got {result}"
