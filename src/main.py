#!/usr/bin/env python3
"""
Robot Taxonomy Agent - Main Application

This application scrapes the internet for robot examples, classifies them according to a taxonomy,
and displays the information graphically as a "tree of life" for robots.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Optional

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_scraper.robot_scraper import RobotScraper
from classifier.robot_classifier import RobotClassifier
from visualizer.robot_tree_visualizer import RobotTreeVisualizer

class RobotTaxonomyAgent:
    """Main application class for robot taxonomy analysis."""
    
    def __init__(self):
        """Initialize the robot taxonomy agent with all components."""
        self.scraper = RobotScraper()
        self.classifier = RobotClassifier()
        self.visualizer = RobotTreeVisualizer()
        
        # Ensure data directory exists
        os.makedirs('./data', exist_ok=True)
        
    def run_full_pipeline(self, search_terms: Optional[List[str]] = None, 
                         launch_dashboard: bool = True) -> None:
        """
        Run the complete pipeline: scrape -> classify -> visualize
        
        Args:
            search_terms: List of search terms for web scraping
            launch_dashboard: Whether to launch the interactive dashboard
        """
        print("🤖 Robot Taxonomy Agent Starting...")
        print("=" * 50)
        
        try:
            # Step 1: Web Scraping
            print("\n📡 Step 1: Scraping robot data from the internet...")
            if search_terms is None:
                search_terms = [
                    "industrial robots",
                    "service robots", 
                    "humanoid robots",
                    "medical robots",
                    "military robots",
                    "domestic robots",
                    "educational robots",
                    "space robots",
                    "underwater robots",
                    "aerial robots"
                ]
            
            robots_data = self.scraper.search_robots(search_terms)
            self.scraper.robots_data = robots_data
            self.scraper.save_data()
            print(f"✅ Found {len(robots_data)} robots")
            
            # Step 2: Classification
            print("\n🏷️  Step 2: Classifying robots according to taxonomy...")
            classified_robots = self.classifier.classify_robots(robots_data)
            
            # Perform clustering
            clustering_info = self.classifier.cluster_robots()
            self.classifier.save_classified_data()
            
            # Print classification summary
            summary = self.classifier.get_taxonomy_summary()
            self._print_classification_summary(summary)
            
            # Step 3: Visualization
            print("\n🌳 Step 3: Creating robot tree of life visualization...")
            self.visualizer.load_data()
            
            if launch_dashboard:
                self._launch_dashboard()
            else:
                self._create_png_visualizations()
            
            print("\n🎉 Robot Taxonomy Agent completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during pipeline execution: {str(e)}")
            raise
    
    def run_scraper_only(self, search_terms: Optional[List[str]] = None) -> None:
        """
        Run only the web scraper
        
        Args:
            search_terms: List of search terms for web scraping
        """
        print("📡 Running web scraper only...")
        try:
            if search_terms is None:
                search_terms = ["industrial robots", "service robots", "humanoid robots"]
            
            robots_data = self.scraper.search_robots(search_terms)
            self.scraper.robots_data = robots_data
            self.scraper.save_data()
            print(f"✅ Scraped {len(robots_data)} robots")
            
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            raise
    
    def run_classifier_only(self) -> None:
        """Run only the classifier on existing data"""
        print("🏷️  Running classifier only...")
        try:
            with open('./data/robots_data.json', 'r', encoding='utf-8') as f:
                robots_data = json.load(f)
            
            classified_robots = self.classifier.classify_robots(robots_data)
            clustering_info = self.classifier.cluster_robots()
            self.classifier.save_classified_data()
            
            summary = self.classifier.get_taxonomy_summary()
            self._print_classification_summary(summary)
            
        except FileNotFoundError:
            print("❌ No robot data found. Please run the scraper first.")
        except Exception as e:
            print(f"❌ Error during classification: {str(e)}")
            raise
    
    def run_visualizer_only(self, launch_dashboard: bool = True) -> None:
        """
        Run only the visualizer on existing classified data
        
        Args:
            launch_dashboard: Whether to launch the interactive dashboard
        """
        print("🌳 Running visualizer only...")
        try:
            self.visualizer.load_data()
            
            if launch_dashboard:
                self._launch_dashboard()
            else:
                self._create_png_visualizations()
                
        except FileNotFoundError:
            print("❌ No classified robot data found. Please run the classifier first.")
        except Exception as e:
            print(f"❌ Error during visualization: {str(e)}")
            raise
    
    def _print_classification_summary(self, summary: dict) -> None:
        """Print a formatted classification summary"""
        print(f"✅ Classified {summary['total_robots']} robots")
        print("📊 Classification Summary:")
        print(f"   Domains: {summary['domain_distribution']}")
        print(f"   Kingdoms: {summary['kingdom_distribution']}")
        print(f"   Phyla: {summary['phylum_distribution']}")
        print(f"   Classes: {summary['class_distribution']}")
        print(f"   Orders: {summary['order_distribution']}")
        print(f"   Families: {summary['family_distribution']}")
        print(f"   Genera: {summary['genus_distribution']}")
        print(f"   Species: {summary['species_distribution']}")
    
    def _launch_dashboard(self) -> None:
        """Launch the interactive dashboard"""
        print("\n🚀 Launching interactive dashboard...")
        print("📱 Open your browser to http://localhost:8050")
        app = self.visualizer.create_dashboard()
        app.run(debug=False, port=8050)
    
    def _create_png_visualizations(self) -> None:
        """Create and save PNG visualizations"""
        print("\n📊 Creating PNG visualizations...")
        self.visualizer.save_radial_tree_as_png()
        self.visualizer.save_phylogenetic_tree_as_png()
        self.visualizer.save_dendrogram_as_png()
        self.visualizer.save_cluster_as_png()
        self.visualizer.save_taxonomy_bar_charts_as_png()
        self.visualizer.save_simplified_tree_as_png()
        self.visualizer.save_taxonomy_summary_as_png()
        print("✅ PNG visualizations saved to data/")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Robot Taxonomy Agent - Analyze and visualize robot classifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run full pipeline with dashboard
  python main.py --mode scraper     # Run only web scraping
  python main.py --mode classifier  # Run only classification
  python main.py --mode visualizer  # Run only visualization
  python main.py --no-dashboard     # Run full pipeline without dashboard
  python main.py --search-terms "industrial robots" "medical robots"
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['full', 'scraper', 'classifier', 'visualizer'], 
        default='full', 
        help='Which components to run (default: full)'
    )
    parser.add_argument(
        '--no-dashboard', 
        action='store_true', 
        help='Don\'t launch the interactive dashboard'
    )
    parser.add_argument(
        '--search-terms', 
        nargs='+', 
        help='Custom search terms for scraping'
    )
    
    args = parser.parse_args()
    
    try:
        agent = RobotTaxonomyAgent()
        
        if args.mode == 'full':
            agent.run_full_pipeline(
                search_terms=args.search_terms, 
                launch_dashboard=not args.no_dashboard
            )
        elif args.mode == 'scraper':
            agent.run_scraper_only(search_terms=args.search_terms)
        elif args.mode == 'classifier':
            agent.run_classifier_only()
        elif args.mode == 'visualizer':
            agent.run_visualizer_only(launch_dashboard=not args.no_dashboard)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 