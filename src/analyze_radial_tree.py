#!/usr/bin/env python3
"""
Radial Tree Analysis Script
Analyzes the results of the radial tree visualization and provides insights
"""

import json
import pandas as pd
from collections import Counter, defaultdict
from typing import Dict, List, Any

class RadialTreeAnalyzer:
    def __init__(self, filename: str = 'data/classified_robots_gpt.json'):
        self.filename = filename
        self.robots_data = []
        self.load_data()
    
    def load_data(self):
        """Load robot classification data"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.robots_data = json.load(f)
            print(f"✅ Loaded {len(self.robots_data)} robots for radial tree analysis")
        except FileNotFoundError:
            print(f"❌ File {self.filename} not found")
            self.robots_data = []
    
    def analyze_radial_structure(self):
        """Analyze the radial tree structure and hierarchy"""
        if not self.robots_data:
            return
        
        print("\n🌳 RADIAL TREE STRUCTURE ANALYSIS")
        print("=" * 60)
        
        # Analyze the hierarchical levels
        print(f"Total robots in tree: {len(self.robots_data)}")
        
        # Count robots at each taxonomic level
        taxonomy_levels = {
            'Domain': 'domain',
            'Kingdom': 'kingdom', 
            'Morpho_Motion_Class': 'morpho_motion_class',
            'Order': 'order',
            'Sensing_Family': 'sensing_family',
            'Actuation_Genus': 'actuation_genus',
            'Cognition_Class': 'cognition_class',
            'Application_Species': 'application_species'
        }
        
        print("\n📊 DISTRIBUTION BY TAXONOMIC LEVEL:")
        print("-" * 40)
        
        for level_name, field_name in taxonomy_levels.items():
            if field_name == 'application_species':
                # Handle list of applications
                all_apps = []
                for robot in self.robots_data:
                    apps = robot.get('application_species', [])
                    if isinstance(apps, list):
                        all_apps.extend(apps)
                    elif apps:
                        all_apps.append(apps)
                
                app_counter = Counter(all_apps)
                print(f"\n{level_name} (Applications):")
                for app, count in app_counter.most_common(10):
                    percentage = (count / len(self.robots_data)) * 100
                    print(f"  {app}: {count} robots ({percentage:.1f}%)")
            else:
                counter = Counter(robot.get(field_name, 'Unknown') for robot in self.robots_data)
                print(f"\n{level_name}:")
                for category, count in counter.most_common():
                    percentage = (count / len(self.robots_data)) * 100
                    print(f"  {category}: {count} robots ({percentage:.1f}%)")
    
    def analyze_central_hub(self):
        """Analyze the central hub (root) of the radial tree"""
        print("\n🎯 CENTRAL HUB ANALYSIS")
        print("=" * 40)
        
        # The central hub represents the root "Robots" node
        print("Central Hub: 'Robots' (Root Node)")
        print(f"Total branches from root: {len(self.robots_data)}")
        
        # Analyze direct connections from root (Domain level)
        domain_counter = Counter(robot.get('domain', 'Unknown') for robot in self.robots_data)
        print("\nDirect branches from root (Domains):")
        for domain, count in domain_counter.items():
            percentage = (count / len(self.robots_data)) * 100
            print(f"  {domain}: {count} robots ({percentage:.1f}%)")
    
    def analyze_branching_patterns(self):
        """Analyze branching patterns in the radial tree"""
        print("\n🌿 BRANCHING PATTERN ANALYSIS")
        print("=" * 40)
        
        # Analyze how robots branch through the taxonomy
        branching_data = defaultdict(int)
        
        for robot in self.robots_data:
            # Create a path through the taxonomy
            path = [
                robot.get('domain', 'Unknown'),
                robot.get('kingdom', 'Unknown'),
                robot.get('morpho_motion_class', 'Unknown'),
                robot.get('order', 'Unknown'),
                robot.get('sensing_family', 'Unknown'),
                robot.get('actuation_genus', 'Unknown'),
                robot.get('cognition_class', 'Unknown')
            ]
            
            # Count unique paths
            path_key = ' → '.join(path)
            branching_data[path_key] += 1
        
        print(f"Total unique taxonomic paths: {len(branching_data)}")
        print(f"Average robots per path: {len(self.robots_data) / len(branching_data):.1f}")
        
        print("\nMost common taxonomic paths:")
        for path, count in sorted(branching_data.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {count} robots: {path}")
    
    def analyze_leaf_distribution(self):
        """Analyze the distribution of leaves (individual robots) in the radial tree"""
        print("\n🍃 LEAF DISTRIBUTION ANALYSIS")
        print("=" * 40)
        
        # Analyze how robots are distributed as leaves
        leaf_clusters = defaultdict(list)
        
        for robot in self.robots_data:
            # Group robots by their final classification
            final_class = robot.get('cognition_class', 'Unknown')
            leaf_clusters[final_class].append(robot)
        
        print(f"Number of leaf clusters: {len(leaf_clusters)}")
        
        print("\nLeaf cluster sizes:")
        for cluster, robots in sorted(leaf_clusters.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {cluster}: {len(robots)} robots")
        
        # Find the most diverse leaf cluster
        most_diverse = max(leaf_clusters.items(), key=lambda x: len(set(r.get('application_species', []) for r in x[1] if isinstance(r.get('application_species'), list))))
        print(f"\nMost diverse leaf cluster: {most_diverse[0]} ({len(most_diverse[1])} robots)")
    
    def analyze_radial_density(self):
        """Analyze the density distribution in the radial tree"""
        print("\n📊 RADIAL DENSITY ANALYSIS")
        print("=" * 40)
        
        # Analyze density at different radial distances
        domain_density = Counter(robot.get('domain', 'Unknown') for robot in self.robots_data)
        kingdom_density = Counter(robot.get('kingdom', 'Unknown') for robot in self.robots_data)
        
        print("Density at different radial levels:")
        print(f"  Level 1 (Domain): {len(domain_density)} categories")
        print(f"  Level 2 (Kingdom): {len(kingdom_density)} categories")
        
        # Calculate density metrics
        total_robots = len(self.robots_data)
        avg_domain_density = total_robots / len(domain_density)
        avg_kingdom_density = total_robots / len(kingdom_density)
        
        print(f"  Average robots per domain: {avg_domain_density:.1f}")
        print(f"  Average robots per kingdom: {avg_kingdom_density:.1f}")
        
        # Find most and least dense areas
        most_dense_domain = domain_density.most_common(1)[0]
        least_dense_domain = domain_density.most_common()[-1]
        
        print(f"\nMost dense domain: {most_dense_domain[0]} ({most_dense_domain[1]} robots)")
        print(f"Least dense domain: {least_dense_domain[0]} ({least_dense_domain[1]} robots)")
    
    def find_radial_clusters(self):
        """Find natural clusters in the radial tree"""
        print("\n🔍 RADIAL CLUSTER ANALYSIS")
        print("=" * 40)
        
        # Find robots that share multiple characteristics
        clusters = defaultdict(list)
        
        for robot in self.robots_data:
            # Create cluster key based on domain + kingdom + morpho_motion
            cluster_key = f"{robot.get('domain', 'Unknown')}-{robot.get('kingdom', 'Unknown')}-{robot.get('morpho_motion_class', 'Unknown')}"
            clusters[cluster_key].append(robot)
        
        # Find largest clusters
        largest_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        print("Largest radial clusters:")
        for i, (cluster_key, robots) in enumerate(largest_clusters, 1):
            print(f"\n{i}. {cluster_key}: {len(robots)} robots")
            
            # Show sample robots from this cluster
            sample_robots = robots[:3]
            for robot in sample_robots:
                print(f"   - {robot.get('name', 'Unknown')} ({', '.join(robot.get('application_species', []))})")
    
    def analyze_radial_balance(self):
        """Analyze the balance of the radial tree"""
        print("\n⚖️ RADIAL BALANCE ANALYSIS")
        print("=" * 40)
        
        # Check if the tree is balanced across different axes
        domain_counts = Counter(robot.get('domain', 'Unknown') for robot in self.robots_data)
        kingdom_counts = Counter(robot.get('kingdom', 'Unknown') for robot in self.robots_data)
        
        # Calculate balance metrics
        domain_balance = max(domain_counts.values()) / min(domain_counts.values()) if domain_counts else 0
        kingdom_balance = max(kingdom_counts.values()) / min(kingdom_counts.values()) if kingdom_counts else 0
        
        print(f"Domain balance ratio (max/min): {domain_balance:.2f}")
        print(f"Kingdom balance ratio (max/min): {kingdom_balance:.2f}")
        
        if domain_balance < 2:
            print("✅ Domain distribution is relatively balanced")
        else:
            print("⚠️ Domain distribution is imbalanced")
        
        if kingdom_balance < 3:
            print("✅ Kingdom distribution is relatively balanced")
        else:
            print("⚠️ Kingdom distribution is imbalanced")
    
    def generate_radial_insights(self):
        """Generate overall insights about the radial tree"""
        print("\n💡 RADIAL TREE INSIGHTS")
        print("=" * 40)
        
        # Key insights
        total_robots = len(self.robots_data)
        unique_domains = len(set(robot.get('domain', 'Unknown') for robot in self.robots_data))
        unique_kingdoms = len(set(robot.get('kingdom', 'Unknown') for robot in self.robots_data))
        
        print(f"📈 Scale: {total_robots} robots across {unique_domains} domains and {unique_kingdoms} kingdoms")
        
        # Most common characteristics
        most_common_domain = Counter(robot.get('domain', 'Unknown') for robot in self.robots_data).most_common(1)[0]
        most_common_kingdom = Counter(robot.get('kingdom', 'Unknown') for robot in self.robots_data).most_common(1)[0]
        
        print(f"🎯 Dominant domain: {most_common_domain[0]} ({most_common_domain[1]} robots, {(most_common_domain[1]/total_robots)*100:.1f}%)")
        print(f"🎯 Dominant kingdom: {most_common_kingdom[0]} ({most_common_kingdom[1]} robots, {(most_common_kingdom[1]/total_robots)*100:.1f}%)")
        
        # Diversity assessment
        all_apps = []
        for robot in self.robots_data:
            apps = robot.get('application_species', [])
            if isinstance(apps, list):
                all_apps.extend(apps)
            elif apps:
                all_apps.append(apps)
        
        unique_apps = len(set(all_apps))
        print(f"🌍 Application diversity: {unique_apps} unique application types")
        
        # Tree complexity
        print(f"🌳 Tree complexity: High (multiple taxonomic levels with {total_robots} end nodes)")
        
        # Recommendations
        print("\n📋 RECOMMENDATIONS:")
        print("1. Focus on the most populated branches for detailed analysis")
        print("2. Investigate sparse areas for potential gaps in robot taxonomy")
        print("3. Use the radial structure to identify evolutionary relationships")
        print("4. Consider the balance when adding new robot classifications")

def main():
    """Main analysis function"""
    analyzer = RadialTreeAnalyzer()
    
    if not analyzer.robots_data:
        print("❌ No data loaded. Please check the file path.")
        return
    
    print("🌳 RADIAL TREE VISUALIZATION ANALYSIS")
    print("=" * 60)
    print("Analyzing the radial tree structure and robot taxonomy...")
    
    # Run all analyses
    analyzer.analyze_radial_structure()
    analyzer.analyze_central_hub()
    analyzer.analyze_branching_patterns()
    analyzer.analyze_leaf_distribution()
    analyzer.analyze_radial_density()
    analyzer.find_radial_clusters()
    analyzer.analyze_radial_balance()
    analyzer.generate_radial_insights()
    
    print("\n✅ Radial tree analysis complete!")
    print("📁 Check 'data/robot_radial_tree.png' for the visual representation")

if __name__ == "__main__":
    main() 