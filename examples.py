import asyncio

import data.steam_data
import src.scraper.async_
import src.scraper.sync

# sync
print(
    src.scraper.sync.market_scraper_sync(
        'Dreams & Nightmares Case',
        data.steam_data.Apps.CS2.value,
        data.steam_data.Currency.USD.value,
    ),
)


# async
async def main():
    items = [
        (
            'Dreams & Nightmares Case',
            data.steam_data.Apps.CS2.value,
            data.steam_data.Currency.USD.value,
        ),
        (
            'Mann Co. Supply Crate Key',
            data.steam_data.Apps.TEAM_FORTRESS_2.value,
            data.steam_data.Currency.EUR.value,
        ),
        (
            'Doomsday Hoodie',
            data.steam_data.Apps.PUBG.value,
            data.steam_data.Currency.GBP.value,
        ),
        (
            'AWP | Neo-Noir (Factory New)',
            data.steam_data.Apps.CS2.value,
            data.steam_data.Currency.USD.value,
        ),
        (
            'Snowcamo Jacket',
            data.steam_data.Apps.RUST.value,
            data.steam_data.Currency.CHF.value,
        ),
    ]

    tasks = [
        src.scraper.async_.market_scraper_async(name, app_id, currency)
        for name, app_id, currency in items
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
