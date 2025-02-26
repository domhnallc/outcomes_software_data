import csv
import pandas as pd
import requests
from urllib import parse
from requests.exceptions import ConnectionError, TooManyRedirects, ReadTimeout
import helper as hlp

"""
Reads in the URL list. Generates a csv file of URLs and their http code when 
attempts made to reach URL. Saves to ./responses.csv.
"""
input_data_folder = "./feb25_data"
output_results_folder = "./feb25_output"

url_input_csv = f"{input_data_folder}/gtr_raw_data_feb25.csv"


def main():
    # TODO: should this check for unique?
    # TODO: if not, maybe run an analysis of the num of duplicates and tld dupes
    df = get_df_from_csv(url_input_csv)
    url_list = get_urls(df)
    print(f"Analysing {len(url_list)} urls.")
    check_urls_for_http_response(url_list)
    categorise_urls(url_list)


def check_urls_for_http_response(url_list):
    responses = []
    counter = 0
    for url in url_list:
        counter = counter + 1
        if url == "missing":
            print("missing")
        else:
            print(f"[{counter}:{len(url_list)}]", url)
            response = check_url(url)
            print(response[0], response[1])
            responses.append(response)

    with open(f"{output_results_folder}/responses.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Url", "Response"])
        writer.writerows(responses)


def check_urls_for_2xx_responses():
    # redo this with only the 2xx responses
    df_only_http200s = get_df_from_csv(f"{output_results_folder}/responses.csv")
    print(df_only_http200s)
    df_only_http200s = df_only_http200s.loc[
        (df_only_http200s["response"] == "200")
        | (df_only_http200s["response"] == "202")
    ]
    print(df_only_http200s)
    # df.loc[df['column_name'] == some_value]

    url_list = df_only_http200s["url"]

    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open("cats_only_200.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def categorise_urls(url_list):
    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open(f"{output_results_folder}/categorized_urls.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def analyse_keywords_in_url(url: str):

    if url == "missing":
        return "missing"

    if not url == "missing" or not url == "None":
        if any([x in url for x in hlp.discipline_non_software_repo]):
            return "discipline-specific (non-software repo)"
        if any([x in url for x in hlp.uk_govt_software]):
            return "UK Govt Software Link"
        if any([x in url for x in hlp.non_software_website]):
            return "Non-software website"
        if any([x in url for x in hlp.unresponsive]):
            return "Non-responsive"
        if any([x in url for x in hlp.cloud_filestore]):
            return "Cloud filestore"
        if any([x in url for x in hlp.data_platform]):
            return "Data platform"
        if any([x in url for x in hlp.institutional]):
            return "institutional"
        if any([x in url for x in hlp.international_institutional]):
            return "international_institutional"
        if any([x in url for x in hlp.public_commercial_code_repo]):
            return "public_commercial_code_repo"
        if any([x in url for x in hlp.public_noncommercial_archive_repo]):
            return "public_noncommercial_archive_repo"
        if any([x in url for x in hlp.public_noncommercial_package_repo]):
            return "public_noncommercial_package_repo"
        if any([x in url for x in hlp.publisher]):
            return "publisher"
        if any([x in url for x in hlp.documentation_site]):
            return "documentation_site"
        if any([x in url for x in hlp.software_specific_website]):
            return "software_specific_website"
        if any([x in url for x in hlp.preprint_site]):
            return "preprint_site"
        if any([x in url for x in hlp.software_paper]):
            return "software_paper"
        if any([x in url for x in hlp.discipline_software_repo]):
            return "discipline_software_repo"
        if any([x in url for x in hlp.public_openscience_repo]):
            return "public openscience repo"
        if any([x in url for x in hlp.web_app_or_db]):
            return "web app"
        if any([x in url for x in hlp.patent]):
            return "patent"
        if any([x in url for x in hlp.project_or_consortium]):
            return "project or consortium"
        if any([x in url for x in hlp.video]):
            return "video"
        if any([x in url for x in hlp.social_media]):
            return "social media"
        if any([x in url for x in hlp.commercial_appstore]):
            return "commercial appstore"
        if any([x in url for x in hlp.non_commercial_appstore]):
            return "non-commercial appstore"
        if any([x in url for x in hlp.commercial_website]):
            return "commercial website"
        if any([x in url for x in hlp.forum_mailing_list_blog]):
            return "forum, mailinglist, blog"
        if any([x in url for x in hlp.conference_site]):
            return "conference site"
        if any([x in url for x in hlp.uk_public_govt_news]):
            return "UK Govt Public site"
        if any([x in url for x in hlp.internations_public_govt]):
            return "International public govt"
        if any([x in url for x in hlp.search_site]):
            return "search site"
        if any([x in url for x in hlp.personal_site]):
            return "personal website"
        if any([x in url for x in hlp.inappropriate]):
            return "inappropriate"
        if any([x in url for x in hlp.news_blog]):
            return "news_blog"
        if any([x in url for x in hlp.google_doc]):
            return "google_doc"
        if any([x in url for x in hlp.institutional_group]):
            return "institutional_group"
        if any([x in url for x in hlp.commercial_workspace_wiki]):
            return "commercial_workspace_wiki"

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

    # changed from get to head to see if speeds up
    try:
        r = requests.head(
            url, headers=headers, timeout=10, stream=True
        )  # set stream to True to avoid automatic decompression
        return url, r.status_code

    except ConnectionError:
        return url, "ConnectionError"
    except TooManyRedirects:
        return url, "TooManyRedirectsError"
    except ReadTimeout:
        return url, "ReadTimeoutError"
    except UnicodeDecodeError:
        return url, "DecodeError"
    except requests.exceptions.RequestException:
        return url, "DecompressionError"


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
