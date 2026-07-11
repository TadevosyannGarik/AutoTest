from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ClickEventsPage:
    """Модель страницы для тестирования событий кликов на practice-automation.com."""

    # URL страницы с событиями кликов
    URL = "https://practice-automation.com/click-events/"

    def __init__(self, driver):
        """Инициализация страницы ClickEventsPage с экземпляром WebDriver.

        Args:
            driver: Экземпляр Selenium WebDriver для взаимодействия с браузером.
        """
        self.driver = driver

    def open(self):
        """Открывает страницу с событиями кликов."""
        self.driver.get(self.URL)

    def click_button_and_get_text(self, button_text: str) -> str:
        """Кликает по кнопке с указанным текстом и возвращает обновлённый текст элемента demo.

        Метод находит кнопку по её тексту, выполняет клик, ожидает изменения текста
        элемента с ID 'demo' и возвращает новый текст.

        Args:
            button_text (str): Текст кнопки для клика.

        Returns:
            str: Обновлённый текст элемента с ID 'demo' после клика.
        """
        # Находит кнопку по её тексту
        button = self.driver.find_element(By.XPATH, f"//button[normalize-space()='{button_text}']")

        # Сохраняет начальный текст элемента demo
        old_text = self.driver.find_element(By.ID, "demo").text

        # Выполняет клик по кнопке
        button.click()

        # Ожидает изменения текста элемента demo
        WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element(By.ID, "demo").text != old_text
        )

        # Возвращает обновлённый текст элемента demo
        return self.driver.find_element(By.ID, "demo").text