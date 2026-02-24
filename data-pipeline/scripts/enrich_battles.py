"""
Script to enrich baseline battle data with Wikidata information.
Reads baseline_battles.json, queries Wikidata for each battle's Q-ID and data,
and saves enriched data to enriched_battles.json.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict

import wikidata_queries

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
SCRIPT_DIR = Path(__file__).parent.parent
INPUT_FILE = SCRIPT_DIR / 'raw_data' / 'baseline_battles.json'
OUTPUT_FILE = SCRIPT_DIR / 'processed_data' / 'enriched_battles.json'
LOG_FILE = SCRIPT_DIR / 'logs' / 'step1b_errors.log'


def setup_directories():
    """Create necessary directories if they don't exist."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Directories ready: {OUTPUT_FILE.parent}, {LOG_FILE.parent}")


def load_baseline_battles() -> List[Dict]:
    """
    Load baseline battles from JSON file.
    
    Returns:
        List of battle dictionaries
    """
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return []
    
    try:
        with open(INPUT_FILE, 'r') as f:
            battles = json.load(f)
        logger.info(f"Loaded {len(battles)} baseline battles from {INPUT_FILE}")
        return battles
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from {INPUT_FILE}: {e}")
        return []


def enrich_all_battles(battles: List[Dict]) -> List[Dict]:
    """
    Enrich all battles with Wikidata data.
    
    Args:
        battles: List of baseline battle dictionaries
        
    Returns:
        List of enriched battle dictionaries
    """
    enriched_battles = []
    total = len(battles)
    
    for i, battle in enumerate(battles, 1):
        battle_name = battle.get('Battle', 'Unknown')
        wikipedia_article = battle.get('Wikipedia Article', None)
        
        # Progress tracking
        print(f"Processing battle {i}/{total}: {battle_name}...")
        logger.debug(f"[{i}/{total}] Starting enrichment for: {battle_name}")
        
        try:
            # Step 1: Find Q-ID
            qid = wikidata_queries.find_battle_qid(battle_name, wikipedia_article)
            
            if not qid:
                # Battle not found on Wikidata - keep baseline data only
                logger.warning(f"[{i}/{total}] Q-ID not found for: {battle_name}")
                enriched_battle = battle.copy()
                enriched_battle['data_source'] = 'wikipedia_only'
                enriched_battles.append(enriched_battle)
                continue
            
            # Step 2: Get battle data from Wikidata
            wikidata_data = wikidata_queries.get_battle_data(qid)
            
            # Step 3: Enrich the battle
            enriched_battle = wikidata_queries.enrich_battle(battle, qid, wikidata_data)
            enriched_battles.append(enriched_battle)
            
            # Log status
            data_status = "complete" if enriched_battle.get('data_complete') else "partial"
            logger.info(f"[{i}/{total}] ✓ Enriched '{battle_name}' ({data_status})")
            print(f"  ✓ Found Q-ID: {qid} ({data_status} data)")
            
        except Exception as e:
            # Unexpected error - keep baseline data and log error
            logger.error(f"[{i}/{total}] Error enriching '{battle_name}': {e}", exc_info=True)
            enriched_battle = battle.copy()
            enriched_battle['data_source'] = 'wikipedia_only'
            enriched_battles.append(enriched_battle)
            print(f"  ✗ Error: {str(e)}")
    
    return enriched_battles


def save_enriched_battles(battles: List[Dict]) -> bool:
    """
    Save enriched battles to JSON file.
    
    Args:
        battles: List of enriched battle dictionaries
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(battles, f, indent=2)
        logger.info(f"Successfully saved {len(battles)} enriched battles to {OUTPUT_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save enriched battles: {e}")
        return False


def main():
    """Main orchestration function for Wikidata enrichment."""
    logger.info("=" * 60)
    logger.info("Starting Wikidata Enrichment")
    logger.info("=" * 60)
    
    # Setup
    setup_directories()
    
    # Load baseline data
    baseline_battles = load_baseline_battles()
    print(f"DEBUG: Loaded {len(baseline_battles)} baseline battles for enrichment")
    if not baseline_battles:
        logger.error("No baseline battles to process. Exiting.")
        return
    
    # Enrich battles
    print(f"\nEnriching {len(baseline_battles)} battles with Wikidata data...\n")
    enriched_battles = enrich_all_battles(baseline_battles)
    
    # Save results
    print(f"\nSaving enriched battles to {OUTPUT_FILE}...")
    success = save_enriched_battles(enriched_battles)
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        complete_count = sum(1 for b in enriched_battles if b.get('data_complete'))
        partial_count = sum(1 for b in enriched_battles if not b.get('data_complete') and b.get('qid'))
        wikipedia_only = sum(1 for b in enriched_battles if b.get('data_source') == 'wikipedia_only')
        
        print(f"✓ Wikidata Enrichment Complete!")
        print(f"  Total battles: {len(enriched_battles)}")
        print(f"  Complete (coords found): {complete_count}")
        print(f"  Partial (Q-ID but no coords): {partial_count}")
        print(f"  Wikipedia only (not on Wikidata): {wikipedia_only}")
    else:
        print("✗ Wikidata Enrichment Failed - check logs for details")
    
    logger.info("=" * 60)
    logger.info("Wikidata Enrichment Complete")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()