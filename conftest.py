import os
import datetime
import logging
import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--bv", default="121.0")
    parser.addoption("--executor", default="selenoid")
    parser.addoption("--url", default="http://localhost")
    parser.addoption("--vnc", action="store_true")


def additional_options(options):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")


@pytest.fixture
def browser(request):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(request.node.name)
    log_file = f"logs/{request.node.name}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("=== Test started at %s ===", datetime.datetime.now())
    logger.info("Test name: %s", request.node.name)

    browser_name = request.config.getoption("browser")
    browser_version = request.config.getoption("bv")
    executor = request.config.getoption("executor")
    url = request.config.getoption("url")
    vnc = request.config.getoption("vnc")

    executor_url = f"http://{executor}:4444/wd/hub"
    logger.info("Executor URL: %s", executor_url)

    driver = None
    options = None

    try:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        additional_options(options)

        # Set capabilities for Selenoid
        options.set_capability("browserVersion", browser_version)
        options.set_capability("selenoid:options", {
            "enableVNC": vnc,
            "name": request.node.name
        })

        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options
        )

        driver.maximize_window()
        driver.logger = logger
        return driver

    except Exception as e:
        logger.error("❌ Failed to initialize WebDriver: %s", e)
        raise


@pytest.fixture
def url(request):
    return request.config.getoption("url")
