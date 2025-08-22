#!/usr/bin/env python3
"""
Separate Phylogenetic Tree Generator
Creates individual, working files for each phylogenetic visualization
"""

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict, Counter
import numpy as np
import os

class SeparatePhylogeneticGenerator:
    def __init__(self, data_path="data/"):
        """Initialize separate phylogenetic generator"""
        self.data_path = data_path
        self.robots_data = self.load_robots_data()
        self.dict_data = self.load_dict_data()
        
    def load_robots_data(self):
        """Load robot data from NDJSON file"""
        robots = []
        try:
            with open(f"{self.data_path}robots.ndjson", 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        robots.append(json.loads(line))
            print(f"Loaded {len(robots)} robots for phylogenetic analysis")
            return robots
        except Exception as e:
            print(f"Error loading robots data: {e}")
            return []
    
    def load_dict_data(self):
        """Load dictionary data for classifications"""
        try:
            with open(f"{self.data_path}dict.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading dictionary data: {e}")
            return {}
    
    def create_sunburst_page(self, output_dir):
        """Create separate Sunburst Phylogenetic Tree page"""
        print("🌞 Creating Sunburst Phylogenetic Tree page...")
        
        # Prepare hierarchical data - simplified for better display
        labels = ["Robot Kingdom"]
        parents = [""]
        values = [len(self.robots_data)]
        
        # Count by domain and class only for cleaner display
        domain_counts = defaultdict(int)
        domain_class_counts = defaultdict(lambda: defaultdict(int))
        
        for robot in self.robots_data:
            domain_id = robot.get('d', -1)
            class_id = robot.get('c', -1)
            
            # Get names safely
            domain_name = 'Unknown Domain'
            if domain_id >= 0 and domain_id < len(self.dict_data.get('domain', [])):
                domain_name = self.dict_data['domain'][domain_id]
            
            class_name = 'Unknown Class'
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_name = self.dict_data['class'][class_id]
            
            # Count occurrences
            domain_counts[domain_name] += 1
            domain_class_counts[domain_name][class_name] += 1
        
        # Add domains
        for domain, count in domain_counts.items():
            labels.append(domain)
            parents.append("Robot Kingdom")
            values.append(count)
        
        # Add classes
        for domain, classes in domain_class_counts.items():
            for class_name, count in classes.items():
                labels.append(class_name)
                parents.append(domain)
                values.append(count)
        
        # Create sunburst chart with clean configuration
        fig = go.Figure()
        
        fig.add_trace(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent:.1f}%<extra></extra>',
            maxdepth=3,
            insidetextorientation='radial'
        ))
        
        fig.update_layout(
            title={
                'text': "Robot Taxonomy Phylogenetic Tree (Sunburst)",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            font_size=14,
            width=900,
            height=900,
            margin=dict(t=80, b=40, l=40, r=40),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        # Use direct write_html for reliability
        fig.write_html(
            f"{output_dir}01_sunburst_phylogenetic.html",
            include_plotlyjs='cdn',
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
            }
        )
        
        print(f"   ✅ Created: {output_dir}01_sunburst_phylogenetic.html")
        return True
    
    def create_treemap_page(self, output_dir):
        """Create separate Treemap page"""
        print("📊 Creating Treemap Phylogenetic Tree page...")
        
        # Prepare data for treemap
        labels = ["Robot Kingdom"]
        parents = [""]
        values = [len(self.robots_data)]
        
        # Count by domain and class
        domain_counts = defaultdict(int)
        domain_class_counts = defaultdict(lambda: defaultdict(int))
        
        for robot in self.robots_data:
            domain_id = robot.get('d', -1)
            class_id = robot.get('c', -1)
            
            domain_name = 'Unknown Domain'
            if domain_id >= 0 and domain_id < len(self.dict_data.get('domain', [])):
                domain_name = self.dict_data['domain'][domain_id]
            
            class_name = 'Unknown Class'
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_name = self.dict_data['class'][class_id]
            
            domain_counts[domain_name] += 1
            domain_class_counts[domain_name][class_name] += 1
        
        # Add domains
        for domain, count in domain_counts.items():
            labels.append(domain)
            parents.append("Robot Kingdom")
            values.append(count)
        
        # Add classes
        for domain, classes in domain_class_counts.items():
            for class_name, count in classes.items():
                labels.append(class_name)
                parents.append(domain)
                values.append(count)
        
        # Create treemap
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent:.1f}%<extra></extra>',
            textinfo="label+value+percent parent",
            pathbar_thickness=20,
            maxdepth=3
        ))
        
        fig.update_layout(
            title={
                'text': "Robot Taxonomy Phylogenetic Tree (Treemap)",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font_size=12,
            width=1200,
            height=800,
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        # Save as standalone HTML
        fig.write_html(f"{output_dir}02_treemap_phylogenetic.html")
        print(f"   ✅ Created: {output_dir}02_treemap_phylogenetic.html")
        
        return True
    
    def create_network_phylogeny_page(self, output_dir):
        """Create separate Network Phylogeny page"""
        print("🕸️ Creating Network Phylogenetic Tree page...")
        
        import networkx as nx
        
        G = nx.DiGraph()
        
        # Color mapping for different levels
        level_colors = {
            'root': '#2E86C1',
            'domain': '#28B463', 
            'class': '#F39C12',
            'role': '#E74C3C'
        }
        
        # Add root node
        G.add_node("Robot Kingdom", level='root', count=len(self.robots_data), color=level_colors['root'])
        
        # Count occurrences
        domain_counts = defaultdict(int)
        domain_class_counts = defaultdict(lambda: defaultdict(int))
        class_role_counts = defaultdict(lambda: defaultdict(int))
        
        for robot in self.robots_data:
            domain_id = robot.get('d', -1)
            class_id = robot.get('c', -1)
            pr_id = robot.get('pr', -1)
            
            # Get names
            domain_name = 'Unknown Domain'
            if domain_id >= 0 and domain_id < len(self.dict_data.get('domain', [])):
                domain_name = self.dict_data['domain'][domain_id]
            
            class_name = 'Unknown Class'
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_name = self.dict_data['class'][class_id]
            
            role_name = 'Unknown Role'
            if pr_id >= 0 and pr_id < len(self.dict_data.get('primary_role', [])):
                role_name = self.dict_data['primary_role'][pr_id]
            
            domain_counts[domain_name] += 1
            domain_class_counts[domain_name][class_name] += 1
            class_role_counts[class_name][role_name] += 1
        
        # Add domain nodes and edges
        for domain, count in domain_counts.items():
            G.add_node(domain, level='domain', count=count, color=level_colors['domain'])
            G.add_edge("Robot Kingdom", domain)
        
        # Add class nodes and edges
        for domain, classes in domain_class_counts.items():
            for class_name, count in classes.items():
                G.add_node(class_name, level='class', count=count, color=level_colors['class'])
                G.add_edge(domain, class_name)
        
        # Add top roles (limit to avoid overcrowding)
        for class_name, roles in class_role_counts.items():
            top_roles = sorted(roles.items(), key=lambda x: x[1], reverse=True)[:2]  # Top 2 roles per class
            for role_name, count in top_roles:
                if count > 2:  # Only roles with more than 2 robots
                    role_node = f"{role_name}"
                    G.add_node(role_node, level='role', count=count, color=level_colors['role'])
                    G.add_edge(class_name, role_node)
        
        # Create network layout
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        
        # Extract node information for plotting
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        node_info = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_size.append(min(G.nodes[node]['count'] + 10, 50))  # Size based on count
            node_color.append(G.nodes[node]['color'])
            node_info.append(f"{node}<br>Count: {G.nodes[node]['count']}")
        
        # Extract edge information
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create the network plot
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle center",
            textfont_size=8,
            hoverinfo='text',
            hovertext=node_info,
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2, color='black'),
                opacity=0.8
            ),
            showlegend=False
        ))
        
        fig.update_layout(
            title={
                'text': "Robot Taxonomy Phylogenetic Network Tree",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=40, l=40, r=40, t=60),
            annotations=[dict(
                text="Node size represents population • Colors show taxonomy levels",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.02,
                xanchor="left", yanchor="bottom",
                font=dict(color="gray", size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=1000,
            height=800,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        # Save as standalone HTML
        fig.write_html(f"{output_dir}05_network_phylogenetic.html")
        print(f"   ✅ Created: {output_dir}05_network_phylogenetic.html")
        
        return True
    
    def create_class_distribution_page(self, output_dir):
        """Create separate Class Distribution page"""
        print("📈 Creating Class Distribution page...")
        
        class_counts = Counter()
        for robot in self.robots_data:
            class_id = robot.get('c', -1)
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_counts[self.dict_data['class'][class_id]] += 1
        
        # Create pie chart
        fig = px.pie(
            values=list(class_counts.values()),
            names=list(class_counts.keys()),
            title="Robot Class Distribution (Phylogenetic Overview)"
        )
        
        fig.update_layout(
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            width=1000,
            height=800,
            font_size=14,
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        # Save as standalone HTML
        fig.write_html(f"{output_dir}03_class_distribution.html")
        print(f"   ✅ Created: {output_dir}03_class_distribution.html")
        
        return True
    
    def create_timeline_page(self, output_dir):
        """Create separate Timeline page"""
        print("⏰ Creating Evolutionary Timeline page...")
        
        timeline_data = []
        
        for robot in self.robots_data:
            year = robot.get('yr')
            if year is not None and year > 0:
                domain_id = robot.get('d', -1)
                class_id = robot.get('c', -1)
                
                domain_name = 'Unknown'
                if domain_id >= 0 and domain_id < len(self.dict_data.get('domain', [])):
                    domain_name = self.dict_data['domain'][domain_id]
                
                class_name = 'Unknown'
                if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                    class_name = self.dict_data['class'][class_id]
                
                timeline_data.append({
                    'year': year,
                    'name': robot['n'],
                    'domain': domain_name,
                    'class': class_name,
                    'id': robot['id']
                })
        
        if not timeline_data:
            print("   ⚠️ No timeline data available")
            return False
        
        df = pd.DataFrame(timeline_data)
        
        fig = px.scatter(
            df, 
            x='year', 
            y='class',
            color='domain',
            size_max=20,
            hover_data=['name'],
            title="Robot Evolution Timeline - Phylogenetic Development"
        )
        
        fig.update_layout(
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            xaxis_title="Year",
            yaxis_title="Robot Class (Taxonomic)",
            width=1200,
            height=800,
            font_size=12,
            margin=dict(t=80, b=60, l=60, r=40)
        )
        
        # Save as standalone HTML
        fig.write_html(f"{output_dir}04_evolutionary_timeline.html")
        print(f"   ✅ Created: {output_dir}04_evolutionary_timeline.html")
        
        return True
    
    def create_navigation_index(self, output_dir):
        """Create navigation index page"""
        print("🏠 Creating Navigation Index page...")
        
        # Generate basic statistics
        domains = set()
        classes = set()
        for robot in self.robots_data:
            domain_id = robot.get('d', -1)
            class_id = robot.get('c', -1)
            
            if domain_id >= 0 and domain_id < len(self.dict_data.get('domain', [])):
                domains.add(self.dict_data['domain'][domain_id])
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                classes.add(self.dict_data['class'][class_id])
        
        # Calculate diversity
        class_counts = Counter()
        for robot in self.robots_data:
            class_id = robot.get('c', -1)
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_counts[self.dict_data['class'][class_id]] += 1
        
        total = sum(class_counts.values())
        shannon_diversity = 0
        if total > 0:
            shannon_diversity = -sum((count/total) * np.log(count/total) for count in class_counts.values() if count > 0)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Phylogenetic Tree Analysis - Navigation</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 3em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            margin: 20px 0 0 0;
            opacity: 0.9;
            font-size: 1.3em;
        }}
        .content {{
            padding: 50px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin: 50px 0;
        }}
        .nav-card {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-decoration: none;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }}
        .nav-card:hover {{
            transform: translateY(-5px);
            text-decoration: none;
            color: white;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }}
        .nav-card h3 {{
            margin: 0 0 15px 0;
            font-size: 1.5em;
        }}
        .nav-card p {{
            margin: 0;
            opacity: 0.9;
            font-size: 1em;
            line-height: 1.5;
        }}
        .nav-icon {{
            font-size: 2.5em;
            margin-bottom: 15px;
            display: block;
        }}
        .methodology {{
            background: linear-gradient(135deg, #f1f2f6 0%, #e8eaf6 100%);
            border-left: 5px solid #3498db;
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
        }}
        .methodology h3 {{
            color: #3498db;
            margin-top: 0;
            font-size: 1.5em;
        }}
        @media (max-width: 768px) {{
            .nav-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .header h1 {{ font-size: 2em; }}
            .content {{ padding: 30px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌳 Robot Phylogenetic Tree Analysis</h1>
            <p>Comprehensive Evolutionary Relationships and Taxonomic Diversity</p>
            <p><strong>Linnaean-inspired Robot Taxonomy V2 Framework</strong></p>
        </div>
        
        <div class="content">
            <!-- Summary Statistics -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(self.robots_data):,}</div>
                    <div class="stat-label">Total Robot Species</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(domains)}</div>
                    <div class="stat-label">Taxonomic Domains</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(classes)}</div>
                    <div class="stat-label">Robot Classes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{shannon_diversity:.3f}</div>
                    <div class="stat-label">Shannon Diversity Index</div>
                </div>
            </div>
            
            <!-- Navigation to Individual Visualizations -->
            <h2 style="color: #2c3e50; font-size: 2.2em; text-align: center; margin: 50px 0 30px 0;">🔍 Explore Phylogenetic Visualizations</h2>
            
            <div class="nav-grid">
                <a href="01_sunburst_phylogenetic.html" class="nav-card">
                    <span class="nav-icon">🌞</span>
                    <h3>Sunburst Phylogenetic Tree</h3>
                    <p>Interactive hierarchical circular tree showing Domain → Class → Role relationships with nested taxonomic levels</p>
                </a>
                
                <a href="02_treemap_phylogenetic.html" class="nav-card">
                    <span class="nav-icon">📊</span>
                    <h3>Treemap Phylogeny</h3>
                    <p>Area-proportional visualization where size represents population size of taxonomic groups</p>
                </a>
                
                <a href="03_class_distribution.html" class="nav-card">
                    <span class="nav-icon">📈</span>
                    <h3>Class Distribution</h3>
                    <p>Pie chart overview showing relative sizes and percentages of different robot classes</p>
                </a>
                
                <a href="04_evolutionary_timeline.html" class="nav-card">
                    <span class="nav-icon">⏰</span>
                    <h3>Evolutionary Timeline</h3>
                    <p>Temporal development of robot classes over time showing evolutionary patterns</p>
                </a>
                
                <a href="05_network_phylogenetic.html" class="nav-card">
                    <span class="nav-icon">🕸️</span>
                    <h3>Network Phylogeny</h3>
                    <p>Network-based visualization showing evolutionary relationships and taxonomic connections</p>
                </a>
            </div>
            
            <!-- Methodology -->
            <div class="methodology">
                <h3>📋 Methodology & Framework</h3>
                <p><strong>Taxonomic Framework:</strong> Based on Linnaean-inspired Robot Taxonomy V2, representing evolutionary relationships through morphological and functional characteristics.</p>
                <p><strong>Hierarchical Structure:</strong> Domain → Class → Order → Primary Role</p>
                <p><strong>Data Coverage:</strong> {len(self.robots_data):,} robot species across {len(domains)} domains and {len(classes)} classes</p>
                <p><strong>Diversity Metrics:</strong> Shannon diversity index: {shannon_diversity:.3f} - measures taxonomic richness and evenness</p>
                <p><strong>Visualization Methods:</strong> Each page contains a dedicated, optimized visualization for detailed exploration of specific phylogenetic aspects.</p>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 40px; background: #f8f9fa; border-radius: 15px; margin-top: 50px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">🌳 Individual Phylogenetic Analysis Pages</h3>
                <p style="color: #7f8c8d; margin: 10px 0;">Each visualization is now on a separate page for optimal performance and clarity</p>
                <p style="color: #7f8c8d; font-size: 0.9em;">All visualizations are interactive - hover, zoom, and explore the robot kingdom!</p>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        # Save navigation index
        with open(f"{output_dir}00_phylogenetic_index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ Created: {output_dir}00_phylogenetic_index.html")
        return True
    
    def generate_all_separate_pages(self, output_dir="phylogenetic_trees/"):
        """Generate all separate phylogenetic pages"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🌳 Separate Phylogenetic Tree Generator")
        print("=" * 60)
        
        try:
            # Create individual pages
            success_count = 0
            
            if self.create_sunburst_page(output_dir):
                success_count += 1
            
            if self.create_treemap_page(output_dir):
                success_count += 1
            
            if self.create_class_distribution_page(output_dir):
                success_count += 1
            
            if self.create_timeline_page(output_dir):
                success_count += 1
            
            if self.create_network_phylogeny_page(output_dir):
                success_count += 1
            
            if self.create_navigation_index(output_dir):
                success_count += 1
            
            if success_count >= 5:  # At least 5 main visualizations
                print(f"\n🎉 SUCCESS! Created {success_count} separate phylogenetic pages!")
                print(f"📁 Start with: {output_dir}00_phylogenetic_index.html")
                return output_dir
            else:
                print(f"\n⚠️ Only {success_count} pages created successfully.")
                return None
                
        except Exception as e:
            print(f"\n❌ Error generating separate pages: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main function to generate separate phylogenetic pages"""
    print("🔧 Separate Phylogenetic Tree Generator")
    print("=" * 60)
    
    try:
        generator = SeparatePhylogeneticGenerator()
        output_dir = generator.generate_all_separate_pages()
        
        if output_dir:
            print(f"\n✅ All separate phylogenetic pages created successfully!")
            print(f"🌟 Navigation: {output_dir}00_phylogenetic_index.html")
        else:
            print(f"\n💥 Failed to generate separate pages.")
            
        return output_dir is not None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
