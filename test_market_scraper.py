import json
import unittest

import data
import scraper


class TestEncodeItemName(unittest.TestCase):
    def test_encode_item_name_regular(self):
        item = 'Dreams & Nightmares'
        expected = 'Dreams+%26+Nightmares'
        self.assertEqual(scraper.encode_item_name(item), expected)

    def test_encode_item_name_tilde(self):
        item = 'Music Kit | Chipzel, ~Yellow Magic~'
        expected = 'Music+Kit+%7C+Chipzel%2C+%7EYellow+Magic%7E'
        self.assertEqual(scraper.encode_item_name(item), expected)

    def test_encode_item_name_empty(self):
        self.assertEqual(scraper.encode_item_name(''), '')

    def test_encode_item_name_none(self):
        with self.assertRaises(TypeError):
            scraper.encode_item_name(None)


class ValidateEnumValue(unittest.TestCase):
    def test_market_scraper_invalid_app_type(self):
        with self.assertRaises(TypeError):
            app_id = 'cs2'
            scraper.validate_enum_value(app_id, data.Apps, 'app ID')

    def test_market_scraper_invalid_currency_type(self):
        with self.assertRaises(TypeError):
            currency = 'usd'
            scraper.validate_enum_value(currency, data.Currency, 'currency')

    def test_market_scraper_invalid_app_without_value(self):
        with self.assertRaises(TypeError):
            app_id = data.Apps.CS2
            scraper.validate_enum_value(app_id, data.Apps, 'app ID')

    def test_market_scraper_invalid_currency_without_value(self):
        with self.assertRaises(TypeError):
            currency = data.Currency.USD
            scraper.validate_enum_value(currency, data.Currency, 'currency')

    def test_market_scraper_invalid_app(self):
        with self.assertRaises(ValueError):
            app_id = 00000
            scraper.validate_enum_value(app_id, data.Apps, 'app ID')

    def test_market_scraper_invalid_currency(self):
        with self.assertRaises(ValueError):
            currency = 00000
            scraper.validate_enum_value(currency, data.Currency, 'currency')


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
