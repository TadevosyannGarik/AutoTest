from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver


class PopupsPage:
    """
    Page Object для страницы Popups на practice-automation.com.
    Сайт: https://practice-automation.com/popups/
    """

    # URL страницы Popups
    URL = "https://practice-automation.com/popups/"

    def __init__(self, driver: WebDriver):
        """Инициализация PopupsPage с WebDriver и локаторами кнопок.

        Args:
            driver: Экземпляр Selenium WebDriver для взаимодействия с браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Ожидание элементов до 10 секунд

        # Локаторы кнопок для тестирования popups
        self.alert_button = (By.ID, "alert")      # Кнопка Alert
        self.confirm_button = (By.ID, "confirm")  # Кнопка Confirm
        self.prompt_button = (By.ID, "prompt")    # Кнопка Prompt

    def open(self):
        """Открывает страницу Popups и ждет полной загрузки URL."""
        self.driver.get(self.URL)
        self.wait.until(EC.url_to_be(self.URL))  # Ждем, пока URL полностью загрузится

    def click_alert(self) -> str:
        """
        Кликает по кнопке Alert и возвращает текст алерта.

        Returns:
            str: Текст всплывающего alert.
        """
        # Находим кнопку Alert и кликаем по ней
        self.driver.find_element(*self.alert_button).click()

        # Ожидаем появления alert и получаем его текст
        alert = self.wait.until(lambda d: d.switch_to.alert)
        text = alert.text

        # Закрываем alert
        alert.accept()

        return text

    def click_confirm(self, accept=True) -> str:
        """
        Кликает по кнопке Confirm и обрабатывает всплывающее окно.

        Args:
            accept (bool): Если True — принимаем alert, иначе отклоняем.

        Returns:
            str: Текст всплывающего confirm.
        """
        # Находим кнопку Confirm и кликаем
        self.driver.find_element(*self.confirm_button).click()

        # Ожидаем появления confirm и получаем его текст
        alert = self.wait.until(lambda d: d.switch_to.alert)
        text = alert.text

        # Принимаем или отклоняем confirm
        if accept:
            alert.accept()
        else:
            alert.dismiss()

        return text

    def click_prompt(self, input_text="Test") -> str:
        """
        Кликает по кнопке Prompt, вводит текст и принимает его.

        Args:
            input_text (str): Текст для ввода в prompt (по умолчанию "Test").

        Returns:
            str: Текст всплывающего prompt до ввода.
        """
        # Находим кнопку Prompt и кликаем
        self.driver.find_element(*self.prompt_button).click()

        # Ожидаем появления prompt и получаем текст
        alert = self.wait.until(lambda d: d.switch_to.alert)
        text = alert.text

        # Вводим текст и подтверждаем
        alert.send_keys(input_text)
        alert.accept()

        return text