import allure
from pages.popups_page import PopupsPage


# -------------------------------
# Тесты для страницы Popups
# -------------------------------
@allure.feature("Popups Page")  # Группа тестов для Allure отчета
class TestPopups:

    @allure.title("Test all popup types: Alert, Confirm, Prompt")
    @allure.description(
        "Проверка работы всех видов попапов на странице Popups: alert, confirm (accept/dismiss) и prompt."
    )
    def test_popups(self, driver):
        """
        Тест проверяет все типы попапов на странице Popups.

        Аргументы:
            driver: WebDriver, переданный через фикстуру Pytest
        """
        # Создаем объект страницы PopupsPage
        page = PopupsPage(driver)

        # -------------------------------
        # Шаг 1: Открытие страницы
        # -------------------------------
        with allure.step("Open Popups page"):
            page.open()  # Открываем страницу и ждем загрузки

        # -------------------------------
        # Шаг 2: Проверка Alert popup
        # -------------------------------
        with allure.step("Click Alert popup and get text"):
            alert_text = page.click_alert()  # Кликаем на кнопку Alert и принимаем
            print("Alert text:", alert_text)  # Выводим текст в консоль

        # -------------------------------
        # Шаг 3: Проверка Confirm popup (accept)
        # -------------------------------
        with allure.step("Click Confirm popup and accept"):
            confirm_text = page.click_confirm(accept=True)  # Принимаем confirm
            print("Confirm accepted text:", confirm_text)

        # -------------------------------
        # Шаг 4: Проверка Confirm popup (dismiss)
        # -------------------------------
        with allure.step("Click Confirm popup and dismiss"):
            confirm_text_dismiss = page.click_confirm(accept=False)  # Отменяем confirm
            print("Confirm dismissed text:", confirm_text_dismiss)

        # -------------------------------
        # Шаг 5: Проверка Prompt popup
        # -------------------------------
        with allure.step("Click Prompt popup and input text"):
            prompt_text = page.click_prompt("Hello!")  # Вводим текст в prompt и принимаем
            print("Prompt text:", prompt_text)

print("Hello World")
print("Hello World")
# Изменение из второй ветки