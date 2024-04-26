from playwright.sync_api._generated import Page

from blat_cli.harvester.command import browser


def test_browser_goes_to_page(mocker):
    url = "https://example.com/"
    with browser(url, headless=True) as page:
        assert page.url == url
        assert isinstance(page, Page)
