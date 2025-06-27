import pytest

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost", help="Base URL")
    parser.addoption("--app-url", action="store", default="http://localhost:8080")
    parser.addoption("--selenoid-url", action="store", default="http://localhost:4444/wd/hub")
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--browser-version", action="store", default="119.0")

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
