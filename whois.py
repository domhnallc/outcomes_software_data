import whois
import datetime
from urllib.parse import urlparse

# Input and output file paths
input_file = "/home/domhnall/Dev/outcomes_software_data/feb25_output/rerun/http_error_urls_for_whois.txt"
output_file = "/home/domhnall/Dev/outcomes_software_data/feb25_output/rerun/whois_expiration_dates_all_error_urls.txt"


def read_url_file():
    # Read URLs from the input file
    with open(input_file, "r") as file:
        urls = list(set(file.readlines()))
    return urls


def check_url_whois():
    # Open the output file for writing
    with open(output_file, "w") as file:
        urls = read_url_file()
        for url in urls:
            url = url.strip()  # Remove any leading/trailing whitespace
            url = urlparse(url).netloc  # Extract the domain name
            if not url:
                continue  # Skip empty lines
            try:
                # Perform WHOIS lookup
                whois_data = whois.whois(url)
                expiration_date = whois_data.expiration_date.date()
                # Write the URL and expiration date to the output file
                file.write(f"{url},{expiration_date}\n")
            except Exception as e:
                # Handle errors and log them
                file.write(f"{url},Error\n")
            print(f"Processed {url}: {expiration_date}")


if __name__ == "__main__":
    check_url_whois()
    print("WHOIS data extraction completed.")
