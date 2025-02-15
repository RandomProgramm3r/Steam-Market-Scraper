import data
import scraper

if __name__ == '__main__':
    print(
        scraper.market_scraper(
            'Dreams & Nightmares Case',
            data.Apps.CS2.value,
            data.Currency.USD.value,
        ),
    )
    print(
        scraper.market_scraper(
            'Mann Co. Supply Crate Key',
            data.Apps.TEAM_FORTRESS_2.value,
            data.Currency.EUR.value,
        ),
    )
    print(
        scraper.market_scraper(
            'Doomsday Hoodie',
            data.Apps.PUBG.value,
            data.Currency.GBP.value,
        ),
    )
    print(
        scraper.market_scraper(
            'AWP | Neo-Noir (Factory New)',
            data.Apps.CS2.value,
            data.Currency.USD.value,
        ),
    )
    print(
        scraper.market_scraper(
            'Snowcamo Jacket',
            data.Apps.RUST.value,
            data.Currency.CHF.value,
        ),
    )
