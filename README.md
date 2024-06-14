proxy_auth = aiohttp.BasicAuth('proxy_username', 'proxy_password')

async with aiohttp.ClientSession(proxy=proxy, proxy_auth=proxy_auth) as session:
    mm = MonarchMoney(session=session)
    await mm.interactive_login()
    # Fetching accounts data
    accounts = await mm.get_accounts()
    print(accounts)

import ssl

# To disable SSL verification (not recommended)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async with aiohttp.ClientSession(proxy=proxy, ssl=ssl_context) as session:
    mm = MonarchMoney(session=session)
    await mm.interactive_login()
    # Fetching accounts data
    accounts = await mm.get_accounts()
    print(accounts)
