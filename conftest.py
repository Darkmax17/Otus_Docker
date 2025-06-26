import pytest
import datetime
import logging
import os
from selenium import webdriver

def pytest_addoption(parser):
parser.addoption("--browser", action="store", default="chrome", help="Browser name")
parser.addoption("--bv", action="store", default="121.0", help="Browser version")
parser.addoption("--executor", action="store", default="selenoid", help="Selenoid host")
parser.addoption("--url", action="store", default="http://localhost", help="Target app URL")
parser.addoption("--vnc", action="store_true", help="Enable VNC for Selenoid")
parser.addoption("--remote", action="store_true", help="Use remote WebDriver")

def additional_options(options):
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

@pytest.fixture
def browser(request):
# Ensure logs directory exists
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
remote = True  # всегда используем удалённый запуск через Selenoid

executor_url = f"http://{executor}:4444/wd/hub"
logger.info("Executor URL: %s", executor_url)

options = None
driver = None

try:
    if browser_name in ["chrome"]:
        options = webdriver.ChromeOptions()
    elif browser_name in ["firefox"]:
        options = webdriver.FirefoxOptions()
    elif browser_name in ["edge"]:
        options = webdriver.EdgeOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    additional_options(options)

    if remote:
        # capabilities for Selenoid
        capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": vnc,
                "name": request.node.name
            }
        }
        for key, value in capabilities["selenoid:options"].items():
            options.set_capability(f"selenoid:options", capabilities["selenoid:options"])
        options.set_capability("browserVersion", browser_version)

        driver = webdriver.Remote(command_executor=executor_url, options=options)
    else:
        # fallback to local (not used in Jenkins usually)
        driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.logger = logger
    return driver

except Exception as e:
    logger.error("❌ Failed to initialize WebDriver: %s", e)
    raise