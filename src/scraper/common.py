import enum
import json
import urllib.parse

import data.steam_data

BASE_URL = 'https://steamcommunity.com/market/priceoverview/?'


def validate_enum_value(
    value: int,
    enum_class: enum.Enum,
    field_name: str,
) -> None:
    """
    Validates that the provided value is an integer and exists
    within the given enum.

    Args:
        value (int): The value to validate.
        enum_class (enum.Enum): The enumeration to check against.
        field_name (str): The name of the field (used in error messages).

    Raises:
        TypeError: If the value is not an integer.
        ValueError: If the value is not found in the provided enumeration.
    """
    if not isinstance(value, int):
        raise TypeError(
            (
                f'Invalid type for {field_name}: expected int, '
                f'got {type(value).__name__}.'
            ),
        )

    if value not in (item.value for item in enum_class):
        raise ValueError(
            (
                f'Invalid {field_name} ({value}): '
                f'not found in {enum_class.__name__}.'
            ),
        )


def validate_parameters(item_name: str, app_id: int, currency: int) -> None:
    """
    Validates the input parameters for the market_scraper function.

    It checks that:
      - item_name is a string.
      - item_name isn't consist solely of whitespace.
      - app_id and currency are valid according to their
      respective enums in data.py.

    Args:
        item_name (str): The full name of the item.
        app_id (int): The application ID to be validated against data.Apps.
        currency (int): The currency code to be validated against
        data.Currency.

    Raises:
        ValueError: If item_name is consist solely of whitespace
        or if app_id/currency are invalid.
        TypeError: If app_id or currency are not integers
        or if item_name isn't str.
    """
    if not isinstance(item_name, str):
        raise TypeError(
            (
                f'Invalid type for item_name: expected str, '
                f'got {type(item_name).__name__}.'
            ),
        )

    if not item_name.strip():
        raise ValueError('Item name cannot consist solely of whitespace.')

    validate_enum_value(app_id, data.steam_data.Apps, 'app ID')
    validate_enum_value(currency, data.steam_data.Currency, 'currency')


def encode_item_name(item_name: str) -> str:
    """
    Encodes the item name for use in a URL.

    The function first removes any leading and trailing whitespace
    from the item name, then applies URL encoding using quote_plus, and finally
    replaces the '~' characterwith '%7E' to ensure proper encoding.

    Args:
        item_name (str): The name of the item.
        Whitespace at the beginning and end is removed.

    Returns:
        str: The URL-encoded item name.
    """
    return urllib.parse.quote_plus(item_name.strip()).replace('~', '%7E')


def format_response(
    item_name: str,
    app_id: int,
    currency: int,
    result: dict | str,
) -> str:
    """
    Construct a standardized response string for the Steam market data.

    This function builds a JSON-formatted string when `result` is a dictionary,
    or returns the raw string otherwise. It enriches the output by inserting
    the game name, currency name, and item name into the result payload if
    they are not already present.

    Args:
        item_name (str): The human-readable name of the item being queried.
        app_id (int): The Steam application ID associated with the item.
        currency (int): Numeric code representing the currency (per Steam API).
        result (dict | str): The price data or error message. If a dict,
            it will be pretty-printed as JSON; if a string, it will be returned
            unchanged.

    Returns:
        str: A JSON-formatted string including `game_name`, `currency_name`,
            `item_name`, and any other data present in `result`, or the raw
            string if `result` is not a dict.

    Raises:
        KeyError: If expected fields in the Steam data lookup are missing.
        TypeError: If `result` is not of type dict or str.
    """

    game_name = data.steam_data.Apps(app_id).name
    currency_name = data.steam_data.Currency(currency).name

    if isinstance(result, dict):
        result.setdefault('game_name', game_name)
        result.setdefault('currency_name', currency_name)
        result.setdefault('item_name', item_name)
        return json.dumps(result, indent=4, ensure_ascii=False)

    return result
