import allure
from pages.click_events_page import ClickEventsPage


# Тесты для страницы Click Events
@allure.feature("Click Events Page")  # Группа тестов для Allure отчета
class TestClickEvents:

    @allure.title("Проверка текста при нажатии кнопок животных")
    def test_click_events(self, driver):
        """
        Тест проверяет текст, который появляется после клика по кнопкам с животными:
        Cat, Dog, Pig, Cow.

        Аргументы:
            driver: WebDriver, переданный через фикстуру Pytest
        """
        # Создаем объект страницы ClickEventsPage
        page = ClickEventsPage(driver)

        # Открываем страницу
        page.open()

        # Словарь с ожидаемыми результатами для каждой кнопки
        expected_results = {
            "Cat": "Meow!",
            "Dog": "Woof!",
            "Pig": "Oink!",
            "Cow": "Moo!"
        }

        # Проходим по каждой кнопке и проверяем текст
        for animal, expected_text in expected_results.items():
            # Создаем шаг в Allure отчете для наглядности
            with allure.step(f"Кликаем по кнопке {animal} и проверяем текст"):
                # Кликаем на кнопку и получаем текст из блока demo
                actual_text = page.click_button_and_get_text(animal)

                # Проверяем, что текст соответствует ожидаемому
                assert expected_text in actual_text, f"Ожидали '{expected_text}', получили '{actual_text}'"