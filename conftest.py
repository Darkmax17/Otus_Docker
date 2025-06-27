import pytest
import datetime
import logging
import os
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost:8080")
    parser.addoption("--executor", action="store", default="http://localhost:4444/wd/hub")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--bv", action="store", default="119.0")
    parser.addoption("--vnc", action="store_true")

@pytest.fixture
def config(request):
    return {
        "browser": request.config.getoption("--browser"),
        "bv": request.config.getoption("--bv"),
        "executor": request.config.getoption("--executor"),
        "vnc": request.config.getoption("--vnc"),
        "url": request.config.getoption("--url")
    }
def additional_options(options):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

@pytest.fixture
def browser(request):
    # Создаём папку под логи, если нет
    os.makedirs("logs", exist_ok=True)

    # Настраиваем логгер на каждый тест
    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("=== Test started at %s ===", datetime.datetime.now())
    logger.info("Test name: %s", request.node.name)

    # Считываем опции
    browser_name    = request.config.getoption("browser")
    browser_version = request.config.getoption("bv")
    executor        = request.config.getoption("executor").rstrip('/')
    target_url      = request.config.getoption("url")
    vnc             = request.config.getoption("vnc")
    # Всегда через Selenoid
    remote          = True

    # Формируем полный URL для Remote WebDriver
    executor_url = f"http://{executor}/wd/hub"
    logger.info("Executor URL: %s", executor_url)

    # Инициализация опций и драйвера
    try:
        # Выбор опций под конкретный браузер
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Общие опции (headless можно добавить по флагу)
        additional_options(options)

        if remote:
            # Устанавливаем capabilities для Selenoid
            options.set_capability("browserName", browser_name)
            options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": vnc,
                "name": request.node.name
            })

            driver = webdriver.Remote(command_executor=executor_url, options=options)
        else:
            # Локальный запуск (не используется на Jenkins)
            driver = webdriver.Chrome(options=options)

        driver.maximize_window()
        driver.logger = logger
        return driver

    except Exception as e:
        logger.error("❌ Failed to initialize WebDriver: %s", e)
        raise