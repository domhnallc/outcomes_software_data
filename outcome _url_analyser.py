import csv
import pandas as pd
import requests
from urllib import parse
from requests.exceptions import ConnectionError, TooManyRedirects, ReadTimeout


def main():

    df = get_df_from_csv("outcomes_software_urls.csv")

    url_list = get_urls(df)

    print(url_list)

    responses = []

    for url in url_list:
        if url == 'missing':
            print('missing')
        else:
            response = check_url(url)
            print(response[0], response[1])
            responses.append(response)
    with open('responses.csv','w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(responses)
        


def get_df_from_csv(csv_to_read: str) -> pd.DataFrame:

    with open(csv_to_read) as data_in:
        df = pd.read_csv(data_in).fillna('missing')

    return df


def get_urls(df_in:pd.DataFrame) -> list:

    urls_list = []
    for url in df_in.Url:
        urls_list.append(url)

    return urls_list
    

def check_url(url: str):

    hostname = get_hostname_from_url(url)
    headers = {
        'Host': hostname,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': hostname,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin'
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        return url, r.status_code

    except ConnectionError:
        return url,'ConnectionError'
    except TooManyRedirects:
        return url,'TooManyRedirectsError'
    except ReadTimeout:
        return url,'ReadTimeoutError'

def get_hostname_from_url(url: str) -> str:
    """Returns hostname from a url e.g pure.qub.ac.uk

    Args:
        url (str): url to break down

    Returns:
        str: hostname
    """
    try:
        hostname = parse.urlsplit(url).hostname
    except AttributeError:
        hostname = 'error'
    return hostname

if __name__ == '__main__':
    main()