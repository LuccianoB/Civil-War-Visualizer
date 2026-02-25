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
import urllib.parse
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
            #extract links if present
            if header == 'Battle':
                link = cell.find('a')
                if link and link.get('href', '').startswith('/wiki/'):
                    article_title = link.get('href')[len('/wiki/'):]
                    battle_info['Wikipedia_Link'] = article_title
                else:
                    #Fallback: use battle name as link title (not ideal but better than nothing)
                    battle_info['Wikipedia_Link'] = battle_info[header].replace(' ', '_')
        
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

def parse_date_range(date_str: str) -> Dict[str, str]:
    """Parse a Wikipedia date string into structured start_date and end_date.
    
    Handles formats like:
      - "July 11, 1861"                        (single day)
      - "April 12-13, 1861"                     (same month range)
      - "April 25- May 1, 1862"                 (cross-month, same year)
      - "December 31, 1862-January 2, 1863"     (cross-month, cross-year)
    
    Args:
        date_str: Raw date string from Wikipedia
        
    Returns:
        Dict with 'start_date' and 'end_date' in YYYY-MM-DD format,
        or both None if parsing fails.
    """
    from datetime import datetime

    MONTHS = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    try:
        # Normalize dashes and whitespace
        cleaned = re.sub(r'\s*-\s*', '-', date_str.strip())

        # Pattern 1: Cross-month (possibly cross-year)
        #   e.g. "April 25-May 1, 1862" or "December 31, 1862-January 2, 1863"
        cross_month = re.match(
            r'(\w+)\s+(\d+),?\s*(\d{4})?-?(\w+)\s+(\d+),\s*(\d{4})',
            cleaned
        )
        if cross_month:
            m1, d1, y1, m2, d2, y2 = cross_month.groups()
            # If the first year is missing, it's the same year as the second
            y1 = y1 if y1 else y2
            start = datetime(int(y1), MONTHS[m1], int(d1))
            end   = datetime(int(y2), MONTHS[m2], int(d2))
            return {
                'start_date': start.strftime('%Y-%m-%d'),
                'end_date':   end.strftime('%Y-%m-%d')
            }

        # Pattern 2: Same-month range  e.g. "April 12-13, 1861"
        same_month = re.match(r'(\w+)\s+(\d+)-(\d+),\s*(\d{4})', cleaned)
        if same_month:
            month, d1, d2, year = same_month.groups()
            start = datetime(int(year), MONTHS[month], int(d1))
            end   = datetime(int(year), MONTHS[month], int(d2))
            return {
                'start_date': start.strftime('%Y-%m-%d'),
                'end_date':   end.strftime('%Y-%m-%d')
            }

        # Pattern 3: Single day  e.g. "July 11, 1861"
        single_day = re.match(r'(\w+)\s+(\d+),\s*(\d{4})', cleaned)
        if single_day:
            month, day, year = single_day.groups()
            dt = datetime(int(year), MONTHS[month], int(day))
            formatted = dt.strftime('%Y-%m-%d')
            return {'start_date': formatted, 'end_date': formatted}

        logger.warning(f"Could not parse date: '{date_str}'")
        return {'start_date': None, 'end_date': None}

    except Exception as e:
        logger.warning(f"Error parsing date '{date_str}': {e}")
        return {'start_date': None, 'end_date': None}


def filter_by_class(battles: List[Dict[str, str]], class_filter: List[str] = ['A','B']) -> List[Dict[str, str]]:
    """Filters battles by their CWSAC class.
    
    Args:
        battles (List[Dict[str, str]]): The list of battle data dictionaries.
        class_filter (List[str]): The list of CWSAC classes to include (e.g., ['A', 'B']).

    Returns:
        List[Dict[str, str]]: A filtered list of battle data dictionaries.
    """
    return [battle for battle in battles if battle.get('CWSAC') in class_filter]