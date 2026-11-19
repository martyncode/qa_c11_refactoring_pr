"""
Тесты для процедурных хелперов из helpers.py.
Необъодимо переписать их под использование класса CourierAPIClient.
"""
import pytest
import requests
from api_client import CourierAPIClient


@pytest.fixture
def api_client():
   
    return CourierAPIClient(
        base_url="http://127.0.0.1:5001/api",
        auth_token="test_token_123",
    )


@pytest.fixture
def new_courier_data():
   
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321"
    }


@pytest.mark.usefixtures("fake_server")
class TestCourierAPIClient:
   

    def test_get_courier_by_id(self, api_client):
       
        courier = api_client.get_courier_by_id(1)
        assert courier["id"] == 1
        assert courier["first_name"] == "Иван"

    def test_create_courier(self, api_client, new_courier_data):
       
        result = api_client.create_courier(new_courier_data)
        assert "id" in result
        assert result["first_name"] == "Мария"

    def test_get_nonexistent_courier_raises(self, api_client):
       
        with pytest.raises(requests.exceptions.HTTPError):
            api_client.get_courier_by_id(99999)

    def test_delete_courier(self, api_client):
       
        result = api_client.delete_courier(2)
        assert result == {"status": "deleted"}