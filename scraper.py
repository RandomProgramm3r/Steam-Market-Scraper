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
                f'Invalid {field_name} ({value}): not found in '
                f'{enum_class.__name__}.'
            ),
        )


def encode_item_name(item_name: str) -> str:
    return urllib.parse.quote_plus(item_name).replace('~', '%7E')


def market_scraper(
    item_name: str,
    app_id: int,
    currency: int = data.Currency.USD.value,
) -> str:
    validate_enum_value(app_id, data.Apps, 'app ID')
    validate_enum_value(currency, data.Currency, 'currency')

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
