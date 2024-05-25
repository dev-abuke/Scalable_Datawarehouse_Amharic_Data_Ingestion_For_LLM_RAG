import unittest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from scrapper.news_sites.alain import AlainNewsScraper

class TestAlainNewsScraper(unittest.TestCase):
    def setUp(self):
        self.driver_mock = MagicMock(spec=WebDriver)
        self.scraper = AlainNewsScraper(driver=self.driver_mock)

    def test_scroll_to_bottom_executes_javascript_command(self):
        self.driver_mock.execute_script.return_value = None
        self.scraper.scroll_to_bottom()
        self.driver_mock.execute_script.assert_called_once_with("window.scrollTo(0, document.body.scrollHeight);")

    def test_scroll_to_bottom_raises_exception_on_error(self):
        self.driver_mock.execute_script.side_effect = WebDriverException("Test exception")
        with self.assertRaises(WebDriverException):
            self.scraper.scroll_to_bottom()

if __name__ == '__main__':
    unittest.main()