import allure
from pages.form_page import FormPage
from selenium.webdriver.common.alert import Alert


# -------------------------------
# Тесты для страницы Form Fields
# -------------------------------
@allure.feature("Form Fields")  # Группа тестов для Allure отчета
class TestForm:

    @allure.title("Successful Form Submission")
    @allure.description("Fill all fields, including Message with Automation Tools, and verify success.")
    def test_successful_form_submission(self, driver):
        """
        Тест проверяет успешную отправку формы на странице Form Fields.
        Заполняются все поля, включая Message со списком Automation Tools, и проверяется успешное сообщение.

        Аргументы:
            driver: WebDriver, переданный через фикстуру Pytest
        """
        # Создаем объект страницы FormPage
        form_page = FormPage(driver)

        # -------------------------------
        # Шаг 1: Открытие страницы формы
        # -------------------------------
        with allure.step("Open the form page"):
            form_page.open()  # Открываем страницу и закрываем попапы

        # -------------------------------
        # Шаг 2: Заполнение полей формы
        # -------------------------------
        with allure.step("Fill Name"):
            form_page.fill_name("Test User")  # Вводим имя

        with allure.step("Fill Password"):
            form_page.fill_password("SecurePass123")  # Вводим пароль

        with allure.step("Select Drink"):
            form_page.select_drink()  # Выбираем чекбокс "Water"

        with allure.step("Select Color"):
            form_page.select_color()  # Выбираем радиокнопку "Blue"

        with allure.step("Select Automation preference"):
            form_page.select_automation("yes")  # Выбираем "Yes" в выпадающем списке

        with allure.step("Fill Email"):
            form_page.fill_email("test@example.com")  # Вводим email

        with allure.step("Fill Message with Automation Tools"):
            form_page.fill_message_with_tools()  # Заполняем поле Message списком инструментов

        # -------------------------------
        # Шаг 3: Отправка формы
        # -------------------------------
        with allure.step("Submit the form"):
            form_page.submit_form()  # Прокрутка до кнопки и клик Submit

            # Обрабатываем возможный alert
            try:
                alert = Alert(driver)
                alert_text = alert.text
                alert.accept()  # Подтверждаем alert
                print(f"Alert closed with text: {alert_text}")
            except:
                print("No alert appeared")  # Если alert не появился

        # -------------------------------
        # Шаг 4: Проверка успешного сообщения
        # -------------------------------
        with allure.step("Verify success message"):
            assert form_page.is_success_message_displayed(), "Success message not displayed"  # Проверка сообщения