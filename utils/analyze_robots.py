#!/usr/bin/env python3
"""
Robot Classification Data Analyzer
Interactive tool to explore and analyze robot taxonomy data
"""

import json
import pandas as pd
from collections import defaultdict, Counter
from typing import Dict, List, Any

class RobotAnalyzer:
    def __init__(self, filename: str = 'data/classified_robots_gpt.json'):
        self.filename = filename
        self.robots_data = []
        self.load_data()
    
    def load_data(self):
        """Load robot classification data"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.robots_data = json.load(f)
            print(f"✅ Loaded {len(self.robots_data)} robots from {self.filename}")
        except FileNotFoundError:
            print(f"❌ File {self.filename} not found")
            self.robots_data = []
    
    def get_basic_stats(self):
        """Get basic statistics about the dataset"""
        if not self.robots_data:
            return
        
        print("\n📊 BASIC STATISTICS")
        print("=" * 50)
        print(f"Total robots: {len(self.robots_data)}")
        
        # Count by domain
        domains = Counter(robot.get('domain', 'Unknown') for robot in self.robots_data)
        print(f"\nDomains:")
        for domain, count in domains.most_common():
            print(f"  {domain}: {count} robots")
        
        # Count by kingdom
        kingdoms = Counter(robot.get('kingdom', 'Unknown') for robot in self.robots_data)
        print(f"\nKingdoms:")
        for kingdom, count in kingdoms.most_common():
            print(f"  {kingdom}: {count} robots")
    
    def search_robots(self, keyword: str = None, domain: str = None, kingdom: str = None):
        """Search robots by various criteria"""
        if not self.robots_data:
            return
        
        results = []
        for robot in self.robots_data:
            match = True
            
            if keyword:
                name = robot.get('name', '').lower()
                description = robot.get('description', '').lower()
                if keyword.lower() not in name and keyword.lower() not in description:
                    match = False
            
            if domain and robot.get('domain') != domain:
                match = False
            
            if kingdom and robot.get('kingdom') != kingdom:
                match = False
            
            if match:
                results.append(robot)
        
        print(f"\n🔍 SEARCH RESULTS ({len(results)} robots found)")
        print("=" * 50)
        
        for i, robot in enumerate(results[:10], 1):  # Show first 10
            print(f"\n{i}. {robot.get('name', 'Unknown')}")
            print(f"   Domain: {robot.get('domain', 'Unknown')}")
            print(f"   Kingdom: {robot.get('kingdom', 'Unknown')}")
            print(f"   Morpho-Motion: {robot.get('morpho_motion_class', 'Unknown')}")
            print(f"   Order: {robot.get('order', 'Unknown')}")
            print(f"   Applications: {', '.join(robot.get('application_species', []))}")
            print(f"   URL: {robot.get('url', 'Unknown')}")
        
        if len(results) > 10:
            print(f"\n... and {len(results) - 10} more robots")
        
        return results
    
    def analyze_taxonomy_distribution(self):
        """Analyze distribution across all taxonomy levels"""
        if not self.robots_data:
            return
        
        print("\n📈 TAXONOMY DISTRIBUTION ANALYSIS")
        print("=" * 50)
        
        taxonomy_fields = [
            'domain', 'kingdom', 'morpho_motion_class', 'order', 
            'sensing_family', 'actuation_genus', 'cognition_class'
        ]
        
        for field in taxonomy_fields:
            counter = Counter(robot.get(field, 'Unknown') for robot in self.robots_data)
            print(f"\n{field.upper().replace('_', ' ')}:")
            for category, count in counter.most_common():
                percentage = (count / len(self.robots_data)) * 100
                print(f"  {category}: {count} robots ({percentage:.1f}%)")
    
    def analyze_applications(self):
        """Analyze application species distribution"""
        if not self.robots_data:
            return
        
        print("\n🎯 APPLICATION SPECIES ANALYSIS")
        print("=" * 50)
        
        all_applications = []
        for robot in self.robots_data:
            apps = robot.get('application_species', [])
            if isinstance(apps, list):
                all_applications.extend(apps)
            elif apps:
                all_applications.append(apps)
        
        app_counter = Counter(all_applications)
        print(f"Total applications: {len(all_applications)}")
        print(f"Unique application types: {len(app_counter)}")
        
        print("\nMost common applications:")
        for app, count in app_counter.most_common():
            percentage = (count / len(self.robots_data)) * 100
            print(f"  {app}: {count} robots ({percentage:.1f}%)")
    
    def find_similar_robots(self, robot_name: str, top_n: int = 5):
        """Find robots similar to a given robot"""
        if not self.robots_data:
            return
        
        # Find the target robot
        target_robot = None
        for robot in self.robots_data:
            if robot.get('name', '').lower() == robot_name.lower():
                target_robot = robot
                break
        
        if not target_robot:
            print(f"❌ Robot '{robot_name}' not found")
            return
        
        print(f"\n🔍 SIMILAR ROBOTS TO: {target_robot.get('name')}")
        print("=" * 50)
        
        similarities = []
        for robot in self.robots_data:
            if robot.get('name') == target_robot.get('name'):
                continue
            
            # Calculate similarity score
            score = 0
            if robot.get('domain') == target_robot.get('domain'):
                score += 1
            if robot.get('kingdom') == target_robot.get('kingdom'):
                score += 1
            if robot.get('morpho_motion_class') == target_robot.get('morpho_motion_class'):
                score += 1
            if robot.get('order') == target_robot.get('order'):
                score += 1
            if robot.get('sensing_family') == target_robot.get('sensing_family'):
                score += 1
            if robot.get('actuation_genus') == target_robot.get('actuation_genus'):
                score += 1
            if robot.get('cognition_class') == target_robot.get('cognition_class'):
                score += 1
            
            # Check application overlap
            target_apps = set(target_robot.get('application_species', []))
            robot_apps = set(robot.get('application_species', []))
            app_overlap = len(target_apps.intersection(robot_apps))
            score += app_overlap * 0.5
            
            similarities.append((robot, score))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Target robot classification:")
        print(f"  Domain: {target_robot.get('domain')}")
        print(f"  Kingdom: {target_robot.get('kingdom')}")
        print(f"  Applications: {', '.join(target_robot.get('application_species', []))}")
        
        print(f"\nTop {top_n} similar robots:")
        for i, (robot, score) in enumerate(similarities[:top_n], 1):
            print(f"\n{i}. {robot.get('name')} (Similarity: {score}/8.5)")
            print(f"   Domain: {robot.get('domain')}")
            print(f"   Kingdom: {robot.get('kingdom')}")
            print(f"   Applications: {', '.join(robot.get('application_species', []))}")
    
    def export_to_csv(self, filename: str = 'data/robot_analysis.csv'):
        """Export robot data to CSV for further analysis"""
        if not self.robots_data:
            return
        
        # Flatten the data for CSV export
        flattened_data = []
        for robot in self.robots_data:
            row = {
                'name': robot.get('name', ''),
                'url': robot.get('url', ''),
                'domain': robot.get('domain', ''),
                'kingdom': robot.get('kingdom', ''),
                'morpho_motion_class': robot.get('morpho_motion_class', ''),
                'order': robot.get('order', ''),
                'sensing_family': robot.get('sensing_family', ''),
                'actuation_genus': robot.get('actuation_genus', ''),
                'cognition_class': robot.get('cognition_class', ''),
                'application_species': ';'.join(robot.get('application_species', [])),
                'description': robot.get('description', ''),
                'manufacturer': robot.get('manufacturer', ''),
                'year': robot.get('year', '')
            }
            flattened_data.append(row)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Data exported to {filename}")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")

def interactive_menu():
    """Interactive menu for robot analysis"""
    analyzer = RobotAnalyzer()
    
    while True:
        print("\n" + "="*60)
        print("🤖 ROBOT CLASSIFICATION ANALYZER")
        print("="*60)
        print("1. Basic Statistics")
        print("2. Search Robots")
        print("3. Taxonomy Distribution")
        print("4. Application Analysis")
        print("5. Find Similar Robots")
        print("6. Export to CSV")
        print("7. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            analyzer.get_basic_stats()
        
        elif choice == '2':
            keyword = input("Enter keyword to search (or press Enter to skip): ").strip()
            domain = input("Enter domain filter (or press Enter to skip): ").strip()
            kingdom = input("Enter kingdom filter (or press Enter to skip): ").strip()
            
            analyzer.search_robots(
                keyword if keyword else None,
                domain if domain else None,
                kingdom if kingdom else None
            )
        
        elif choice == '3':
            analyzer.analyze_taxonomy_distribution()
        
        elif choice == '4':
            analyzer.analyze_applications()
        
        elif choice == '5':
            robot_name = input("Enter robot name to find similar robots: ").strip()
            if robot_name:
                analyzer.find_similar_robots(robot_name)
        
        elif choice == '6':
            analyzer.export_to_csv()
        
        elif choice == '7':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    interactive_menu() 