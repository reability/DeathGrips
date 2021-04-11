import asyncio
import json
import requests
from bs4 import BeautifulSoup

from datetime import datetime as dt

# MARK: - Constants

URL = "https://www.avito.ru/moskva?q=ps4"
GATEWAY = "http://134.209.248.84:8000/item"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
CASHE = []
# MARK: - Main

async def main():
    print("Main task has started")
    task = asyncio.Task(job())


async def job():
    while True:
        print("new job")
        r = await request_task()
        #await asyncio.sleep(3)
        r2 = requests.post(GATEWAY, json=r)
        if r2.status_code == requests.codes.ok :
            print(1/0)
        else:
            print(r2.text) 
            1/0
        print("")

        print(r)

async def request_task():
    url = URL
    result = await make_request(url)
    if result.status_code ==  requests.codes.ok:
        print("response status - OK")
        data = await parse(result.text)
        return data
    else:
        print("response status - NOT OK")
        print(result.text)
        raise result.raise_for_status()

async def parse(text: str):
    soup = BeautifulSoup(text, 'lxml-xml')

    ads_data_string = soup.find('div', {'class': 'js-initial'}).get('data-state')
    ads_data_string = ads_data_string.replace('&quot', '"').replace(";","").replace(r"\\", "")

    ads_data_dict = json.loads(ads_data_string)

    items = []
    for item in ads_data_dict.get('catalog').get('items'):

        item_id = item.get('id')
        if item_id is None:
            continue

        if item_id in CASHE:
            continue

        short_url = item.get('urlPath')
        url_path = ""
        if short_url is not None:
            url_path = 'https://www.avito.ru' + short_url
        else:
            url_path = None

        raw_date = item.get('iva')
        if raw_date is not None:
            try:
                item_date = raw_date.get('DateInfoStep')[0].get('payload').get('absolute')
            except:
                print("Starnge case 1")
                item_date = None
        else:
            item_date = None

        filtered = {
            "id": item_id,
            "title": item.get('title'),
            "date_str": item_date,
            "url_path": url_path,
        }
        items.append(filtered)

    return items

async def make_request(url):
    print(current_time() + " request")
    session_resp = requests.Session()
    result = session_resp.get(url, headers=HEADERS)
    if result is None:
        result = session_resp.get(url, headers=headers, cookies=result.cookies)
    print(result.cookies)
    #a = 1/0
    return result

# MARK: - Utilities

def current_time():
    now = dt.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    print("Application has started")
    loop = asyncio.new_event_loop()
    #loop = asyncio.current_task()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Application has been terminated")
