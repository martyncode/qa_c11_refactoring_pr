"""
Тесты для процедурных хелперов из helpers.py.
Необъодимо переписать их под использование класса CourierAPIClient.
"""
import pytest
import requests
from api_client import CourierAPIClient


@pytest.fixture
def api_client():
    """Клиент для работы с API курьеров."""
    return CourierAPIClient(
        base_url="http://127.0.0.1:5001/api",
        auth_token="test_token_123",
    )


@pytest.fixture
def new_courier_data():
    """Данные для создания нового курьера."""
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321"
    }


@pytest.mark.usefixtures("fake_server")
class TestCourierAPIClient:
    """Тесты для класса CourierAPIClient."""

    def test_get_courier_by_id(self, api_client):
        """Получение курьера с id=1 (зашит в fake_api)."""
        courier = api_client.get_courier_by_id(1)
        assert courier["id"] == 1
        assert courier["first_name"] == "Иван"

    def test_create_courier(self, api_client, new_courier_data):
        """Создание нового курьера."""
        result = api_client.create_courier(new_courier_data)
        assert "id" in result
        assert result["first_name"] == "Мария"

    def test_get_nonexistent_courier_raises(self, api_client):
        """Запрос несуществующего курьера вызывает ошибку 404."""
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_courier_by_id(99999)

    def test_delete_courier(self, api_client):
        """Удаление курьера с id=2 (зашит в fake_api)."""
        result = api_client.delete_courier(2)
        assert result == {"status": "deleted"}