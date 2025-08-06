# Robot Taxonomy Agent

A comprehensive tool for scraping, classifying, and visualizing robot data according to a hierarchical taxonomy system. This project creates a "tree of life" for robots, similar to biological taxonomy.

## 🌟 Features

- **Web Scraping**: Automatically collects robot information from the internet
- **Intelligent Classification**: Classifies robots using rule-based taxonomy matching
- **Interactive Visualization**: Creates interactive dashboards and static visualizations
- **Modular Architecture**: Separate components for scraping, classification, and visualization
- **Multiple Output Formats**: PNG images, interactive dashboards, and JSON data

## 📁 Project Structure

```
robots_agent/
├── src/                          # Main application source
│   └── main.py                   # Main application entry point
├── web_scraper/                  # Web scraping components
│   └── robot_scraper.py          # Robot data scraper
├── classifier/                   # Classification components
│   └── robot_classifier.py       # Rule-based robot classifier
├── visualizer/                   # Visualization components
│   └── robot_tree_visualizer.py  # Interactive tree visualizer
├── utils/                        # Utility scripts
│   ├── analyze_robots.py         # Robot data analysis
│   ├── analyze_radial_tree.py    # Radial tree analysis
│   └── filter_robots.py          # Data filtering utilities
├── scripts/                      # Standalone scripts
│   └── gptclassifier.py          # GPT-based classifier (standalone)
├── data/                         # Data storage
│   ├── robots_data.json          # Raw scraped robot data
│   ├── classified_robots.json    # Classified robot data
│   └── *.png                     # Generated visualizations
├── requirements.txt              # Python dependencies
├── robot_taxonomy_framework.md   # Taxonomy framework documentation
└── README.md                     # This file
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd robots_agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional, for GPT classifier):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 📖 Usage

### Main Application

The main application provides a complete pipeline for robot taxonomy analysis:

```bash
# Run the complete pipeline (scrape → classify → visualize)
python src/main.py

# Run only web scraping
python src/main.py --mode scraper

# Run only classification
python src/main.py --mode classifier

# Run only visualization
python src/main.py --mode visualizer

# Run without launching the dashboard
python src/main.py --no-dashboard

# Use custom search terms
python src/main.py --search-terms "industrial robots" "medical robots"
```

### Standalone Scripts

#### GPT Classifier
```bash
# Run GPT-based classification (requires OpenAI API key)
python scripts/gptclassifier.py
```

#### Data Analysis
```bash
# Analyze robot data
python utils/analyze_robots.py

# Analyze radial tree structure
python utils/analyze_radial_tree.py
```

#### Data Filtering
```bash
# Filter robot data
python utils/filter_robots.py input.json output.json
```

## 🔧 Configuration

### Taxonomy Framework

The project uses a hierarchical taxonomy system with 8 levels:

1. **Domain**: Operational environment (Physical, Virtual, Hybrid)
2. **Kingdom**: Application domains (Industrial, Medical, Service, etc.)
3. **Phylum**: Morphological structure (Manipulator, Mobile, Humanoid, etc.)
4. **Class**: Locomotion mechanism (Static, Wheeled, Legged, etc.)
5. **Order**: Autonomy and control (Teleoperated, Autonomous, etc.)
6. **Family**: Sensing modalities (Vision-Based, LiDAR-Based, etc.)
7. **Genus**: Actuation systems (Electric, Hydraulic, etc.)
8. **Species**: Application specialization (Surgery, Inspection, etc.)

### Customization

- Modify `robot_taxonomy_framework.md` to adjust the taxonomy structure
- Update `classifier/robot_classifier.py` to change classification rules
- Customize visualizations in `visualizer/robot_tree_visualizer.py`

## 📊 Output

The application generates several types of output:

### Data Files
- `data/robots_data.json`: Raw scraped robot data
- `data/classified_robots.json`: Classified robot data with taxonomy

### Visualizations
- `robot_radial_tree.png`: Radial tree visualization
- `robot_phylogenetic_tree.png`: Phylogenetic tree
- `robot_dendrogram.png`: Hierarchical dendrogram
- `robot_clusters.png`: Clustering visualization
- `robot_taxonomy_bars.png`: Bar chart distributions
- `robot_simplified_tree.png`: Simplified tree view
- `robot_taxonomy_summary.png`: Summary statistics

### Interactive Dashboard
- Web-based interactive visualization at `http://localhost:8050`
- Filterable tree view with robot details
- Real-time statistics and analysis

## 🛠️ Development

### Adding New Robot Types

1. Update the taxonomy framework in `robot_taxonomy_framework.md`
2. Add classification rules in `classifier/robot_classifier.py`
3. Update visualization logic in `visualizer/robot_tree_visualizer.py`

### Extending Functionality

- **New Scrapers**: Add to `web_scraper/` directory
- **New Classifiers**: Add to `classifier/` directory
- **New Visualizations**: Add to `visualizer/` directory
- **New Analysis Tools**: Add to `utils/` directory

## 📝 Dependencies

- **Web Scraping**: `requests`, `beautifulsoup4`, `selenium`
- **Data Processing**: `pandas`, `numpy`, `scikit-learn`
- **Visualization**: `plotly`, `dash`, `networkx`, `matplotlib`
- **AI/ML**: `openai` (for GPT classifier)
- **Utilities**: `python-dotenv`, `fake-useragent`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by biological taxonomy systems
- Uses modern web scraping and data visualization techniques
- Leverages AI/ML for intelligent classification

## 📞 Support

For questions or issues, please open an issue on the GitHub repository. 