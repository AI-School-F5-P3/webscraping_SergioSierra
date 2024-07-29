import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from web_scraping_project.scraper import QuoteScraper
from web_scraping_project.models import Quote
from tenacity import RetryError


class TestQuoteScraper(unittest.TestCase):

    @patch('web_scraping_project.scraper.requests.get')
    def test_get_page_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html>Test content</html>"
        mock_get.return_value = mock_response

        scraper = QuoteScraper()
        result = scraper.get_page('http://test.com')

        self.assertEqual(result, "<html>Test content</html>")
        mock_get.assert_called_once_with('http://test.com', timeout=10)

    @patch('web_scraping_project.scraper.requests.get')
    def test_get_page_failure(self, mock_get):
        # Simula errores en todos los intentos
        mock_get.side_effect = RequestException("Error")

        # Crear un scraper con retry deshabilitado para la prueba
        scraper = QuoteScraper()

        # Deshabilitar los reintentos para esta prueba
        with patch('web_scraping_project.scraper.retry', lambda *args, **kwargs: lambda func: func):
            with self.assertRaises(RetryError):
                scraper.get_page('http://test.com')


    @patch.object(QuoteScraper, 'get_page')
    @patch.object(QuoteScraper, 'get_author_bio')
    @patch('web_scraping_project.scraper.sessionmaker')
    def test_get_quotes_from_page(self, mock_sessionmaker, mock_get_author_bio, mock_get_page):
        """Tests if quotes are extracted from a page and added to the database."""

        # Mock HTML with a quote
        mock_get_page.return_value = '''
        <div class="quote">
            <span class="text">"Test quote"</span>
            <small class="author">Author Name<a href="/author/test"></a></small>
            <div class="tags">
                <a class="tag">tag1</a>
                <a class="tag">tag2</a>
            </div>
        </div>
        '''
        mock_get_author_bio.return_value = "Author bio"

        # Mock session behavior
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session.__enter__.return_value = mock_session

        # Create a QuoteScraper instance and call the method
        scraper = QuoteScraper()
        scraper.get_quotes_from_page('http://test.com')

        # Verify session.add calls
        self.assertTrue(mock_session.add.called, "session.add was not called")
        calls = mock_session.add.call_args_list

        # Verify arguments passed to session.add
        self.assertGreater(len(calls), 0, "session.add was not called with any arguments")
        for call in calls:
            args, kwargs = call
            self.assertIsInstance(args[0], Quote, "session.add was not called with a Quote instance")
            # Additional checks for specific quote attributes
            self.assertEqual(args[0].quote, "Test quote")
            self.assertEqual(args[0].author, "Author Name")
            self.assertEqual(args[0].tags, ["tag1", "tag2"])
            self.assertEqual(args[0].bio, "Author bio")  
            
        # Verify session.commit call
        self.assertEqual(mock_session.commit.call_count, 1, "session.commit was not called once")


    def test_parse_quote(self):
        quote_html = '''
        <div class="quote">
            <span class="text">"Test quote"</span>
            <small class="author">Author Name</small>
            <div class="tags">
                <a class="tag">tag1</a>
                <a class="tag">tag2</a>
            </div>
        </div>
        '''
        soup = BeautifulSoup(quote_html, 'html.parser')
        quote_div = soup.find('div', class_='quote')

        scraper = QuoteScraper()
        text, author_name, tags = scraper.parse_quote(quote_div)

        self.assertEqual(text, '"Test quote"')
        self.assertEqual(author_name, 'Author Name')
        self.assertEqual(tags, 'tag1,tag2')

    @patch.object(QuoteScraper, 'get_page')
    def test_get_author_bio(self, mock_get_page):
        mock_get_page.return_value = '''
        <div class="author-details">
            <div class="author-description">
                This is a test author bio.
            </div>
        </div>
        '''

        scraper = QuoteScraper()
        bio = scraper.get_author_bio('/author/test')

        self.assertEqual(bio, "This is a test author bio.")
        mock_get_page.assert_called_once_with('http://quotes.toscrape.com/author/test')

    @patch.object(QuoteScraper, 'get_page')
    @patch.object(QuoteScraper, 'get_quotes_from_page')
    def test_scrape_quotes(self, mock_get_quotes_from_page, mock_get_page):
        mock_get_page.side_effect = [
            "Some quotes",
            "Some more quotes",
            "No quotes found!"
        ]

        scraper = QuoteScraper()
        scraper.scrape_quotes()

        self.assertEqual(mock_get_quotes_from_page.call_count, 2)
        mock_get_quotes_from_page.assert_any_call('http://quotes.toscrape.com/page/1')
        mock_get_quotes_from_page.assert_any_call('http://quotes.toscrape.com/page/2')

if __name__ == '__main__':
    unittest.main()
