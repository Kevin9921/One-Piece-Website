import unittest
from Scraper import get_characterData, onlyCanon, formateName, UrlName
import os

class TestScraper(unittest.TestCase):

    def test_download_image(self):
        # Mock data or real data for testing
        image_url = 'https://example.com/image.jpg'
        expected_image_path = 'path/to/expected/image.jpg'

        # Call your download_image function or relevant part of your code
        download_image(image_url)

        # Assertions to check the result
        self.assertTrue(os.path.isfile(expected_image_path), "Image file was not created.")

if __name__ == '__main__':
    unittest.main()