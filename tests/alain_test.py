import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from unittest.mock import MagicMock, patch
from scrapper.news_sites.alain import AlainNewsScraper, AlainNewsCategory

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

class TestAlainNewsScraper(unittest.TestCase):

    @patch('scrapper.news_sites.alain.WebDriver')
    def test_initialize_driver_success(self, mock_webdriver):
        # Arrange
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        scraper = AlainNewsScraper()
        category = AlainNewsCategory.BUSINESS
        expected_url = f"{scraper.url}/section/{category.value}/"

        # Act
        scraper.initialize_driver(category)

        # Assert
        mock_webdriver.assert_called_once()
        mock_driver.get.assert_called_once_with(expected_url)

    @patch('scrapper.news_sites.alain.WebDriver')
    def test_initialize_driver_webdriver_exception(self, mock_webdriver):
        # Arrange
        mock_driver = MagicMock()
        mock_driver.get.side_effect = WebDriverException("Error occurred")
        mock_webdriver.return_value = mock_driver
        scraper = AlainNewsScraper()
        category = AlainNewsCategory.BUSINESS

        # Act & Assert
        with self.assertRaises(WebDriverException):
            scraper.initialize_driver(category)

if __name__ == '__main__':
    unittest.main()

    