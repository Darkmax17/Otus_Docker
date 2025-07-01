import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--app-url",
        action="store",
        default="http://opencart:80",
        help="URL вашего Opencart"
    )
    parser.addoption(
        "--selenoid-url",
        action="store",
        default="http://selenoid:4444/wd/hub",
        help="URL Selenoid WebDriver"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Имя браузера"
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="119.0",
        help="Версия браузера"
    )

@pytest.fixture(scope="session")
def app_url(request):
    return request.config.getoption("--app-url")

@pytest.fixture(scope="session")
def selenoid_url(request):
    return request.config.getoption("--selenoid-url")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def browser_version(request):
    return request.config.getoption("--browser-version")
