from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SearchPage:
    def __init__(self, driver):
        self.driver = driver  # Инициализация драйвера
        self.search_button = (By.CSS_SELECTOR, "input[value='поиск']")  
    # Метод для поиска по году выпуска
    def search_by_year(self, year):
        self._enter_text(By.ID, "year", str(year))  
        self._click_search_button() 

    # Метод для поиска по названию фильма
    def search_by_title(self, title):
        self._enter_text(By.ID, "find_film", title)  
        self._click_search_button()  

    # Метод для поиска по жанру
    def search_by_genre(self, genre_value):
        # Находим и кликаем по опции жанра (например, 'драма')
        genre_option = self.driver.find_element(By.XPATH, f"//input[@value='{genre_value}'] | //option[text()='драма']")
        genre_option.click()  
        self._click_search_button()  

    # Метод для поиска по актеру и названию фильма
    def search_by_actor(self, title, actor):
        self._enter_text(By.ID, "find_film", title)  
        self._enter_text(By.NAME, "m_act[actor]", actor)  
        self._click_search_button()  

    # Метод для поиска по стране производства
    def search_by_country(self, country_value):
        # Выбор страны из выпадающего списка
        self._select_dropdown_option(By.ID, "country", f"//option[@value='{country_value}' or text()='Россия']")
        self.driver.find_element(*self.search_button).click()  

    # Метод для ввода текста в указанное поле
    def _enter_text(self, by, identifier, text):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, identifier)))  
        element.clear()  
        element.send_keys(text)  

    # Метод для выбора опции из выпадающего списка
    def _select_dropdown_option(self, by, dropdown_id, option_xpath):
        dropdown = self.driver.find_element(by, dropdown_id)  
        dropdown.click()  
        option = self.driver.find_element(By.XPATH, option_xpath)  
        option.click() 

    # Method для нажатия на кнопку поиска
    def _click_search_button(self):
        self.driver.find_element(*self.search_button).click()  

    # Method  ожидания видимости элемента на странице
    def wait_for_element(self, by, value, timeout=8):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    # Method ожидания появления текста в элементе на странице
    def wait_for_element_with_text(self, by, value, text, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)  
            )
        except TimeoutException:
            # Сообщение об ошибке при отсутствии текста в течение заданного времени
            print(f"Элемент с локатором {by} и значением {value}, содержащий текст '{text}', не найден после {timeout} секунд.")
            return False 
