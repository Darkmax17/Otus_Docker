import pytest
import datetime
import logging
import os
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption(
        "--app-url", action="store", default="http://localhost:8082",
        help="Base URL приложения OpenCart"
    )
    parser.addoption(
        "--selenoid-url", action="store",
        default="http://selenoid:4444/wd/hub",
        help="URL Selenoid (Remote WebDriver endpoint)"
    )
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Имя браузера (chrome или firefox)"
    )
    parser.addoption(
        "--browser-version", action="store", default="119.0",
        help="Версия браузера"
    )
    parser.addoption(
        "--vnc", action="store_true", default=False,
        help="Включить VNC в Selenoid"
    )

@pytest.fixture(scope="session")
def app_url(request):
    return request.config.getoption("--app-url")

@pytest.fixture(scope="session")
def selenoid_url(request):
    return request.config.getoption("--selenoid-url")

@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def browser_version(request):
    return request.config.getoption("--browser-version")

@pytest.fixture(scope="session")
def vnc(request):
    return request.config.getoption("--vnc")

def _additional_options(options):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

@pytest.fixture
def browser(request, selenoid_url, browser_name, browser_version, vnc):
    # подготовка логирования
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/{request.node.name}.log"
    logger = logging.getLogger(request.node.name)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    logger.info(">>> Test started: %s", request.node.name)

    # выбираем опции браузера
    if browser_name.lower() == "chrome":
        options = webdriver.ChromeOptions()
    elif browser_name.lower() == "firefox":
        options = webdriver.FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    _additional_options(options)

    # capabilities для Selenoid
    options.set_capability("browserVersion", browser_version)
    options.set_capability(
        "selenoid:options",
        {"enableVNC": vnc, "name": request.node.name}
    )

    logger.info("→ Launch remote WebDriver at %s", selenoid_url)
    driver = webdriver.Remote(command_executor=selenoid_url, options=options)
    driver.logger = logger

    yield driver
    logger.info("<<< Test finished: %s", request.node.name)
    driver.quit()

@pytest.fixture
def url(app_url):
    return app_url
