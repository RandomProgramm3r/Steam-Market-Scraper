import json
import unittest

import data
import scraper


class TestEncodeItemName(unittest.TestCase):
    def test_encode_item_name_regular(self):
        item_name = 'Dreams & Nightmares'
        expected = 'Dreams+%26+Nightmares'
        self.assertEqual(scraper.encode_item_name(item_name), expected)

    def test_encode_item_name_tilde(self):
        item_name = 'Music Kit | Chipzel, ~Yellow Magic~'
        expected = 'Music+Kit+%7C+Chipzel%2C+%7EYellow+Magic%7E'
        self.assertEqual(scraper.encode_item_name(item_name), expected)

    def test_encode_item_with_leading_and_trailing_whitespaces(self):
        item_name = '        AWP | Neo-Noir (Factory New)       '
        expected = 'AWP+%7C+Neo-Noir+%28Factory+New%29'
        self.assertEqual(scraper.encode_item_name(item_name), expected)

    def test_encode_item_name_empty(self):
        self.assertEqual(scraper.encode_item_name(''), '')

    def test_encode_item_name_none(self):
        with self.assertRaises(AttributeError):
            scraper.encode_item_name(None)


class ValidateParameters(unittest.TestCase):
    def test_market_scraper_invalid_item_name_type(self):
        with self.assertRaises(TypeError):
            scraper.market_scraper(
                11111,
                data.Apps.CS2.value,
                data.Currency.USD.value,
            )

    def test_market_scraper_invalid_app_id_type(self):
        with self.assertRaises(TypeError):
            scraper.validate_parameters(
                'Dreams & Nightmares Case',
                'CS2',
                data.Currency.USD.value,
            )

    def test_market_scraper_invalid_currency_type(self):
        with self.assertRaises(TypeError):
            scraper.validate_parameters(
                'Dreams & Nightmares Case',
                data.Apps.CS2.value,
                'USD',
            )

    def test_market_scraper_item_name_consist_solely_of_whitespace(self):
        with self.assertRaises(ValueError):
            scraper.market_scraper(
                '   ',
                data.Apps.CS2.value,
                data.Currency.USD.value,
            )

    def test_market_scraper_invalid_app_id(self):
        with self.assertRaises(ValueError):
            scraper.market_scraper(
                'Dreams & Nightmares Case',
                00000,
                data.Currency.USD.value,
            )

    def test_market_scraper_invalid_currency(self):
        with self.assertRaises(ValueError):
            scraper.market_scraper(
                'Dreams & Nightmares Case',
                data.Apps.CS2.value,
                00000,
            )


class TestMarketScraper(unittest.TestCase):
    def test_valid_response_keys(self):
        response = json.loads(
            scraper.market_scraper(
                'Dreams & Nightmares Case',
                data.Apps.CS2.value,
                data.Currency.USD.value,
            ),
        )
        expected_keys = {'success', 'lowest_price', 'volume', 'median_price'}
        self.assertTrue(expected_keys.issubset(response.keys()))

    def test_invalid_game_for_selected_item(self):
        response = json.loads(
            scraper.market_scraper(
                'Dreams & Nightmares Case',
                data.Apps.PUBG.value,
                data.Currency.USD.value,
            ),
        )
        expected_key = {'success'}
        unexpected_keys = {'success', 'lowest_price', 'volume', 'median_price'}
        self.assertTrue(expected_key.issubset(response.keys()))
        self.assertFalse(unexpected_keys.issubset(response.keys()))


if __name__ == '__main__':
    unittest.main()
