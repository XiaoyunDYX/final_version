#!/usr/bin/env python3
import json
import argparse
from typing import List, Dict

def is_valid_robot_entry(robot: Dict) -> bool:
    """
    Return True if this robot entry looks like a real robot:
      1. Name does not contain category/list/portal keywords
      2. Description is at least 50 characters long
    """
    name = robot.get("name", "").lower()
    description = robot.get("description", "")
    

    # 1) Exclude entries that are clearly pages of lists/categories
    bad_keywords = ["category:", "list_of", "portal:",] 
    if any(kw in name for kw in bad_keywords):
        return False

    # 2) Require a reasonably long description
    if not description or len(description) < 50:
        return False

    # 3) Must have either an application tag or a manufacturer
    

    return True

def filter_robots(input_path: str, output_path: str) -> None:
    # Load the original robots JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        robots = json.load(f)

    # Apply the filter
    cleaned: List[Dict] = [r for r in robots if is_valid_robot_entry(r)]

    # Save the cleaned list
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Filtered {len(robots)} → {len(cleaned)} valid robot entries.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Filter out invalid/dirty robot entries from a JSON file."
    )
    parser.add_argument(
        "input_json",
        help="Path to the original robots_data.json"
    )
    parser.add_argument(
        "output_json",
        help="Path where the cleaned JSON should be saved"
    )
    args = parser.parse_args()

    filter_robots(args.input_json, args.output_json)
