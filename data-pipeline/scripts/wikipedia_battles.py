"""
Wikipedia Civil War Battles Scraper Functions
Utilities for extracting and processing battle data from Wikipedia's 
"List of American Civil War battles" page
"""
import requests
from bs4 import BeautifulSoup
import re 
from typing import List, Dict
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        logger.error(f"Error fetching Wikipedia page: {e}")
        raise

def parse_CWSAC_from_table(html: str) -> List[Dict[str, str]]:
    """Parses the HTML content to extract the CWSAC battle data from the table.
    
    Args:
        html (str): The HTML content of the Wikipedia page.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing battle data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    battle_data = []
    
    # Find all wikitables and get the one with CWSAC column
    tables = soup.find_all('table', {'class': 'wikitable'})
    logger.debug(f"Found {len(tables)} wikitables on the page.")
    
    table = None
    for t in tables:
        table_headers = [th.get_text(strip=True) for th in t.find_all('th')]
        logger.debug(f"Checking table with headers: {table_headers}")
        if 'CWSAC' in table_headers:
            table = t
            logger.debug("CWSAC table found.")
            break

    if not table:
        logger.warning("CWSAC table not found.")
        return battle_data
    
    # Extract headers, filtering out parent headers (those with colspan)
    headers = [th.get_text(strip=True) for th in table.find_all('th') if not th.get('colspan')]

    logger.debug(f"Extracted headers (filtered): {headers}")

    if not headers:
        logger.warning("No headers found in CWSAC table.")
        return battle_data

    # Iterate through table rows
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        battle_info = {}
        if len(cells) < len(headers):
            logger.warning(f"Skipping row with {len(cells)} cells, expected {len(headers)}")
            continue
        
        for header, cell in zip(headers, cells):
            battle_info[header] = cell.get_text(strip=True)
        
        battle_data.append(battle_info)
    
    logger.info(f"Successfully parsed {len(battle_data)} battles from table")
    return battle_data

def clean_battle_data(battles: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Clean battle data by removing footnotes and normalizing whitespace.
    
    Args:
        battles: List of battle dictionaries with raw data
        
    Returns:
        List of battle dictionaries with cleaned data
    """
    cleaned = []
    for battle in battles:
        cleaned_battle = {}
        for key, value in battle.items():
            # Remove footnote brackets
            cleaned_value = re.sub(r'\[.*?\]', '', value)
            # Replace en-dashes and other dashes with hyphen
            cleaned_value = re.sub(r'–|—', '-', cleaned_value)
            # Normalize whitespace
            cleaned_value = re.sub(r'\s+', ' ', cleaned_value).strip()
            cleaned_battle[key] = cleaned_value
        cleaned.append(cleaned_battle)
    return cleaned

def filter_by_class(battles: List[Dict[str, str]], class_filter: List[str] = ['A','B']) -> List[Dict[str, str]]:
    """Filters battles by their CWSAC class.
    
    Args:
        battles (List[Dict[str, str]]): The list of battle data dictionaries.
        class_filter (List[str]): The list of CWSAC classes to include (e.g., ['A', 'B']).

    Returns:
        List[Dict[str, str]]: A filtered list of battle data dictionaries.
    """
    return [battle for battle in battles if battle.get('CWSAC') in class_filter]