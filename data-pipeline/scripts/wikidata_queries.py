"""
Wikidata Query Functions for Civil War Battle Enrichment
Handles SPARQL queries to Wikidata API with error handling and retry logic.
"""

import requests
import json
import time
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Wikidata SPARQL endpoint
WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"

# Request headers (respectful bot identification)
HEADERS = {
    'User-Agent': 'Civil War Visualizer Bot v1.0',
    'Accept': 'application/sparql-results+json'
}

# Retry settings
MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds
QUERY_DELAY = 0.5  # seconds between queries


def query_wikidata_sparql(sparql_query: str) -> Optional[Dict]:
    """
    Execute a SPARQL query against Wikidata API with retry logic.
    
    Args:
        sparql_query: The SPARQL query string
        
    Returns:
        Dict with query results, or None if query fails after retries
        
    Raises:
        Logs errors but doesn't raise exceptions (graceful failure)
    """
    retries = 0
    backoff = INITIAL_BACKOFF
    
    while retries < MAX_RETRIES:
        try:
            # Add delay between queries (respectful to API)
            time.sleep(QUERY_DELAY)
            
            # Make the request
            response = requests.get(
                WIKIDATA_SPARQL_URL,
                params={'query': sparql_query},
                headers=HEADERS,
                timeout=10
            )
            
            # Handle rate limiting (429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', backoff))
                logger.warning(f"Rate limited by Wikidata. Waiting {retry_after}s...")
                time.sleep(retry_after)
                retries += 1
                backoff *= 2
                continue
            
            # Raise for other HTTP errors
            response.raise_for_status()
            
            # Parse and return results
            data = response.json()
            logger.debug(f"Query successful. Found {len(data.get('results', {}).get('bindings', []))} results")
            return data
            
        except requests.exceptions.Timeout:
            retries += 1
            logger.warning(f"Query timeout. Retry {retries}/{MAX_RETRIES}. Waiting {backoff}s...")
            time.sleep(backoff)
            backoff *= 2
            
        except requests.exceptions.RequestException as e:
            retries += 1
            logger.error(f"Request error: {e}. Retry {retries}/{MAX_RETRIES}. Waiting {backoff}s...")
            time.sleep(backoff)
            backoff *= 2
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
    
    logger.error(f"Query failed after {MAX_RETRIES} retries")
    return None


def find_battle_qid(battle_name: str) -> Optional[str]:
    """
    Find a battle's Wikidata Q-ID by its name using search API.
    
    Args:
        battle_name: The name of the battle (e.g., "Battle of Fort Sumter")
        
    Returns:
        The Q-ID (e.g., "Q543165") or None if not found
    """
    logger.debug(f"Searching for battle: {battle_name}")
    
    try:
        # Use Wikidata search API instead of SPARQL
        search_url = "https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbsearchentities',
            'search': battle_name,
            'language': 'en',
            'format': 'json'
        }
        
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = data.get('search', [])
        
        if not results:
            logger.warning(f"Battle not found on Wikidata: {battle_name}")
            return None
        
        # Return the first result's Q-ID
        qid = results[0].get('id')
        logger.info(f"Found Q-ID for '{battle_name}': {qid}")
        return qid
        
    except Exception as e:
        logger.error(f"Error searching for battle: {e}")
        return None

def get_battle_data(qid: str) -> Dict:
    """
    Get battle coordinates from Wikidata using its Q-ID.
    
    Args:
        qid: The Wikidata Q-ID (e.g., "Q543165")
        
    Returns:
        Dict with key: 'coordinates' (value may be None if not found)
    """
    # Build the SPARQL query (coordinates only — dates parsed from Wikipedia)
    sparql_query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    
    SELECT ?coords WHERE {{
      OPTIONAL {{ wd:{qid} wdt:P625 ?coords }}
    }}
    """
    
    logger.debug(f"Fetching data for Q-ID: {qid}")
    
    # Execute query
    response = query_wikidata_sparql(sparql_query)
    
    if not response:
        logger.warning(f"No response from Wikidata for Q-ID: {qid}")
        return {'coordinates': None}
    
    # Extract data from response
    bindings = response.get('results', {}).get('bindings', [])
    
    if not bindings:
        logger.debug(f"No data found for Q-ID {qid} (battle may lack coordinates)")
        return {'coordinates': None}
    
    # Get the first result
    result = bindings[0]
    
    # Extract coordinates
    coordinates = result.get('coords', {}).get('value', None)
    
    logger.debug(f"Retrieved data for {qid}: coords={bool(coordinates)}")
    
    return {
        'coordinates': coordinates
    }

def enrich_battle(battle: Dict, qid: str, wikidata_data: Dict) -> Dict:
    """
    Combine baseline battle data with Wikidata enrichment.
    
    Args:
        battle: The baseline battle dict from baseline_battles.json
        qid: The Wikidata Q-ID for the battle
        wikidata_data: Dict with 'coordinates' from Wikidata
        
    Returns:
        Enriched battle dict with Wikidata fields added
    """
    # Start with a copy of the baseline battle
    enriched = battle.copy()
    
    # Add Wikidata Q-ID
    enriched['qid'] = qid
    
    # Add coordinates (only if not None)
    if wikidata_data.get('coordinates'):
        enriched['wikidata_coordinates'] = wikidata_data['coordinates']
    
    # Data is complete when we have coordinates (dates come from Wikipedia)
    enriched['data_complete'] = bool(wikidata_data.get('coordinates'))
    enriched['data_source'] = 'wikipedia_and_wikidata'
    
    logger.debug(f"Enriched battle '{battle.get('Battle', 'Unknown')}' with Q-ID {qid}")
    
    return enriched