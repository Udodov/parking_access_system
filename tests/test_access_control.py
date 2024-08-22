import pytest

from src.access_control.access_manager import AccessManager


@pytest.fixture
def access_manager():
    # Создаем экземпляр AccessManager для использования в тестах
    return AccessManager()


def test_grant_access(access_manager):
    # Предположим, что AccessManager имеет метод grant_access, который возвращает True для разрешенного доступа
    plate_number = "ABC1234"
    access_manager.add_allowed_plate(plate_number)  # Добавляем номер в список разрешенных

    result = access_manager.grant_access(plate_number)
    assert result is True, f"Expected access to be granted for plate {plate_number}, but it was denied"


def test_deny_access(access_manager):
    # Тестируем случай, когда доступ должен быть запрещен
    plate_number = "XYZ9876"

    result = access_manager.grant_access(plate_number)
    assert result is False, f"Expected access to be denied for plate {plate_number}, but it was granted"
