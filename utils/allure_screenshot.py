import allure
from selenium.webdriver.chrome.webdriver import WebDriver


# -------------------------------
# Утилита для работы со скриншотами
# -------------------------------

def attach_screenshot(driver: WebDriver, name: str):
    """
    Прикрепляет скриншот текущего состояния страницы к отчету Allure.

    Args:
        driver (WebDriver): Экземпляр Selenium WebDriver.
        name (str): Название скриншота в отчете Allure.

    Usage:
        attach_screenshot(driver, "failure_screenshot")

    Notes:
        - Скриншот делается в формате PNG.
        - Используется для фиксации состояния страницы при падении теста.
    """
    # Получаем скриншот страницы как PNG
    screenshot = driver.get_screenshot_as_png()

    # Прикрепляем скриншот к отчету Allure
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )