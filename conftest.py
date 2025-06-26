import pytest
import datetime
import logging
from selenium import webdriver
import os


default_url = "http://localhost"
default_executor = "localhost"
log_level = "DEBUG"

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome/firefox/edge")
    parser.addoption("--bv", action="store", default="100.0", help="Browser version")
    parser.addoption("--headless", action="store_true", help="Enable headless mode")
    parser.addoption("--executor", action="store", default=default_executor, help="Selenoid executor host (no port)")
    parser.addoption("--vnc", action="store_true", help="Enable VNC support")
    parser.addoption("--url", action="store", default=default_url, help="URL of the OpenCart app")
    parser.addoption("--remote", action="store_true", help="Use remote Selenium (Selenoid)")


def additional_option(options):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")


@pytest.fixture
def browser(request):
    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info("===> Test started at %s", datetime.datetime.now())
    logger.info("===> Test name: %s", request.node.name)

    browser_name = request.config.getoption("browser")
    browser_version = request.config.getoption("bv")
    executor = request.config.getoption("executor")
    headless = request.config.getoption("headless")
    remote = request.config.getoption("remote")
    vnc = request.config.getoption("vnc")

    logger.info("===> Browser: %s, Version: %s", browser_name, browser_version)
    executor_url = f"http://{executor}:4444/wd/hub"

    options = None
    driver = None

    try:
        if browser_name in ["chrome", "ch"]:
            options = webdriver.ChromeOptions()
        elif browser_name in ["firefox", "ff"]:
            options = webdriver.FirefoxOptions()
        elif browser_name in ["edge", "ed"]:
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        additional_option(options)

        if headless:
            if browser_name in ["chrome", "ch", "edge", "ed"]:
                options.add_argument("--headless=new")
            else:
                options.add_argument("--headless")

        if remote:
            capabilities = {
                "browserName": browser_name,
                "browserVersion": browser_version,
                "selenoid:options": {
                    "name": request.node.name,
                    "enableVNC": vnc,
                },
            }
            options.set_capability("selenoid:options", capabilities["selenoid:options"])
            options.set_capability("browserVersion", browser_version)
            driver = webdriver.Remote(command_executor=executor_url, options=options)
        else:
            if browser_name == "chrome":
                driver = webdriver.Chrome(options=options)
            elif browser_name == "firefox":
                driver = webdriver.Firefox(options=options)
            elif browser_name == "edge":
                driver = webdriver.Edge(options=options)

        driver.maximize_window()
        driver.logger = logger
        return driver

    except Exception as e:
        logger.error(f"Browser setup failed: {e}")
        raise


@pytest.fixture
def url(request):
    return request.config.getoption("url")

@pytest.fixture
def browser(request):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # ✅ создать папку logs, если её нет
    ...
    file_handler = logging.FileHandler(f"{log_dir}/{request.node.name}.log")
