import json
import unittest

import data.steam_data
import src.scraper.common
import src.scraper.sync


class TestValidateEnumValue(unittest.TestCase):
    def test_non_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            src.scraper.common.validate_enum_value(
                'not_int',
                data.steam_data.Currency,
                'currency',
            )

    def test_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            src.scraper.common.validate_enum_value(
                99999,
                data.steam_data.Currency,
                'currency',
            )

    def test_valid_enum_value_passes(self):
        src.scraper.common.validate_enum_value(
            data.steam_data.Currency.USD.value,
            data.steam_data.Currency,
            'currency',
        )


class TestEncodeItemName(unittest.TestCase):
    def test_encode_item_name_regular(self):
        item_name = 'Dreams & Nightmares'
        expected = 'Dreams+%26+Nightmares'
        self.assertEqual(
            src.scraper.common.encode_item_name(item_name),
            expected,
        )

    def test_encode_item_name_tilde(self):
        item_name = 'Music Kit | Chipzel, ~Yellow Magic~'
        expected = 'Music+Kit+%7C+Chipzel%2C+%7EYellow+Magic%7E'
        self.assertEqual(
            src.scraper.common.encode_item_name(item_name),
            expected,
        )

    def test_encode_item_with_leading_and_trailing_whitespaces(self):
        item_name = '        AWP | Neo-Noir (Factory New)       '
        expected = 'AWP+%7C+Neo-Noir+%28Factory+New%29'
        self.assertEqual(
            src.scraper.common.encode_item_name(item_name),
            expected,
        )

    def test_special_chars_encoding(self):
        item = 'A+B/C: D'
        encoded = src.scraper.common.encode_item_name(item)
        self.assertIn('%2B', encoded)
        self.assertIn('%2F', encoded)
        self.assertIn('%3A', encoded)

    def test_internal_whitespace_preserved(self):
        item = 'Alpha    Beta'
        encoded = src.scraper.common.encode_item_name(item)
        self.assertEqual(encoded, 'Alpha++++Beta')

    def test_encode_item_name_empty(self):
        self.assertEqual(src.scraper.common.encode_item_name(''), '')

    def test_encode_item_name_none(self):
        with self.assertRaises(AttributeError):
            src.scraper.common.encode_item_name(None)


class ValidateParameters(unittest.TestCase):
    def test_market_scraper_invalid_item_name_type(self):
        with self.assertRaises(TypeError):
            src.scraper.common.validate_parameters(
                11111,
                data.steam_data.Apps.CS2.value,
                data.steam_data.Currency.USD.value,
            )

    def test_market_scraper_invalid_app_id_type(self):
        with self.assertRaises(TypeError):
            src.scraper.common.validate_parameters(
                'Dreams & Nightmares Case',
                'CS2',
                data.steam_data.Currency.USD.value,
            )

    def test_market_scraper_invalid_currency_type(self):
        with self.assertRaises(TypeError):
            src.scraper.common.validate_parameters(
                'Dreams & Nightmares Case',
                data.steam_data.Apps.CS2.value,
                'USD',
            )

    def test_market_scraper_item_name_consist_solely_of_whitespace(self):
        with self.assertRaises(ValueError):
            src.scraper.sync.market_scraper_sync(
                '   ',
                data.steam_data.Apps.CS2.value,
                data.steam_data.Currency.USD.value,
            )

    def test_market_scraper_invalid_app_id(self):
        with self.assertRaises(ValueError):
            src.scraper.sync.market_scraper_sync(
                'Dreams & Nightmares Case',
                00000,
                data.steam_data.Currency.USD.value,
            )

    def test_market_scraper_invalid_currency(self):
        with self.assertRaises(ValueError):
            src.scraper.sync.market_scraper_sync(
                'Dreams & Nightmares Case',
                data.steam_data.Apps.CS2.value,
                00000,
            )


class TestMarketScraper(unittest.TestCase):
    def test_valid_response_keys(self):
        response = json.loads(
            src.scraper.sync.market_scraper_sync(
                'Dreams & Nightmares Case',
                data.steam_data.Apps.CS2.value,
                data.steam_data.Currency.USD.value,
            ),
        )
        expected_keys = {'success', 'lowest_price', 'volume', 'median_price'}
        self.assertTrue(expected_keys.issubset(response.keys()))

    def test_invalid_game_for_selected_item(self):
        response = json.loads(
            src.scraper.sync.market_scraper_sync(
                'Dreams & Nightmares Case',
                data.steam_data.Apps.PUBG.value,
                data.steam_data.Currency.USD.value,
            ),
        )
        expected_key = {'success'}
        unexpected_keys = {'success', 'lowest_price', 'volume', 'median_price'}
        self.assertTrue(expected_key.issubset(response.keys()))
        self.assertFalse(unexpected_keys.issubset(response.keys()))


class TestValidateParametersBoundary(unittest.TestCase):
    def test_long_item_name(self):
        long_name = 'A' * 1000
        src.scraper.common.validate_parameters(
            long_name,
            data.steam_data.Apps.CS2.value,
            data.steam_data.Currency.USD.value,
        )

    def test_whitespace_vs_valid(self):
        with self.assertRaises(ValueError):
            src.scraper.common.validate_parameters(
                '   ',
                data.steam_data.Apps.CS2.value,
                data.steam_data.Currency.USD.value,
            )
        src.scraper.common.validate_parameters(
            '  x  ',
            data.steam_data.Apps.CS2.value,
            data.steam_data.Currency.USD.value,
        )


if __name__ == '__main__':
    unittest.main()
