from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time


class FormPage:
    """Модель страницы для тестирования формы на practice-automation.com."""

    def __init__(self, driver: WebDriver):
        """Инициализация FormPage с WebDriver и локаторами элементов.

        Args:
            driver: Экземпляр Selenium WebDriver для взаимодействия с браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Ожидание элементов до 10 секунд

        # URL страницы формы
        self.url = "https://practice-automation.com/form-fields/"

        # Локаторы основных элементов формы
        self.name_input = (By.CSS_SELECTOR, "[data-cy='name-input']")  # Поле Имени (обязательное)
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")  # Поле Пароля
        self.drink_checkbox = (By.CSS_SELECTOR, "[data-cy='drink1']")  # Чекбокс "Water"
        self.color_radio = (By.CSS_SELECTOR, "[data-cy='color2']")  # Радиокнопка "Blue"
        self.automation_select = (By.CSS_SELECTOR, "[data-cy='automation']")  # Выпадающий список
        self.email_input = (By.CSS_SELECTOR, "[data-cy='email']")  # Поле Email
        self.message_textarea = (By.CSS_SELECTOR, "[data-cy='message']")  # Текстовое поле Message
        self.automation_tools = (By.CSS_SELECTOR, "ul li")  # Список Automation Tools
        self.submit_button = (By.CSS_SELECTOR, "[data-cy='submit-btn']")  # Кнопка Submit
        self.name_error = (
        By.XPATH, "//input[@data-cy='name-input']/following-sibling::p[@class='red_txt']")  # Ошибка для поля Имени

        # Локаторы для попапов и баннеров
        self.cookie_banner = (By.CSS_SELECTOR,
                              "[id*='cookie'],[class*='cookie'],[id*='accept'],[class*='accept'],[id*='banner'],[class*='banner'],[id*='modal'],[class*='modal'],[id*='popup'],[class*='popup']")
        self.popup_close_button = (
        By.CSS_SELECTOR, "button.pum-close.popmake-close, button[class*='close'], button[id*='close']")
        self.popup_container = (
        By.CSS_SELECTOR, "div.pum-container.popmake, div[class*='pum-'], div[class*='popmake-']")

        # Переменная для хранения текста последнего алерта
        self.last_alert_text = ""

    def open(self):
        """Открывает страницу формы и закрывает все попапы."""
        self.driver.get(self.url)
        self.wait.until(EC.url_to_be(self.url))  # Ожидание полной загрузки страницы
        self.close_popups()  # Закрытие всех попапов и баннеров

    def close_popups(self):
        """Закрывает все попапы, баннеры и модальные окна на странице."""
        # Закрытие cookie-баннеров
        for banner in self.driver.find_elements(*self.cookie_banner):
            try:
                self.driver.execute_script("arguments[0].click();", banner)
            except Exception:
                pass  # Игнорируем ошибки закрытия баннеров

        # Закрытие кнопок закрытия попапов
        for button in self.driver.find_elements(*self.popup_close_button):
            try:
                self.driver.execute_script("arguments[0].click();", button)
            except Exception:
                pass  # Игнорируем ошибки закрытия кнопок

        # Принудительное скрытие всех попапов через JavaScript
        self.driver.execute_script(
            "document.querySelectorAll('div.pum-container.popmake, div[class*=\"pum-\"], div[class*=\"popmake-\"]').forEach(e => e.style.display='none');"
        )

    def smooth_scroll_to(self, element, steps=5, delay=0.01):
        """Плавная прокрутка к элементу для избежания ElementClickInterceptedException.

        Args:
            element: WebElement для прокрутки.
            steps (int): Количество шагов прокрутки (по умолчанию 5).
            delay (float): Задержка между шагами в секундах (по умолчанию 0.01).
        """
        element_location = element.location_once_scrolled_into_view
        current_scroll = self.driver.execute_script("return window.pageYOffset;")
        target_scroll = element_location['y'] + element.size['height']  # Прокручиваем до низа элемента
        delta = (target_scroll - current_scroll) / steps

        # Выполняем плавную прокрутку по шагам
        for i in range(steps):
            self.driver.execute_script(f"window.scrollBy(0, {delta});")
            time.sleep(delay)

    def scroll_to_bottom(self, delay=0.02):
        """Прокрутка страницы до самого низа для доступа к кнопке Submit.

        Args:
            delay (float): Задержка между шагами прокрутки (по умолчанию 0.02 сек).
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        current_height = 0

        # Прокручиваем по 50px до достижения низа страницы
        while current_height < last_height:
            self.driver.execute_script("window.scrollBy(0, 50);")
            time.sleep(delay)
            current_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")

    def safe_click(self, locator):
        """Безопасный клик по элементу с обработкой попапов и ошибок клика.

        Args:
            locator: Кортеж локатора (By, selector).

        Returns:
            WebElement или None, если элемент не найден.
        """
        self.close_popups()  # Закрываем попапы перед кликом
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.smooth_scroll_to(element)  # Плавная прокрутка к элементу
            try:
                element.click()  # Пробуем обычный клик
            except ElementClickInterceptedException:
                self.close_popups()  # Повторно закрываем попапы
                self.driver.execute_script("arguments[0].click();", element)  # JavaScript-клик
            return element
        except TimeoutException:
            return None  # Возвращаем None, если элемент не найден

    def fill_name(self, name: str):
        """Заполняет поле Имени.

        Args:
            name (str): Имя для заполнения поля.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.name_input))
        self.smooth_scroll_to(element)
        element.clear()  # Очищаем поле
        element.send_keys(name)

    def fill_password(self, password: str):
        """Заполняет поле Пароля.

        Args:
            password (str): Пароль для заполнения поля.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.password_input))
        self.smooth_scroll_to(element)
        element.clear()
        element.send_keys(password)

    def select_drink(self):
        """Выбирает чекбокс напитка "Water"."""
        self.safe_click(self.drink_checkbox)

    def select_color(self):
        """Выбирает радиокнопку цвета "Blue"."""
        self.safe_click(self.color_radio)

    def select_automation(self, option: str = "yes"):
        """Выбирает опцию в выпадающем списке "Do you like automation?".

        Args:
            option (str): Опция для выбора ("yes", "no", "undecided"). По умолчанию "yes".
        """
        self.safe_click(self.automation_select)
        option_locator = (By.CSS_SELECTOR, f"[data-cy='automation-{option}']")
        self.safe_click(option_locator)

    def fill_email(self, email: str):
        """Заполняет поле Email.

        Args:
            email (str): Email-адрес для заполнения поля.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.email_input))
        self.smooth_scroll_to(element)
        element.clear()
        element.send_keys(email)

    def get_automation_tools(self) -> str:
        """Получает список Automation Tools и возвращает его как строку.

        Returns:
            str: Список инструментов, разделённых переносами строк.
        """
        tools = self.wait.until(EC.presence_of_all_elements_located(self.automation_tools))
        return "\n".join([tool.text for tool in tools])

    def fill_message_with_tools(self):
        """Заполняет поле Message списком Automation Tools."""
        element = self.wait.until(EC.element_to_be_clickable(self.message_textarea))
        self.smooth_scroll_to(element)
        element.clear()
        element.send_keys(self.get_automation_tools())

    def submit_form(self):
        """Отправляет форму и обрабатывает алерт/попап после отправки."""
        self.scroll_to_bottom()  # Прокручиваем до кнопки Submit
        submit_btn = self.safe_click(self.submit_button)

        # Обрабатываем алерт, если он появляется
        try:
            alert = self.wait.until(lambda d: d.switch_to.alert)
            self.last_alert_text = alert.text  # Сохраняем текст алерта
            time.sleep(1)
            alert.accept()  # Подтверждаем алерт
        except TimeoutException:
            self.last_alert_text = ""  # Алерт не появился

    def is_success_message_displayed(self) -> bool:
        """Проверяет отображение сообщения об успешной отправке.

        Returns:
            bool: True, если сообщение "Message received!" отображено.
        """
        return self.last_alert_text == "Message received!"

    def is_name_error_displayed(self) -> bool:
        """Проверяет отображение ошибки валидации для поля Имени.

        Returns:
            bool: True, если ошибка отображена.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.name_error))
            return True
        except TimeoutException:
            return False