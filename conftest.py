import pytest
import datetime
from selenium import webdriver
import logging

default_url = "http://192.168.100.9:8085"
default_executor = "192.168.100.9"
log_level = "DEBUG"


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser for tests"
    )
    parser.addoption("--bv", action="store", help="browser version")
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="enable/disable headless mode: 'true' or 'false'",
    )
    parser.addoption(
        "--remote", action="store_true", help="remote launching by default"
    )
    parser.addoption("--url", action="store", default=default_url)
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--executor", action="store", default=default_executor)


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
    logger.info("===> Test started at %s" % datetime.datetime.now())
    logger.info("===> Test name: %s" % request.node.name)

    remote = request.config.getoption("remote")
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("headless")
    browser_version = request.config.getoption("bv")

    logger.info("===> Browser: %s, version: %s" % (browser_name, browser_version))

    vnc = request.config.getoption("vnc")
    executor = request.config.getoption("executor")
    executor_url = f"http://{executor}:4444/wd/hub"

    driver = None
    options = None

    try:
        if remote:
            if browser_name in ["chrome", "ch"]:
                options = webdriver.ChromeOptions()
            elif browser_name in ["firefox", "ff"]:
                options = webdriver.FirefoxOptions()
            elif browser_name in ["edge", "ed"]:
                options = webdriver.EdgeOptions()

            if options:
                options.set_capability("browserVersion", browser_version)
                options.set_capability("selenoid:options", {"name": request.node.name})
                if vnc:
                    options.set_capability("selenoid:options", {"enableVNC": True})
                driver = webdriver.Remote(command_executor=executor_url, options=options)

        else:
            if browser_name in ["chrome", "ch"]:
                options = webdriver.ChromeOptions()
                additional_option(options)
                if headless or headless is None:
                    options.add_argument("--headless=new")
                driver = webdriver.Chrome(options=options)

            elif browser_name in ["firefox", "ff"]:
                options = webdriver.FirefoxOptions()
                additional_option(options)
                if headless or headless is None:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)

            elif browser_name in ["edge", "ed"]:
                options = webdriver.EdgeOptions()
                additional_option(options)
                if headless or headless is None:
                    options.add_argument("--headless=new")
                driver = webdriver.Edge(options=options)

        if driver is None:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.maximize_window()
        driver.logger = logger  # Добавляем logger к драйверу
        return driver

    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        raise


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
