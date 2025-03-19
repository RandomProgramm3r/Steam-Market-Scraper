import enum


class Apps(enum.IntEnum):
    TEAM_FORTRESS_2 = 440
    DOTA_2 = 570
    CS2 = 730
    RUST = 252490
    PUBG = 578080


class Currency(enum.IntEnum):
    # ISO 4217
    USD = 1  # United States dollar
    GBP = 2  # Pound sterling
    EUR = 3  # Euro
    CHF = 4  # Swiss franc
    RUB = 5  # Russian ruble
    PLN = 6  # Polish złoty
    BRL = 7  # Brazilian real
    JPY = 8  # Japanese yen
    SEK = 9  # Swedish króna
    IDR = 10  # Indonesian rupiah
    MYR = 11  # Malaysian ringgit
    PHP = 12  # Philippine peso
    SGD = 13  # Singapore dollar
    THB = 14  # Thai baht
    VND = 15  # Vietnamese đồng
    KRW = 16  # South Korean won
    TRY = 17  # Turkish lira
    UAH = 18  # Ukrainian hryvnia
    MXN = 19  # Mexican peso
    CAD = 20  # Canadian dollar
    AUD = 21  # Australian dollar
    NZD = 22  # New Zealand dollar
    CNY = 23  # Renminbi
    INR = 24  # Indian rupee
    CLP = 25  # Chilean peso
    CUP = 26  # Cuban peso
    COP = 27  # Colombian peso
    ZAR = 28  # South African rand
    HKD = 29  # Hong Kong dollar
    TWD = 30  # New Taiwan dollar
    SAR = 31  # Saudi riyal
    AED = 32  # United Arab Emirates dirham
    # 33 - None
    ARS = 34  # Argentine peso
    ILS = 35  # Israeli new shekel
    # 36 - None
    KZT = 37  # Kazakhstani tenge
    KWD = 38  # Kuwaiti dinar
    QAR = 39  # Qatari riyal
    CRC = 40  # Costa Rican colon
    UYU = 41  # Uruguayan Peso
