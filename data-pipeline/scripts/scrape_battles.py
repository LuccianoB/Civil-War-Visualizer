"""
Script to scrape battle data from Wikipedia and save it as a CSV file.
Connects to the Wikipedia page, extracts the CWSAC battle data from the table, cleans it, and saves it to a CSV file.
"""
import wikipedia_battles
import json
import os 
from pathlib import Path

def main():
    """Main orchestration function for Step 1A."""
    # 1. Fetch Wikipedia page
    html = wikipedia_battles.fetch_wikipedia_page()
    print(f"✓ Fetched HTML ({len(html)} characters)")
    
    # 2. Parse battles from table
    battles = wikipedia_battles.parse_CWSAC_from_table(html)
    print(f"✓ Parsed {len(battles)} battles from table")
    
    # 3. Clean the data
    cleaned_battles = wikipedia_battles.clean_battle_data(battles)
    print(f"✓ Cleaned {len(cleaned_battles)} battles")
    
    # 4. Parse dates into structured start_date / end_date
    for battle in cleaned_battles:
        date_info = wikipedia_battles.parse_date_range(battle.get('Date', ''))
        battle['start_date'] = date_info['start_date']
        battle['end_date'] = date_info['end_date']
    parsed_count = sum(1 for b in cleaned_battles if b['start_date'])
    print(f"✓ Parsed dates for {parsed_count}/{len(cleaned_battles)} battles")
    
    # 5. Filter by class
    filtered_battles = wikipedia_battles.filter_by_class(cleaned_battles)
    print(f"✓ Filtered to {len(filtered_battles)} battles")
    
    # 6. Save to JSON
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent  # Go up from scripts/ to data-pipeline/
    output_dir = script_dir / 'raw_data'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'baseline_battles.json'
    
    with open(output_file, 'w') as f:
        json.dump(filtered_battles, f, indent=2)
    
    print(f"✓ Saved {len(filtered_battles)} battles to {output_file}")

if __name__ == '__main__':
    main()