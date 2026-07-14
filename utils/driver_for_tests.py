from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# -------------------------------
# Утилита для инициализации WebDriver
# -------------------------------

def get_driver():
    """
    Инициализирует и возвращает экземпляр Chrome WebDriver с необходимыми опциями.

    Returns:
        WebDriver: Экземпляр Selenium WebDriver для Chrome.

    Notes:
        - Используется WebDriver Manager для автоматической установки драйвера.
        - Настроены опции для стабильной работы в разных средах.
        - Опция headless закомментирована для удобства отладки.
    """
    # Настройка опций Chrome
    chrome_options = Options()

    # Для отладки браузера можно раскомментировать headless
    # chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")  # Отключаем sandbox для Linux
    chrome_options.add_argument("--disable-dev-shm-usage")  # Использовать /dev/shm для хранения
    chrome_options.add_argument("--disable-notifications")  # Отключаем уведомления
    chrome_options.add_argument("--disable-gpu")  # Отключаем GPU (для headless)
    chrome_options.add_argument("--disable-webgl")  # Отключаем WebGL
    chrome_options.add_argument("--log-level=3")  # Минимизируем логи
    chrome_options.add_argument("--disable-sync")  # Отключаем синхронизацию Chrome
    chrome_options.add_argument("--no-first-run")  # Игнорируем первый запуск
    chrome_options.add_argument("--disable-search-engine-choice-screen")  # Отключаем экран выбора поисковой системы

    # Инициализация Chrome WebDriver с менеджером драйвера
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Максимизация окна браузера для удобства тестов
    driver.maximize_window()

    return driver