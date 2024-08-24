import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import allure
from search_page import SearchPage
from config import BASE_URL_UI

@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def search_page(driver):
    driver.get(BASE_URL_UI)
    return SearchPage(driver)

@allure.feature('Search by Year')
def test_search_by_year(search_page):
    """
    Тест UI на поиск контента по году.
    """
    with allure.step("Поиск контента по году 2000"):
        search_page.search_by_year(2000)
    
    with allure.step("Проверка, что найденный контент соответствует году 2000"):
        year_element = search_page.wait_for_element(By.CLASS_NAME, "year")
        assert year_element.text == "2000", f"Expected year to be 2000, but got {year_element.text}"

@allure.feature('Search by Title')
def test_search_by_title(search_page):
    """
    Тест UI на поиск контента по названию фильма.
    """
    with allure.step("Поиск контента по названию 'Начало'"):
        search_page.search_by_title("Начало")
    
    with allure.step("Проверка, что найденный контент соответствует фильму 'Inception'"):
        is_content_found = search_page.wait_for_element_with_text(By.CLASS_NAME, "gray", "Inception, 148 мин")
        assert is_content_found, "Expected to find content 'Inception, 148 мин'"

@allure.feature('Search by Genre')
def test_search_by_genre(search_page):
    """
    Тест UI на поиск контента по жанру.
    """
    with allure.step("Поиск контента по жанру 'драма'"):
        search_page.search_by_genre("драма")
    
    with allure.step("Проверка, что найденный контент относится к жанру 'драма'"):
        is_genre_found = search_page.wait_for_element_with_text(By.XPATH, "//span[@class='gray' and contains(., 'драма')]", "драма")
        assert is_genre_found, "Expected to find content with genre 'драма'"

@allure.feature('Search by Actor')
def test_search_by_actor(search_page):
    """
    Тест UI на поиск контента по названию фильма и актеру.
    """
    with allure.step("Поиск контента по названию 'Начало' и актеру 'Леонардо'"):
        search_page.search_by_actor("Начало", "Леонардо")
    
    with allure.step("Проверка, что найденный контент соответствует фильму 'Inception' с актером 'Леонардо'"):
        is_content_found = search_page.wait_for_element_with_text(By.CLASS_NAME, "gray", "Inception, 148 мин")
        assert is_content_found, "Expected to find content 'Inception, 148 мин'"

@allure.feature('Search by Country')
def test_search_by_country(search_page):
    """
    Тест UI на поиск контента по стране.
    """
    with allure.step("Поиск контента по стране 'Россия'"):
        search_page.search_by_country("Россия")
    
    with allure.step("Проверка, что найденный контент соответствует стране 'Россия'"):
        country_element = search_page.wait_for_element(By.CLASS_NAME, "text-blue")
        assert country_element.text == "«Россия»", f"Expected country to be '«Россия»', but got {country_element.text}"
