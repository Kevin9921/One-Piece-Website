import unittest
from Scraper import get_characterData, onlyCanon, formateName
import os

class TestScraper(unittest.TestCase):

    def test_get_characterData(self):
        result = get_characterData()

        # Add your assertions based on the expected behavior of your function
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
    def test_onlyCanon(self):
        # Mock data for testing
        mock_list = [
            ["Data", "jimmy", "Other", "Other", "Other", "SBS", "URL1"],
            ["Data", "Timmy", "Other", "Other", "Other", "Blue databook", "URL2"],
            ["Data", "Kimmy", "Other", "Other", "Other", "Vivre Card", "URL3"],
            ["Data", "Mimmy", "Other", "Other", "Other", "Stay", "URL4"]
        ]
        result = onlyCanon(mock_list)

        check_list = [
            ["Mimmy", "URL4"]
        ]
        self.assertListEqual(result, check_list)

         
           
        
    def test_formatName(self):
        # Mock data for testing
        mock_list = [
            ["Charlotte Katakuri", "URL1"],
            ["Vinsmoke Sanji", "URL2"],
            ["Monkey D. Luffy", "URL3"],
        ]

        result = formateName(mock_list)

        # Add your assertions based on the expected behavior of your function
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

        check_list = [
            ["Katakuri", "URL1"],
            ["Sanji", "URL2"],
            ["Luffy", "URL3"],
        ]
        self.assertListEqual(result, check_list)

            

    # def test_download_image(self):
    #     # Mock data or real data for testing
    #     image_url = "https://onepiece.fandom.com/wiki/"
    #     expected_image_path = 'path/to/expected/image.jpg'

    #     # Call your download_image function or relevant part of your code
    #     download_image(image_url)

    #     # Assertions to check the result
    #     self.assertTrue(os.path.isfile(expected_image_path), "Image file was not created.")

if __name__ == '__main__':
    '''
    unittest.main()
    '''