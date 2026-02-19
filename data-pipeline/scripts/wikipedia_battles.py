"""
Wikipedia Civil War Battles Scraper
Utilities for extracting and processing battle data from Wikipedia's 
"List of American Civil War battles" page
"""
import requests
from bs4 import BeautifulSoup
import re 
from typing import List, Dict

""


def fetch_wikipedia_page(url: str = "https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles") -> str:
    """Fetches the HTML content of a Wikipedia page.
    
    Args:        
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page.
    """
    headers = {
        'User-Agent': 'CivilWarVisualizerBot/1.0 (contact: luccianobarberan@gmail.com)'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching Wikipedia page: {e}")
        raise

def parse_CWSAC_from_table(html: str) -> List[Dict[str, str]]:
    """Parses the HTML content to extract the CWSAC (Civil War Soldiers and Sailors) data from the table.
    
    Args:
        html (str): The HTML content of the Wikipedia page.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing battle data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    battle_data = []
    
    # Find all wikitables and get the one with CWSAC column
    tables = soup.find_all('table', {'class': 'wikitable'})
    table = None
    for t in tables:
        table_headers = [th.get_text(strip=True) for th in t.find_all('th')]
        if 'CWSAC' in table_headers:
            table = t
            break

    if not table:
        print("CWSAC table not found.")
        return battle_data
    
    # Extract headers to identify columns
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    
    # Iterate through table rows, skipping the header row
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        battle_info = {}
        if len(cells) < len(headers):
            continue  # Skip rows that don't have enough cells
        
        for header, cell in zip(headers, cells):
            battle_info[header] = cell.get_text(strip=True)
        
        battle_data.append(battle_info)
    
    return battle_data