import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from unittest.mock import MagicMock, patch
from scrapper.news_sites.alain import AlainNewsScraper, AlainNewsCategory
from selenium.webdriver.remote.webelement import WebElement

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

class TestAlainNewsScraper(unittest.TestCase):
    def setUp(self):
        self.driver_mock = MagicMock()
        self.scraper = AlainNewsScraper(self.driver_mock)

    def test_get_news_with_no_articles(self):
        self.scraper.get_all_articles_on_page_by_category = MagicMock(return_value=[])
        self.assertEqual(self.scraper.get_news(), [])

    def test_get_news_with_articles(self):
        article_mock = MagicMock(spec=WebElement)
        self.scraper.get_all_articles_on_page_by_category = MagicMock(return_value=[article_mock])
        self.scraper.get_image_url = MagicMock(return_value="image_url")
        self.scraper.get_title = MagicMock(return_value="title")
        self.scraper.get_article_url = MagicMock(return_value="article_url")
        self.scraper.get_highlight = MagicMock(return_value="highlight")
        self.scraper.get_time_publish = MagicMock(return_value="time_publish")

        result = self.scraper.get_news()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {
            "image_url": "image_url",
            "title": "title",
            "article_url": "article_url",
            "highlight": "highlight",
            "time_publish": "time_publish",
            "category": AlainNewsCategory.NEWS.value
        })

    def test_get_news_with_errors(self):
        article_mock = MagicMock(spec=WebElement)
        self.scraper.get_all_articles_on_page_by_category = MagicMock(return_value=[article_mock])
        self.scraper.get_image_url = MagicMock(side_effect=WebDriverException("WebDriverException error occurred while retrieving the image url of the article"))
        self.scraper.get_title = MagicMock(side_effect=WebDriverException("WebDriverException error occurred while retrieving the title of the article"))
        self.scraper.get_article_url = MagicMock(side_effect=WebDriverException("WebDriverException error occurred while retrieving the article url of the article"))
        self.scraper.get_highlight = MagicMock(side_effect=WebDriverException("WebDriverException error occurred while retrieving the highlight of the article"))
        self.scraper.get_time_publish = MagicMock(side_effect=WebDriverException("WebDriverException error occurred while retrieving the time publish of the article"))

        result = self.scraper.get_news()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {
            "image_url": "",
            "title": "",
            "article_url": "",
            "highlight": "",
            "time_publish": "",
            "category": AlainNewsCategory.NEWS.value
        })

if __name__ == '__main__':
    unittest.main()

    