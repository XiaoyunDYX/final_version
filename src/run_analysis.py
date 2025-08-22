#!/usr/bin/env python3
"""
Robot Taxonomy Analysis - Main Runner
Orchestrates the complete robot taxonomy analysis and visualization pipeline
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from data_processor import RobotDataProcessor
from enhanced_robot_visualizer import EnhancedRobotVisualizer
from separate_phylogenetic_generator import SeparatePhylogeneticGenerator

def run_complete_analysis():
    """Run the complete robot taxonomy analysis pipeline"""
    print("🤖 Robot Taxonomy Analysis Pipeline")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Ensure output directories exist
    os.makedirs("outputs/visualizations", exist_ok=True)
    os.makedirs("outputs/phylogenetic_trees", exist_ok=True)
    os.makedirs("outputs/analysis", exist_ok=True)
    
    try:
        # Step 1: Data Processing and Analysis
        print("\n📊 Step 1: Processing Robot Data...")
        processor = RobotDataProcessor(data_path="data/")
        
        # Generate analysis outputs
        processor.analyze_temporal_trends()
        processor.analyze_regional_patterns()
        processor.perform_clustering_analysis()
        
        print("   ✅ Data processing complete")
        
        # Step 2: Generate Main Visualizations
        print("\n🎨 Step 2: Creating Main Visualizations...")
        visualizer = EnhancedRobotVisualizer(data_path="data/")
        
        # Create main visualizations
        visualizer.create_regional_distribution()
        visualizer.create_taxonomy_sunburst() 
        visualizer.create_timeline_visualization()
        visualizer.create_network_graph()
        visualizer.create_dashboard()
        
        print("   ✅ Main visualizations complete")
        
        # Step 3: Generate Phylogenetic Trees
        print("\n🌳 Step 3: Creating Phylogenetic Trees...")
        phylo_generator = SeparatePhylogeneticGenerator(data_path="data/")
        phylo_generator.generate_all_separate_pages(output_dir="outputs/phylogenetic_trees/")
        
        print("   ✅ Phylogenetic trees complete")
        
        print(f"\n🎉 Analysis Complete!")
        print(f"📁 Outputs saved to:")
        print(f"   • outputs/visualizations/ - Main analysis visualizations")
        print(f"   • outputs/phylogenetic_trees/ - Phylogenetic tree visualizations")
        print(f"   • outputs/analysis/ - Raw analysis data")
        
        print(f"\n🌟 Start exploring:")
        print(f"   • outputs/phylogenetic_trees/00_phylogenetic_index.html")
        print(f"   • outputs/visualizations/08_summary_report.html")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in analysis pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_complete_analysis()
    sys.exit(0 if success else 1)
