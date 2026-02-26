"""
Wikidata Query Functions for Civil War Battle Enrichment
Handles SPARQL queries to Wikidata API with error handling and retry logic.
"""

import re
import requests
import json
import time
import logging
import urllib.parse
from typing import Dict, List, Optional

# Configure logging

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


# Keywords for filtering Wikidata search results
_BAD_KEYWORDS = ['order of battle', 'disambiguation', 'wikimedia', 'print', 'given name', 'family name', 'female given name', 'male given name', 'video game', 'war-game', 'war game', 'politician', 'painter']
_GOOD_KEYWORDS = ['battle', 'siege', 'civil war', 'military engagement', 'military operation', 'military campaign', 'skirmish', 'raid', 'american civil war', 'engagement', 'bombardment']

# Common abbreviation map for Civil War battle names
_ABBREV_MAP = {
    'Ft.': 'Fort',
    'Mt.': 'Mount',
    'St.': 'Saint',
    'Pt.': 'Point',
    'Is.': 'Island',
    'Ops.': 'Operations'
}
_ABBREV_PATTERN = r'\b(' + '|'.join(re.escape(k) for k in _ABBREV_MAP.keys()) + r')(?=\b|$)'

def _expand_abbreviations(text: str) -> str:
    """Expand common abbreviations in a battle name string."""
    return re.sub(_ABBREV_PATTERN, lambda m: _ABBREV_MAP.get(m.group(0), m.group(0)), text)


def _build_search_candidates(battle_name: str) -> List[str]:
    """Generate cleaned search candidates from a Wikipedia battle name.
    
    Handles Wikipedia formatting quirks:
      - Concatenated 'or': "Bull Runor First Manassas" → "Bull Run"
      - Parenthetical alternates: "Monocacy(Battle of Monocacy Junction)"
      - Year disambiguation: "Franklin (1864)" → "Franklin"
      - Internal capitals: "DeRussy" → "De Russy"
      - Strips parenthetical text for a cleaner name: "Battle of Franklin (1864)" → "Battle of Franklin"
      - Expands abreviations: "Ft. Sumter" → "Fort Sumter"
      - Removes leading 'Battle of', 'Siege of', etc. for a more concise search term: "Battle of Gettysburg" → "Gettysburg"
      - Removes possessives for a more general search term: "Battle of Sailor's Creek" → "Battle of Sailors Creek"
    """
    candidates = []

    # Strategy 1: Split on concatenated "or" + capital letter
    # e.g. "First Battle of Bull Runor First Manassas" → "First Battle of Bull Run"
    # Negative lookbehind avoids matching "(or " inside parentheses
    or_match = re.match(r'(.+?)(?<!\()or ([A-Z].+)', battle_name)
    if or_match:
        candidates.append(or_match.group(1).strip())

    # Strategy 2: Strip all parenthetical text
    # e.g. "Battle of Franklin (1864)" → "Battle of Franklin"
    stripped = re.sub(r'\s*\(.*?\)', '', battle_name).strip()
    if stripped and stripped != battle_name:
        candidates.append(stripped)

    # Strategy 3: Try alternate names from inside parentheses
    # e.g. "(Battle of Monocacy Junction)" → "Battle of Monocacy Junction"
    for content in re.findall(r'\(([^)]+)\)', battle_name):
        # Skip pure years like "(1864)"
        if re.match(r'^\d{4}$', content.strip()):
            continue
        # Strip leading "or ": "(or Sailor's Creek)" → "Sailor's Creek"
        alt = re.sub(r'^or\s+', '', content.strip())
        if alt:
            candidates.append(alt)

    # Strategy 4:Add variation with spaces before internal capitals (e.g., DeRussy -> De Russy)
    spaced_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', battle_name)
    if spaced_name != battle_name and spaced_name not in candidates:
        candidates.append(spaced_name)

    # Strategy 5: Expand common abbreviations (e.g., Ft. → Fort) for all candidates
    expanded_candidates = []
    for candidate in [battle_name] + candidates:
        expanded = _expand_abbreviations(candidate)
        if expanded != candidate and expanded not in candidates and expanded not in expanded_candidates:
            expanded_candidates.append(expanded)
    candidates.extend(expanded_candidates)

    # Strategy 6: For every candidate, add a version with all apostrophes removed (e.g., Brice's → Brices)
    apostrophe_variants = []
    for candidate in candidates[:]:
        no_apostrophes = candidate.replace("'", "")
        if no_apostrophes != candidate and no_apostrophes not in candidates and no_apostrophes not in apostrophe_variants:
            apostrophe_variants.append(no_apostrophes)
    candidates.extend(apostrophe_variants)

    # Apply same spacing fix to all existing candidates
    new_candidates = []
    for candidate in candidates[:]:
        spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', candidate)
        if spaced != candidate and spaced not in candidates and spaced not in new_candidates:
            new_candidates.append(spaced)
    candidates.extend(new_candidates)

    # Strategy 7: Raw name as fallback
    candidates.append(battle_name)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def _pick_best_result(results: list) -> Optional[str]:
    """Pick the best Wikidata entity from search results.
    
    Only accepts results whose description indicates an actual battle/military event;
    skips 'order of battle', disambiguation pages, given names, video games, etc.
    """
    # Only accept results with good description keywords and no bad ones
    for r in results:
        desc = r.get('description', '').lower()
        if any(bad in desc for bad in _BAD_KEYWORDS):
            continue
        if any(good in desc for good in _GOOD_KEYWORDS):
            return r.get('id')

    return None

def _lookup_by_sitelink(article_title: str) -> Optional[str]:
    """Lookup a battle's Q-ID by its Wikipedia sitelink.
    
    This is a fallback method when the search API doesn't yield good results.
    It checks if there's a Wikidata item with a sitelink to the given Wikipedia page.
    
    Args:
        article_title: The Wikipedia article title (e.g., "Battle of Fort Sumter")
        
    Returns:
        The Q-ID (e.g., "Q543165") or None if not found
    """
    
    try:
        time.sleep(QUERY_DELAY)  # Respectful delay before API call
        sitelink_search_url = "https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbgetentities',
            'sites': 'enwiki',
            'titles': article_title,
            'format': 'json'
        }

        response = requests.get(sitelink_search_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        entities = data.get('entities', {})
        for qid, entity in entities.items():
            if qid.startswith('Q') and 'missing' not in entity:  # Entity exists
                logger.info(f"Found Q-ID by sitelink for '{article_title}': {qid}")
                return qid
            else:
                logger.debug(f"No Wikidata item with sitelink for '{article_title}'")
        return None
    except Exception as e:
        logger.error(f"Error during sitelink lookup for '{article_title}': {e}")
        return None


def _try_sitelink_candidates(sitelink_candidates: List[str], tried_titles: set) -> Optional[str]:
    """Try sitelink lookup for each candidate, converting spaces to underscores.
    
    Args:
        sitelink_candidates: List of battle name candidates to try
        tried_titles: Set of titles already attempted (to avoid duplicates)
        
    Returns:
        The Q-ID if found, or None if no match
    """
    for candidate in sitelink_candidates:
        candidate_title = candidate.replace(' ', '_')
        candidate_title = urllib.parse.unquote(candidate_title)
        if candidate_title in tried_titles:
            continue
        tried_titles.add(candidate_title)
        print(f"[DEBUG] Trying sitelink lookup for candidate title: '{candidate_title}'")
        logger.debug(f"Trying sitelink lookup for candidate title '{candidate_title}' as fallback")
        qid = _lookup_by_sitelink(candidate_title)
        if qid:
            return qid
    return None



def find_battle_qid(battle_name: str, wikipedia_article: Optional[str] = None) -> Optional[str]:
    """
    Find a battle's Wikidata Q-ID by its name using search API.
    
    Generates multiple search candidates to handle Wikipedia formatting
    quirks (concatenated alternate names, parenthetical text), and filters
    results to prefer actual battle entities.
    
    Args:
        battle_name: The name of the battle (e.g., "Battle of Fort Sumter")
        wikipedia_article: Optional Wikipedia article title to use for sitelink lookup fallback
        
    Returns:
        The Q-ID (e.g., "Q543165") or None if not found
    """
    candidates = _build_search_candidates(battle_name)
    logger.debug(f"Search candidates for '{battle_name}': {candidates}")

    print(f"[DEBUG] Candidates for '{battle_name}': {candidates}")

    for candidate in candidates:
        print(f"[DEBUG] Trying name candidate: '{candidate}'")
        try:
            time.sleep(QUERY_DELAY)

            search_url = "https://www.wikidata.org/w/api.php"
            params = {
                'action': 'wbsearchentities',
                'search': candidate,
                'language': 'en',
                'format': 'json',
                'limit': 5
            }

            response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get('search', [])

            if not results:
                logger.debug(f"No results for candidate: '{candidate}'")
                continue

            # Pick the best result (prefer actual battle entities)
            qid = _pick_best_result(results)
            if qid:
                logger.info(f"Found Q-ID for '{battle_name}': {qid}")
                return qid

        except Exception as e:
            logger.error(f"Error searching for '{candidate}': {e}")
            continue

    # Enhanced fallback: try sitelink lookup for scraped article title and all candidates
    tried_titles = set()
    # Try the scraped article title first (if present)
    if wikipedia_article:
        tried_titles.add(wikipedia_article)
        print(f"[DEBUG] Trying sitelink lookup for scraped article title: '{wikipedia_article}'")
        logger.debug(f"Trying sitelink lookup for scraped article title '{wikipedia_article}' as fallback")
        qid = _lookup_by_sitelink(wikipedia_article)
        if qid:
            return qid
    
    # Build sitelink candidates: base candidates + stripped-leading variants + abbreviation expansions
    sitelink_candidates = list(candidates)
    stripped_leading = re.sub(r'^(Battle|Siege|Skirmish|Engagement|Action|Raid|Capture|Occupation|Bombardment|Attack|Defense|Expedition|Affair|Operations|Campaign) of ', '', battle_name, flags=re.IGNORECASE)
    if stripped_leading != battle_name and stripped_leading not in sitelink_candidates:
        sitelink_candidates.append(stripped_leading)
        # Expand abbreviations only on the newly generated candidate (e.g., "Manassas Station Ops." → "Manassas Station Operations")
        expanded = _expand_abbreviations(stripped_leading)
        if expanded != stripped_leading and expanded not in sitelink_candidates:
            sitelink_candidates.append(expanded)
    
    # Try all sitelink candidates
    qid = _try_sitelink_candidates(sitelink_candidates, tried_titles)
    if qid:
        return qid
    logger.warning(f"Battle not found on Wikidata: {battle_name}")
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