import pytest
from selenium import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
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

@allure.feature('Поиск по году')
def test_search_by_year(search_page):
    """
    Улучшенный UI тест для поиска контента по году и проверки результатов.
    """
    search_year = 2000
    with allure.step(f"Инициация поиска контента по году {search_year}"):
        search_page.search_by_year(search_year)

    with allure.step("Ожидание загрузки результатов поиска"):
        try:
            WebDriverWait(search_page.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
            )
        except TimeoutException:
            allure.attach(
                search_page.driver.get_screenshot_as_png(),
                name="screenshot_search_results_timeout",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Результаты поиска не загрузились в ожидаемое время.")

    with allure.step(f"Проверка, что результаты поиска содержат год {search_year}"):
        try:
            year_elements = search_page.driver.find_elements(By.XPATH, f"//span[contains(@class, 'year') and contains(text(), '{search_year}')]")
            assert len(year_elements) > 0, f"Ожидалось найти год '{search_year}' в результатах, но он не был найден."
        except Exception as e:
            allure.attach(
                search_page.driver.get_screenshot_as_png(),
                name="screenshot_validation_failure",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Не удалось найти год '{search_year}' в результатах поиска. Ошибка: {e}")

    with allure.step("Проверка, что результаты поиска содержат правильный контент"):
        try:
            content_elements = search_page.driver.find_elements(By.CLASS_NAME, "content-item")
            assert any(search_year in element.text for element in content_elements), f"Не найдено контента с годом '{search_year}' в результатах поиска."
        except Exception as e:
            allure.attach(
                search_page.driver.get_screenshot_as_png(),
                name="screenshot_content_verification_failure",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Проверка контента не удалась. Ошибка: {e}")

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

