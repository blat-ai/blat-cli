import pytest
from playwright.sync_api._generated import Page

from blat_cli.harvester.command import browser
from blat_cli.init.command import install_playwright


@pytest.fixture
def pw_chromium(tmp_config):
    install_playwright(tmp_config / "browsers", with_deps=False)
    return tmp_config / "browsers"


def test_browser_goes_to_page(pw_chromium):
    url = "https://example.com/"
    with browser(url, headless=True) as page:
        assert page.url == url
        assert isinstance(page, Page)
