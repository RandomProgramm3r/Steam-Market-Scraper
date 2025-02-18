import enum
import json
import urllib.error
import urllib.parse
import urllib.request

import data


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

    validate_enum_value(app_id, data.Apps, 'app ID')
    validate_enum_value(currency, data.Currency, 'currency')


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


def market_scraper(
    item_name: str,
    app_id: int,
    currency: int = data.Currency.USD.value,
) -> str:
    """
    Retrieves data from the Steam Community Market for the specified item.

    The function validates the input parameters, encodes the item name,
    constructs the URL, and performs an HTTP request. It returns a formatted
    JSON response or an error message.

    Args:
        item_name (str): The full name of the item.
        app_id (int): The application ID for the request.
        currency (int, optional): The currency code.
        Defaults to data.Currency.USD.value. (USD)

    Returns:
        str: A formatted JSON response or an error message.
    """
    validate_parameters(item_name, app_id, currency)

    encoded_name = encode_item_name(item_name)

    base_url = 'https://steamcommunity.com/market/priceoverview/?'

    url = (
        f'{base_url}'
        f'appid={app_id}'
        f'&currency={currency}'
        f'&market_hash_name={encoded_name}'
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            result = json.loads(response.read().decode())

            if isinstance(result, dict):
                return json.dumps(result, indent=4, ensure_ascii=False)

            return result

    except urllib.error.HTTPError as e:
        return f'Server error: {e.code}'
    except urllib.error.URLError:
        return 'Network error. Please check your internet connection.'
    except json.JSONDecodeError:
        return 'Error decoding JSON response from server.'
