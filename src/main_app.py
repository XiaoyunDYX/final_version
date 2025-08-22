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
        
        # 3. Generate advanced visualizations
        print("3. Creating advanced visualizations...")
        advanced_viz = self.processor.create_advanced_visualizations()
        
        # Save advanced visualizations
        for viz_name, fig in advanced_viz.items():
            if hasattr(fig, 'write_html'):
                fig.write_html(f"{output_dir}{viz_name}.html")
                try:
                    fig.write_image(f"{output_dir}{viz_name}.png", width=1200, height=800)
                except Exception as e:
                    print(f"Could not save {viz_name} as PNG: {e}")
        
        # 4. Generate standard visualizations
        print("4. Creating standard visualizations...")
        self.visualizer.save_static_visualizations(f"{output_dir}standard_viz/")
        
        # 5. Generate summary report
        print("5. Generating summary report...")
        self.generate_summary_report(insights, f"{output_dir}summary_report.md")
        
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
