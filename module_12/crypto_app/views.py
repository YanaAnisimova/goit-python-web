import aiohttp
import aiohttp_jinja2
import asyncio
import humanize

from settings import URL_BITCOIN_MYFIN, URL_ETHEREUM_MYFIN, URL_BITCOINCASH_MYFIN, \
    URL_BITCOIN_BITINFOCHARTS, URL_ETHEREUM_BITINFOCHARTS, URL_BITCOINCASH_BITINFOCHARTS, \
    URL_BITCOIN_BITSTAT, URL_ETHEREUM_BITSTAT, URL_BITCOINCASH_BITSTAT


@aiohttp_jinja2.template('crypto/index.html')
async def index(request):
    rates_myfin = await client_myfin(URL_BITCOIN_MYFIN, URL_ETHEREUM_MYFIN, URL_BITCOINCASH_MYFIN)
    rates_bitinfo = await client_bitinfo(URL_BITCOIN_BITINFOCHARTS, URL_ETHEREUM_BITINFOCHARTS, URL_BITCOINCASH_BITINFOCHARTS)
    rates_bitstat = await client_bitstat(URL_BITCOIN_BITSTAT, URL_ETHEREUM_BITSTAT, URL_BITCOINCASH_BITSTAT)

    print(rates_myfin)
    print(rates_bitinfo)
    print(rates_bitstat)

    return {
        'rates_myfin': rates_myfin,
        'rates_bitinfo': rates_bitinfo,
        'rates_bitstat': rates_bitstat
            }


#  myfin.by
async def parse_data_myfin(data):
    rate = data.split('"birzha_info_head_rates">')[1].split('$')[0].strip()
    print('a ------', float(rate))
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_myfin(session, url):
    async with session.get(url) as resp:
        print("Status:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_myfin(data)


async def client_myfin(url_bitcoin, url_ethereum, url_bitcoin_cash):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        bitcoin, ethereum, bitcoin_cash = await asyncio.gather(
            requests_course_myfin(session, url_bitcoin),
            requests_course_myfin(session, url_ethereum),
            requests_course_myfin(session, url_bitcoin_cash)
        )

        return {'bitcoin': bitcoin, 'ethereum': ethereum, 'bitcoin_cash': bitcoin_cash}


# bitinfocharts.com
async def parse_data_bitinfo(data):
    rate = data.split('"price"')[1].split('>')[1].split('<')[0].strip().replace(',', '')
    print('b ------', rate)
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitinfo(session, url):
    async with session.get(url) as resp:
        print("Status:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitinfo(data)


async def client_bitinfo(url_bitcoin, url_ethereum, url_bitcoin_cash):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        bitcoin, ethereum, bitcoin_cash = await asyncio.gather(
            requests_course_bitinfo(session, url_bitcoin),
            requests_course_bitinfo(session, url_ethereum),
            requests_course_bitinfo(session, url_bitcoin_cash)
        )

        return {'bitcoin': bitcoin, 'ethereum': ethereum, 'bitcoin_cash': bitcoin_cash}


# bitstat.top
async def parse_data_bitstat(data):
    rate = data.split('"ticker_usd">')[1].split('$')[0].replace(' ', '')
    print('c ------', rate)
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitstat(session, url):
    async with session.get(url) as resp:
        print("Status:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitstat(data)


async def client_bitstat(url_bitcoin, url_ethereum, url_bitcoin_cash):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        bitcoin, ethereum, bitcoin_cash = await asyncio.gather(
            requests_course_bitstat(session, url_bitcoin),
            requests_course_bitstat(session, url_ethereum),
            requests_course_bitstat(session, url_bitcoin_cash)
        )

        return {'bitcoin': bitcoin, 'ethereum': ethereum, 'bitcoin_cash': bitcoin_cash}
