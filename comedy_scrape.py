import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from unidecode import unidecode
from urllib.error import HTTPError, URLError

RUTA = 'C:/Users/Vercetto/comedia_chile/'

# Function to read lists from files
def read_list(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Fetch lists
def get_locations(): return read_list(os.path.join(RUTA + "/Input/Locations.txt"))
def get_artists(): return read_list(os.path.join(RUTA + "/Input/Artists.txt"))
def get_dates(): return read_list(os.path.join(RUTA + "/Input/Dates.txt"))
def get_times(): return read_list(os.path.join(RUTA + "/Input/Times.txt"))
def get_URLs(): return read_list(os.path.join(RUTA + "/Output/URLs.txt"))

# Fetch web page content
def get_web_page(URL):
    try:
        response = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(response).read()
        return BeautifulSoup(webpage, 'html.parser')
    except (HTTPError, URLError) as e:
        print(f"Error fetching {URL}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error with {URL}: {e}")
        return None

# Scrape data from web page
def scrape_web_page(URL, web_page, artists, locations, dates, times):
    titulo = unidecode(web_page.title.get_text().lower())

    # Extract data using search lists
    result = {
        'url': URL,
        'artist': next((x.strip() for x in artists if x in titulo), ''),
        'location': next((x.strip() for x in locations if x in titulo), ''),
        'date': next((x.strip() for x in dates if x in titulo), ''),
        'time': next((x.strip() for x in times if x in titulo), '')
    }
    return result

# Main scraping workflow
def main():
    # Fetch input data
    artists = get_artists()
    locations = get_locations()
    dates = get_dates()
    times = get_times()
    URLs = list(dict.fromkeys(get_URLs()))  # Remove duplicates

    shows = []

    # Scrape each URL
    for URL in URLs:
        if URL:
            web_page = get_web_page(URL)
            if web_page:
                show_data = scrape_web_page(URL, web_page, artists, locations, dates, times)
                shows.append(show_data)

    # Save results to Excel
    df_shows = pd.DataFrame(shows)
    output_path = os.path.join(RUTA, '/Output/shows.xlsx')
    df_shows.to_excel(output_path, sheet_name='data', index=False)
    print(f"Data saved to {output_path}")

# Run script
if __name__ == "__main__":
    main()