import pytest
import requests 
import allure
from diplom.config import BASE_URL, HEADERS

@allure.feature('API Responses')
@pytest.mark.parametrize("endpoint, expected_status", [
    ("/movie/10000", 200),
    ("/movie/search?page=1&limit=10&query=Лобстер", 200),
    ("/person/search?page=1&limit=10&query=Стэйтем", 200),
    ("/movie/search?page=0&limit=0&query=Лобстер", 400),
    ("/movie/1000000000000", 400)
])
def test_api_responses(endpoint, expected_status):
    """
    Универсальный тест для проверки статуса ответа API по различным endpoint'ам.
    """
    with allure.step(f"Отправка GET запроса на {endpoint}"):
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    
    with allure.step(f"Проверка, что статус ответа равен {expected_status}"):
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

@allure.feature('Search by ID')
def test_search_content_by_id():
    """
    Тест API на поиск контента по ID.
    """
    with allure.step("Отправка GET запроса на https://api.kinopoisk.dev/v1.4/movie/10000"):
        response = requests.get(f"{BASE_URL}/movie/10000", headers=HEADERS)
    
    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200

@allure.feature('Search by Title')
def test_search_content_by_title():
    """
    Тест API на поиск контента по названию.
    """
    with allure.step("Отправка GET запроса на https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query=Лобстер"):
        response = requests.get(f"{BASE_URL}/movie/search?page=1&limit=10&query=Лобстер", headers=HEADERS)
    
    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200

@allure.feature('Search Persons by Name')
def test_search_person_by_name():
    """
    Тест API на поиск актеров, режиссеров по имени/фамилии.
    """
    with allure.step("Отправка GET запроса на https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10&query=Стэйтем"):
        response = requests.get(f"{BASE_URL}/person/search?page=1&limit=10&query=Стэйтем", headers=HEADERS)
    
    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200

@allure.feature('Search Content with Invalid Parameters')
def test_search_content_invalid_params():
    """
    Тест API на поиск контента с неверными параметрами запроса.
    """
    with allure.step("Отправка GET запроса на https://api.kinopoisk.dev/v1.4/movie/search?page=0&limit=0&query=Лобстер"):
        response = requests.get(f"{BASE_URL}/movie/search?page=0&limit=0&query=Лобстер", headers=HEADERS)
    
    with allure.step("Проверка, что статус ответа равен 400"):
        assert response.status_code == 400

@allure.feature('Search Content by ID with Out-of-Bounds Value')
def test_search_content_id_out_of_bounds():
    """
    Тест API на поиск контента по ID, выходящему за допустимые значения.
    """
    with allure.step("Отправка GET запроса на https://api.kinopoisk.dev/v1.4/movie/1000000000000"):
        response = requests.get(f"{BASE_URL}/movie/1000000000000", headers=HEADERS)
    
    with allure.step("Проверка, что статус ответа равен 400"):
        assert response.status_code == 400