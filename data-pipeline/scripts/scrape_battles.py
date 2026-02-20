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
    
    # 4. Filter by class
    filtered_battles = wikipedia_battles.filter_by_class(cleaned_battles)
    print(f"✓ Filtered to {len(filtered_battles)} battles")
    
    # 5. Save to JSON
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