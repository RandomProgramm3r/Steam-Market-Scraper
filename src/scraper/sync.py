import json
import urllib.error
import urllib.request

import data.steam_data
import src.scraper.common


def market_scraper_sync(
    item_name: str,
    app_id: int,
    currency: int = data.steam_data.Currency.USD.value,
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
    src.scraper.common.validate_parameters(item_name, app_id, currency)

    encoded_name = src.scraper.common.encode_item_name(item_name)

    url = (
        f'{src.scraper.common.BASE_URL}'
        f'appid={app_id}'
        f'&currency={currency}'
        f'&market_hash_name={encoded_name}'
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            parsed = json.loads(response.read().decode())
            return src.scraper.common.format_response(
                item_name,
                app_id,
                currency,
                parsed,
            )

    except urllib.error.HTTPError as e:
        return f'Server error: {e.code}'
    except urllib.error.URLError:
        return 'Network error. Please check your internet connection.'
    except json.JSONDecodeError:
        return 'Error decoding JSON response from server.'
