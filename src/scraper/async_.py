import asyncio
import json

import aiohttp

import data.steam_data
import src.scraper.common


async def fetch_price(
    session: aiohttp.ClientSession,
    item_name: str,
    app_id: int,
    currency: int,
) -> str:
    """
    A request is sent asynchronously to the Steam Market and a formatted
    JSON response or error text is returned.
    """
    encoded = src.scraper.common.encode_item_name(item_name)
    url = (
        f'{src.scraper.common.BASE_URL}'
        f'appid={app_id}'
        f'&currency={currency}'
        f'&market_hash_name={encoded}'
    )

    try:
        async with session.get(url, timeout=5) as response:
            text = await response.text()
            parsed = json.loads(text)

            return src.scraper.common.format_response(
                item_name,
                app_id,
                currency,
                parsed,
            )

    except aiohttp.ClientResponseError as e:
        return f'Server error: {e.status}'
    except aiohttp.ClientConnectionError:
        return 'Network error. Please check your internet connection.'
    except asyncio.TimeoutError:
        return 'Timeout error.'
    except json.JSONDecodeError:
        return 'Error decoding JSON response from server.'


async def market_scraper_async(
    item_name: str,
    app_id: int,
    currency: int = data.steam_data.Currency.USD.value,
) -> str:
    """
    Asynchronously fetch the market price for a given Steam item.

    This coroutine validates the input parameters, opens an HTTP session,
    and delegates to the `fetch_price` helper to retrieve live pricing data
    from the Steam market.

    Parameters:
        item_name (str): The exact name of the Steam marketplace item.
        app_id (int): The Steam application ID where the item is listed.
        currency (int, optional): The currency code for price conversion.
            Defaults to USD if not provided.

    Returns:
        str: A formatted result, which may be a JSON string
        (via `format_response`) or an error message if the fetch fails.

    Raises:
        ValueError: If any of `item_name`, `app_id`, or `currency` is invalid.
        aiohttp.ClientError: If the HTTP request to the Steam API fails.
    """

    src.scraper.common.validate_parameters(item_name, app_id, currency)
    async with aiohttp.ClientSession() as session:
        return await fetch_price(session, item_name, app_id, currency)
