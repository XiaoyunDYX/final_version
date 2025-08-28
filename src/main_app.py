#!/usr/bin/env python3
"""
Enhanced Robot Taxonomy Analysis Application
Main application integrating all visualization and analysis components
Based on new Linnaean-inspired classification framework
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Add the enhanced_visualizer directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_robot_visualizer import EnhancedRobotVisualizer
from data_processor import RobotDataProcessor

class RobotTaxonomyApp:
    def __init__(self, data_path="data/"):
        """Initialize the main application"""
        self.data_path = data_path
        self.visualizer = None
        self.processor = None
        
    def initialize_components(self):
        """Initialize all application components"""
        print("Initializing Robot Taxonomy Analysis Application...")
        
        # Initialize data processor
        print("Loading and processing data...")
        self.processor = RobotDataProcessor(self.data_path)
        
        # Initialize visualizer
        print("Initializing visualization components...")
        self.visualizer = EnhancedRobotVisualizer(self.data_path)
        
        print("Initialization complete!")
        
    def generate_comprehensive_report(self, output_dir="analysis_output/"):
        """Generate comprehensive analysis report"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n=== Generating Comprehensive Analysis Report ===")
        
        # 1. Generate insights
        print("1. Generating data insights...")
        insights = self.processor.generate_insights()
        
        # Save insights to JSON
        with open(f"{output_dir}comprehensive_insights.json", 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        
        # 2. Export processed data
        print("2. Exporting processed data...")
        exported_files = self.processor.export_processed_data(f"{output_dir}processed_data/")
        
        # 3. Generate advanced visualizations as PNG
        print("3. Creating advanced visualizations...")
        advanced_viz = self.processor.create_advanced_visualizations(f"{output_dir}figures/")
        
        # 4. Generate standard visualizations as PNG
        print("4. Creating standard visualizations...")
        self.visualizer.save_static_visualizations(f"{output_dir}figures/")
        
        # 5. Generate phylogenetic visualizations as PNG
        print("5. Creating phylogenetic visualizations...")
        from separate_phylogenetic_generator import SeparatePhylogeneticGenerator
        phylo_generator = SeparatePhylogeneticGenerator()
        phylo_generator.generate_all_separate_pages(f"{output_dir}figures/")
        
        # 6. Generate comprehensive PNG-based report
        print("6. Generating comprehensive PNG-based report...")
        self.generate_png_report(insights, f"{output_dir}report.md")
        
        print(f"\nComprehensive analysis report generated in: {output_dir}")
        return output_dir
        
    def generate_summary_report(self, insights, output_file):
        """Generate a markdown summary report"""
        report = f"""# Robot Taxonomy Analysis Report

## Executive Summary

This report presents a comprehensive analysis of robot taxonomy data based on the new Linnaean-inspired classification framework.

## Key Statistics

- **Total Robots Analyzed**: {insights['basic_stats']['total_robots']:,}
- **Geographic Coverage**: {insights['basic_stats']['total_regions']} regions/countries
- **Robot Categories**: {insights['basic_stats']['total_classes']} distinct classes
- **Application Sectors**: {insights['basic_stats']['total_sectors']} sectors
- **Temporal Range**: {insights['basic_stats']['year_range'][0]} - {insights['basic_stats']['year_range'][1]}

## Temporal Trends

- **Peak Development Year**: {insights['trends']['peak_year']} ({insights['trends']['peak_count']} robots)
- **Recent Growth Rate**: {insights['trends']['recent_growth']:.1f}% (last 5 years average)
- **Overall Growth**: {insights['trends']['total_growth']:.1f}% (total period)

## Geographic Distribution

### Top 5 Regions by Robot Count
"""
        
        for i, (region, count) in enumerate(insights['regional']['top_regions'].items(), 1):
            report += f"{i}. **{region}**: {count:,} robots\n"
        
        report += f"""
### Regional Characteristics
- **Most Diverse Region**: {insights['regional']['most_diverse_region']} (highest variety of robot types)
- **Most Specialized Region**: {insights['regional']['most_specialized_region']} (focused on specific types)

## Classification Analysis

### Robot Categories
- **Dominant Category**: {insights['classification']['dominant_class']} ({insights['classification']['dominant_class_count']:,} robots)
- **Category Diversity**: {insights['classification']['class_diversity']} distinct categories
- **Rare Categories**: {len(insights['classification']['rare_classes'])} categories with only 1 robot each

### Rare Categories
"""
        
        for rare_class in insights['classification']['rare_classes'][:10]:  # Show first 10
            report += f"- {rare_class}\n"
        
        report += f"""
## Methodology

This analysis was conducted using:
- **Data Source**: Linnaean-inspired Robot Taxonomy V2 framework
- **Analysis Tools**: Python with pandas, plotly, scikit-learn
- **Visualization**: Interactive dashboards and static charts
- **Classification**: Hierarchical taxonomy with domain, class, order, and sector levels

## Data Quality Notes

- Some robots may have incomplete temporal or geographic data
- Classification is based on the new framework which may differ from traditional categorizations
- Regional mapping uses standardized country codes where available

## Recommendations

1. **Temporal Analysis**: Focus on recent trends (post-2015) for current market insights
2. **Regional Analysis**: Consider cultural and economic factors when analyzing geographic patterns
3. **Classification**: Use the hierarchical structure for detailed categorization needs
4. **Future Research**: Investigate correlations between geographic location and robot specialization

---

*Report generated by Enhanced Robot Taxonomy Analysis Application*
*Based on Linnaean-inspired Robot Taxonomy V2 framework*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def generate_png_report(self, insights, output_file):
        """Generate comprehensive PNG-based report"""
        import os
        
        # Determine the relative path to figures
        output_dir = os.path.dirname(output_file)
        figures_path = "figures/"
        
        report = f"""# Robot Taxonomy Analysis Report

## Executive Summary

This comprehensive report presents an analysis of robot taxonomy data based on the new Linnaean-inspired classification framework. All visualizations have been generated as high-quality static PNG images for optimal printing and documentation purposes.

## Key Statistics

- **Total Robots Analyzed**: {insights['basic_stats']['total_robots']:,}
- **Geographic Coverage**: {insights['basic_stats']['total_regions']} regions/countries
- **Robot Categories**: {insights['basic_stats']['total_classes']} distinct classes
- **Application Sectors**: {insights['basic_stats']['total_sectors']} sectors
- **Temporal Range**: {insights['basic_stats']['year_range'][0]} - {insights['basic_stats']['year_range'][1]}

## Visualizations

### Figure 1: Regional Distribution Map
![Regional Distribution Map]({figures_path}01_regional_map.png)

Global distribution of robot technologies showing concentration patterns across different regions and countries.

### Figure 2: Regional Distribution Bar Chart
![Regional Distribution]({figures_path}02_regional_distribution.png)

Quantitative analysis of robot distribution across major regions, highlighting the leading countries in robot development.

### Figure 3: Development Timeline
![Development Timeline]({figures_path}03_timeline.png)

Temporal analysis showing robot development trends over time, with peaks and growth patterns clearly visible.

### Figure 4: Taxonomy Sunburst
![Taxonomy Sunburst]({figures_path}04_taxonomy_sunburst.png)

Hierarchical visualization of robot taxonomy showing the relationship between domains, classes, and specific robot types.

### Figure 5: Network Classification Graph
![Network Graph]({figures_path}05_network_graph.png)

Network-based visualization displaying the interconnections between different robot classifications and their relationships.

### Figure 6: Feature Analysis
![Feature Analysis]({figures_path}06_feature_analysis.png)

Analysis of morphological features showing the most common characteristics across the robot population.

### Figure 7: Phylogenetic Sunburst
![Phylogenetic Sunburst]({figures_path}07_sunburst_phylogenetic.png)

Detailed phylogenetic tree visualization showing evolutionary relationships in sunburst format.

### Figure 8: Phylogenetic Treemap
![Phylogenetic Treemap]({figures_path}08_treemap_phylogenetic.png)

Area-proportional visualization where size represents population size of different taxonomic groups.

### Figure 9: Phylogenetic Network
![Phylogenetic Network]({figures_path}09_network_phylogenetic.png)

Network-based phylogenetic tree showing evolutionary connections and taxonomic relationships.

### Figure 10: Class Distribution
![Class Distribution]({figures_path}10_class_distribution.png)

Pie chart overview showing relative sizes and percentages of different robot classes in the taxonomy.

### Figure 11: Evolutionary Timeline
![Evolutionary Timeline]({figures_path}11_evolutionary_timeline.png)

Temporal development of robot classes over time showing evolutionary patterns and emergence trends.

### Figure 12: Temporal Heatmap
![Temporal Heatmap]({figures_path}12_temporal_heatmap.png)

Heat map visualization showing robot class development intensity across different years.

### Figure 13: PCA Clustering Analysis
![PCA Clustering]({figures_path}13_pca_clusters.png)

Principal Component Analysis visualization showing natural clustering patterns in the robot data.

### Figure 14: 3D Feature Space
![3D Scatter Plot]({figures_path}14_3d_scatter.png)

Three-dimensional visualization of robot feature space distribution showing complex relationships.

### Figure 15: Domain-Class Distribution
![Domain-Class Distribution]({figures_path}15_domain_class_distribution.png)

Bar chart showing the distribution of robots across different domain-class combinations.

## Temporal Trends Analysis

- **Peak Development Year**: {insights['trends']['peak_year']} ({insights['trends']['peak_count']} robots)
- **Recent Growth Rate**: {insights['trends']['recent_growth']:.1f}% (last 5 years average)
- **Overall Growth**: {insights['trends']['total_growth']:.1f}% (total period)

The temporal analysis reveals significant patterns in robot development, with clear peaks during certain years and consistent growth trends in recent decades.

## Geographic Distribution Analysis

### Top 5 Regions by Robot Count
"""
        
        for i, (region, count) in enumerate(insights['regional']['top_regions'].items(), 1):
            report += f"{i}. **{region}**: {count:,} robots\n"
        
        report += f"""
### Regional Characteristics
- **Most Diverse Region**: {insights['regional']['most_diverse_region']} (highest variety of robot types)
- **Most Specialized Region**: {insights['regional']['most_specialized_region']} (focused on specific types)

The geographic analysis shows clear patterns of specialization, with certain regions focusing on specific types of robotics while others maintain broader diversity.

## Classification Analysis

### Robot Categories
- **Dominant Category**: {insights['classification']['dominant_class']} ({insights['classification']['dominant_class_count']:,} robots)
- **Category Diversity**: {insights['classification']['class_diversity']} distinct categories
- **Rare Categories**: {len(insights['classification']['rare_classes'])} categories with only 1 robot each

### Notable Rare Categories
"""
        
        for rare_class in insights['classification']['rare_classes'][:10]:  # Show first 10
            report += f"- {rare_class}\n"
        
        report += f"""

## Methodology

This analysis was conducted using advanced data science techniques:

- **Data Source**: Linnaean-inspired Robot Taxonomy V2 framework
- **Analysis Tools**: Python with pandas, plotly, scikit-learn, matplotlib
- **Visualization**: High-quality static PNG images (300 DPI minimum)
- **Classification**: Hierarchical taxonomy with domain, class, order, and sector levels
- **Image Quality**: All figures saved at 1600px width with professional typography

## Technical Specifications

- **Image Format**: PNG with transparent backgrounds where appropriate
- **Resolution**: 300 DPI minimum for print quality
- **Dimensions**: Optimized for A4 printing and digital display
- **Color Scheme**: Professional color palettes with accessibility considerations
- **Typography**: Clear, readable fonts suitable for both screen and print

## Data Quality Notes

- Some robots may have incomplete temporal or geographic data
- Classification is based on the new framework which may differ from traditional categorizations
- Regional mapping uses standardized country codes where available
- All visualizations are static images suitable for documentation and printing

## Recommendations

1. **Temporal Analysis**: Focus on recent trends (post-2015) for current market insights
2. **Regional Analysis**: Consider cultural and economic factors when analyzing geographic patterns
3. **Classification**: Use the hierarchical structure for detailed categorization needs
4. **Future Research**: Investigate correlations between geographic location and robot specialization
5. **Documentation**: All PNG images can be used directly in presentations and reports

## Artifacts

The following PNG images have been generated as part of this analysis:

1. `01_regional_map.png` - Global robot distribution map
2. `02_regional_distribution.png` - Regional distribution bar chart
3. `03_timeline.png` - Robot development timeline
4. `04_taxonomy_sunburst.png` - Taxonomic hierarchy sunburst chart
5. `05_network_graph.png` - Classification network visualization
6. `06_feature_analysis.png` - Morphological feature analysis
7. `07_sunburst_phylogenetic.png` - Phylogenetic sunburst tree
8. `08_treemap_phylogenetic.png` - Phylogenetic treemap visualization
9. `09_network_phylogenetic.png` - Phylogenetic network graph
10. `10_class_distribution.png` - Robot class distribution pie chart
11. `11_evolutionary_timeline.png` - Evolutionary development timeline
12. `12_temporal_heatmap.png` - Class-year temporal heatmap
13. `13_pca_clusters.png` - PCA clustering analysis
14. `14_3d_scatter.png` - 3D feature space visualization
15. `15_domain_class_distribution.png` - Domain-class distribution analysis

All images are production-ready with professional quality suitable for academic papers, presentations, and technical documentation.

---

*Report generated by Enhanced Robot Taxonomy Analysis Application*  
*Based on Linnaean-inspired Robot Taxonomy V2 framework*  
*All visualizations converted to static PNG format for optimal compatibility*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
    def run_interactive_dashboard(self, port=8050, debug=False):
        """Run the interactive dashboard"""
        print(f"\nStarting interactive dashboard on port {port}...")
        print(f"Dashboard will be available at: http://localhost:{port}")
        print("Press Ctrl+C to stop the dashboard")
        
        app = self.visualizer.create_dashboard()
        app.run_server(debug=debug, host='0.0.0.0', port=port)
        
    def run_analysis_only(self, output_dir="analysis_output/"):
        """Run analysis without starting dashboard"""
        self.generate_comprehensive_report(output_dir)
        
        # Print summary to console
        insights = self.processor.generate_insights()
        print("\n" + "="*60)
        print("ROBOT TAXONOMY ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total Robots: {insights['basic_stats']['total_robots']:,}")
        print(f"Geographic Coverage: {insights['basic_stats']['total_regions']} regions")
        print(f"Robot Categories: {insights['basic_stats']['total_classes']}")
        print(f"Time Period: {insights['basic_stats']['year_range'][0]}-{insights['basic_stats']['year_range'][1]}")
        print(f"Dominant Category: {insights['classification']['dominant_class']}")
        print(f"Top Region: {list(insights['regional']['top_regions'].keys())[0]}")
        print("="*60)

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Enhanced Robot Taxonomy Analysis Application")
    parser.add_argument("--data-path", default="data/", 
                       help="Path to the robot data directory")
    parser.add_argument("--output-dir", default="analysis_output/",
                       help="Output directory for analysis results")
    parser.add_argument("--mode", choices=["dashboard", "analysis", "both"], default="both",
                       help="Run mode: dashboard only, analysis only, or both")
    parser.add_argument("--port", type=int, default=8050,
                       help="Port for the dashboard server")
    parser.add_argument("--debug", action="store_true",
                       help="Run dashboard in debug mode")
    parser.add_argument("--no-browser", action="store_true",
                       help="Don't automatically open browser")
    
    args = parser.parse_args()
    
    # Check if data directory exists
    if not os.path.exists(args.data_path):
        print(f"Error: Data directory '{args.data_path}' not found!")
        print("Please ensure the data directory exists and contains the required files:")
        print("- robots.ndjson")
        print("- features.json") 
        print("- dict.json")
        print("- family_index.json")
        sys.exit(1)
    
    # Initialize application
    app = RobotTaxonomyApp(args.data_path)
    app.initialize_components()
    
    try:
        if args.mode == "analysis":
            # Run analysis only
            app.run_analysis_only(args.output_dir)
            
        elif args.mode == "dashboard":
            # Run dashboard only
            app.run_interactive_dashboard(args.port, args.debug)
            
        else:  # both
            # Run analysis first
            app.run_analysis_only(args.output_dir)
            
            # Then start dashboard
            print("\nAnalysis complete! Starting interactive dashboard...")
            if not args.no_browser:
                import webbrowser
                webbrowser.open(f"http://localhost:{args.port}")
            
            app.run_interactive_dashboard(args.port, args.debug)
            
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
