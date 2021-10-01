import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, "templates")
STATIC_PATH = os.path.join(DIR_PATH, "static")
# SECRET_KEY = b"s}\x19\xf0\xa2\x0b\x86\x12\xb8\n'\xa38\x02Z\x1aB\x85>\xd6\x0b\x90%\x95\xe6\x7f\x17q\xa8\xd4^;"

# in real world applications DEBUG_APP should be default False
DEBUG = os.environ.get("DEBUG_APP", True)

# Resources
URL_BITCOIN_MYFIN = 'https://myfin.by/crypto-rates/bitcoin'
URL_ETHEREUM_MYFIN = 'https://myfin.by/crypto-rates/ethereum'
URL_BITCOINCASH_MYFIN = 'https://myfin.by/crypto-rates/bitcoincash'
URL_BITCOIN_BITINFOCHARTS = 'https://bitinfocharts.com/ru/bitcoin/'
URL_ETHEREUM_BITINFOCHARTS = 'https://bitinfocharts.com/ru/ethereum/'
URL_BITCOINCASH_BITINFOCHARTS = 'https://bitinfocharts.com/ru/bitcoin%20cash/'
URL_BITCOIN_BITSTAT = 'https://bitstat.top/coin.php?id_coin=1'
URL_ETHEREUM_BITSTAT = 'https://bitstat.top/coin.php?id_coin=2'
URL_BITCOINCASH_BITSTAT = 'https://bitstat.top/coin.php?id_coin=11'