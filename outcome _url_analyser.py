import csv
import pandas as pd
import requests
from urllib import parse
from requests.exceptions import ConnectionError, TooManyRedirects, ReadTimeout

"""
Reads in the URL list. Generates a csv file of URLs and their http code when 
attempts made to reach URL. Saves to ./responses.csv.
"""


def main():
    """"""
    df = get_df_from_csv("outcomes_software_urls.csv")
    url_list = get_urls(df)

    """
    for url in url_list:
        if url == "missing":
            print("missing")
        else:
            response = check_url(url)
            print(response[0], response[1])
            responses.append(response)
    with open("responses.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(responses)
    """

    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open("cats.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def analyse_keywords_in_url(url: str):
    institutional = [".ac.uk"]
    international_institutional = [".edu", "http://fair.dei.unipd.it"]
    public_commercial_code_repo = ["github", "bitbucket", "sourceforge", "gitlab"]
    public_noncommercial_archive_repo = ["zenodo", "figshare"]
    public_noncommercial_package_repo = ["r-project", "mathworks"]
    publisher = [
        "sciencedirect",
        "researchgate",
        "thelancet",
        "tandfonline",
        "dx.doi.org/10",
        "wiley.com",
        "pubs.acs.org",
        "nature.com",
    ]
    documentation_site = ["readthedocs"]
    software_specific_website = ["jalview"]
    preprint_site = ["arxiv"]
    software_paper = ["joss.theoj.org"]
    discipline_software_repo = ["https://www.bioconductor.org"]

    unknowns = 0
    if not url == "missing":
        if any([x in url for x in institutional]):
            return "institutional"
        if any([x in url for x in international_institutional]):
            return "international_institutional"
        if any([x in url for x in public_commercial_code_repo]):
            return "public_commercial_code_repo"
        if any([x in url for x in public_noncommercial_archive_repo]):
            return "public_noncommercial_archive_repo"
        if any([x in url for x in public_noncommercial_package_repo]):
            return "public_noncommercial_package_repo"
        if any([x in url for x in publisher]):
            return "publisher"
        if any([x in url for x in documentation_site]):
            return "documentation_site"
        if any([x in url for x in software_specific_website]):
            return "software_specific_website"
        if any([x in url for x in preprint_site]):
            return "preprint_site"
        if any([x in url for x in software_paper]):
            return "software_paper"
        if any([x in url for x in discipline_software_repo]):
            return "discipline_software_repo"

        else:
            return "unknown"


def get_df_from_csv(csv_to_read: str) -> pd.DataFrame:
    """Returns dataframe from a csv

    Args:
        csv_to_read (str): filepath of csv

    Returns:
        Dataframe: df
    """
    with open(csv_to_read) as data_in:
        df = pd.read_csv(data_in).fillna("missing")

    return df


def get_urls(df_in: pd.DataFrame) -> list:
    urls_list = []
    for url in df_in.Url:
        urls_list.append(url)

    return urls_list


def check_url(url: str):

    
    hostname = get_hostname_from_url(url)
    headers = {
        "Host": hostname,
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Referer": hostname,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        return url, r.status_code

    except ConnectionError:
        return url, "ConnectionError"
    except TooManyRedirects:
        return url, "TooManyRedirectsError"
    except ReadTimeout:
        return url, "ReadTimeoutError"


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
        hostname = "error"
    return hostname


if __name__ == "__main__":
    main()
