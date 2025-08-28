#!/usr/bin/env python3
"""
Enhanced Robot Taxonomy Visualizer
Enhanced visualization system based on new Linnaean-inspired classification framework
Supports timeline analysis, regional distribution, and interactive exploration
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import dash
from dash import dcc, html, Input, Output, callback
import networkx as nx
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
import colorcet as cc

class EnhancedRobotVisualizer:
    def __init__(self, data_path="data/"):
        """Initialize enhanced visualizer"""
        self.data_path = data_path
        self.robots_data = self.load_robots_data()
        self.features_data = self.load_features_data()
        self.dict_data = self.load_dict_data()
        self.family_index = self.load_family_index()
        self.path_counts = self.load_path_counts()
        
        # Create mapping dictionaries
        self.create_mappings()
        
        # Color schemes
        self.color_schemes = {
            'domain': ['#1f77b4', '#ff7f0e', '#2ca02c'],
            'class': cc.glasbey_light[:8],
            'region': cc.glasbey_dark[:20],
            'sector': cc.rainbow[:15]
        }

    def load_robots_data(self):
        """Load robot data"""
        robots = []
        try:
            with open(f"{self.data_path}robots.ndjson", 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        robots.append(json.loads(line))
            print(f"Successfully loaded {len(robots)} robot records")
            return robots
        except Exception as e:
            print(f"Failed to load robot data: {e}")
            return []

    def load_features_data(self):
        """Load features data"""
        try:
            with open(f"{self.data_path}features.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load features data: {e}")
            return {}

    def load_dict_data(self):
        """Load dictionary data"""
        try:
            with open(f"{self.data_path}dict.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load dictionary data: {e}")
            return {}

    def load_family_index(self):
        """Load family index"""
        try:
            with open(f"{self.data_path}family_index.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load family index: {e}")
            return {}

    def load_path_counts(self):
        """Load path counts"""
        try:
            with open(f"{self.data_path}path_counts.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load path counts: {e}")
            return {}

    def create_mappings(self):
        """Create various mapping dictionaries"""
        # Create ID to robot mapping
        self.id_to_robot = {robot['id']: robot for robot in self.robots_data}
        
        # Create feature index mapping
        if 'features' in self.features_data:
            self.id_to_features = {item['id']: item for item in self.features_data['features']}
        else:
            self.id_to_features = {}
        
        # Create vocabulary mapping
        self.vocab = self.features_data.get('vocab', [])
        
        # Create region mapping (extended region codes)
        self.region_mapping = {
            'US': 'United States', 'JP': 'Japan', 'DE': 'Germany', 'SE': 'Sweden',
            'CN': 'China', 'UK': 'United Kingdom', 'FR': 'France', 'IT': 'Italy',
            'CA': 'Canada', 'DK': 'Denmark', 'CH': 'Switzerland', 'ES': 'Spain',
            'IL': 'Israel', 'AU': 'Australia', 'KR': 'South Korea', 'IN': 'India',
            'UN': 'Unknown/International', 'EU': 'European Union', 'ZA': 'South Africa',
            'LE': 'Lebanon', 'TW': 'Taiwan', 'PA': 'Pakistan', 'IR': 'Iran',
            'PL': 'Poland', 'BE': 'Belgium', 'PE': 'Peru', 'JA': 'Japan (Alt)',
            'SW': 'Sweden (Alt)'
        }

    def create_timeline_visualization(self):
        """Create timeline visualization"""
        # Prepare timeline data
        timeline_data = []
        for robot in self.robots_data:
            if robot.get('yr') and robot.get('yr') > 0:
                timeline_data.append({
                    'id': robot['id'],
                    'name': robot['n'],
                    'year': robot['yr'],
                    'region': self.region_mapping.get(robot['rg'], robot['rg']),
                    'domain': self.dict_data['domain'][robot['d']] if robot['d'] < len(self.dict_data['domain']) else 'Unknown',
                    'class': self.dict_data['class'][robot['c']] if robot['c'] < len(self.dict_data['class']) else 'Unknown',
                    'sector': robot.get('tags', {}).get('sector', ['Unknown'])[0] if robot.get('tags', {}).get('sector') else 'Unknown'
                })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        # Create timeline charts
        fig_timeline = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Robot Development Timeline - By Category', 'Robot Development Timeline - By Region', 'Robot Development Timeline - By Sector'),
            vertical_spacing=0.08,
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Timeline by category
        class_counts = df_timeline.groupby(['year', 'class']).size().reset_index(name='count')
        for i, cls in enumerate(df_timeline['class'].unique()):
            cls_data = class_counts[class_counts['class'] == cls]
            fig_timeline.add_trace(
                go.Scatter(
                    x=cls_data['year'], 
                    y=cls_data['count'],
                    mode='lines+markers',
                    name=str(cls),
                    line=dict(color=self.color_schemes['class'][i % len(self.color_schemes['class'])]),
                    stackgroup='one'
                ),
                row=1, col=1
            )
        
        # Timeline by region
        region_counts = df_timeline.groupby(['year', 'region']).size().reset_index(name='count')
        top_regions = df_timeline['region'].value_counts().head(10).index
        for i, region in enumerate(top_regions):
            region_data = region_counts[region_counts['region'] == region]
            fig_timeline.add_trace(
                go.Scatter(
                    x=region_data['year'], 
                    y=region_data['count'],
                    mode='lines+markers',
                    name=str(region),
                    line=dict(color=self.color_schemes['region'][i % len(self.color_schemes['region'])]),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # Timeline by sector
        sector_counts = df_timeline.groupby(['year', 'sector']).size().reset_index(name='count')
        for i, sector in enumerate(df_timeline['sector'].unique()):
            sector_data = sector_counts[sector_counts['sector'] == sector]
            fig_timeline.add_trace(
                go.Scatter(
                    x=sector_data['year'], 
                    y=sector_data['count'],
                    mode='lines+markers',
                    name=str(sector),
                    line=dict(color=self.color_schemes['sector'][i % len(self.color_schemes['sector'])]),
                    showlegend=False
                ),
                row=3, col=1
            )
        
        fig_timeline.update_layout(
            title="Robot Technology Development Timeline Analysis",
            height=1200,
            showlegend=True
        )
        
        return fig_timeline

    def create_regional_distribution(self):
        """Create regional distribution visualization"""
        # Statistical regional distribution
        region_stats = defaultdict(lambda: {'count': 0, 'classes': Counter(), 'sectors': Counter()})
        
        for robot in self.robots_data:
            region = self.region_mapping.get(robot['rg'], robot['rg'])
            region_stats[region]['count'] += 1
            
            if robot['c'] < len(self.dict_data['class']):
                cls = self.dict_data['class'][robot['c']]
                region_stats[region]['classes'][cls] += 1
            
            if robot.get('tags', {}).get('sector'):
                sector = robot['tags']['sector'][0]
                region_stats[region]['sectors'][sector] += 1
        
        # Create regional distribution map
        regions = list(region_stats.keys())
        counts = [region_stats[r]['count'] for r in regions]
        
        # World map
        fig_map = go.Figure(data=go.Choropleth(
            locations=[r for r in regions if r in ['United States', 'Japan', 'Germany', 'Sweden', 'China', 'United Kingdom', 'France', 'Italy', 'Canada', 'Denmark', 'Switzerland', 'Spain']],
            z=[region_stats[r]['count'] for r in regions if r in ['United States', 'Japan', 'Germany', 'Sweden', 'China', 'United Kingdom', 'France', 'Italy', 'Canada', 'Denmark', 'Switzerland', 'Spain']],
            locationmode='country names',
            colorscale='Viridis',
            text=[f"{r}: {region_stats[r]['count']} robots" for r in regions if r in ['United States', 'Japan', 'Germany', 'Sweden', 'China', 'United Kingdom', 'France', 'Italy', 'Canada', 'Denmark', 'Switzerland', 'Spain']],
            colorbar_title="Number of Robots"
        ))
        
        fig_map.update_layout(
            title="Global Robot Technology Distribution Map",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            )
        )
        
        # Regional bar chart
        fig_bar = px.bar(
            x=regions[:15], 
            y=[region_stats[r]['count'] for r in regions[:15]],
            title="Robot Distribution by Major Regions",
            labels={'x': 'Region', 'y': 'Number of Robots'},
            color=[region_stats[r]['count'] for r in regions[:15]],
            color_continuous_scale='viridis'
        )
        
        return fig_map, fig_bar

    def create_taxonomy_sunburst(self):
        """Create taxonomy sunburst chart"""
        # Prepare sunburst data
        sunburst_data = []
        
        for robot in self.robots_data:
            domain = self.dict_data['domain'][robot['d']] if robot['d'] < len(self.dict_data['domain']) else 'Unknown'
            cls = self.dict_data['class'][robot['c']] if robot['c'] < len(self.dict_data['class']) else 'Unknown'
            
            # Get order information
            order = 'Unknown'
            if cls in self.dict_data.get('order_by_class', {}):
                orders = self.dict_data['order_by_class'][cls]
                if robot['o'] < len(orders):
                    order = orders[robot['o']]
            
            # Get sector information
            sector = 'Unknown'
            if robot.get('tags', {}).get('sector'):
                sector = robot['tags']['sector'][0]
            
            sunburst_data.append({
                'ids': f"{domain}-{cls}-{order}-{sector}",
                'labels': sector,
                'parents': f"{domain}-{cls}-{order}",
                'values': 1
            })
            
            sunburst_data.append({
                'ids': f"{domain}-{cls}-{order}",
                'labels': order,
                'parents': f"{domain}-{cls}",
                'values': 1
            })
            
            sunburst_data.append({
                'ids': f"{domain}-{cls}",
                'labels': cls,
                'parents': domain,
                'values': 1
            })
            
            sunburst_data.append({
                'ids': domain,
                'labels': domain,
                'parents': "",
                'values': 1
            })
        
        # Merge duplicates and calculate actual values
        merged_data = defaultdict(int)
        labels_map = {}
        parents_map = {}
        
        for item in sunburst_data:
            merged_data[item['ids']] += item['values']
            labels_map[item['ids']] = item['labels']
            parents_map[item['ids']] = item['parents']
        
        # Create sunburst chart
        fig_sunburst = go.Figure(go.Sunburst(
            ids=list(merged_data.keys()),
            labels=[labels_map[k] for k in merged_data.keys()],
            parents=[parents_map[k] for k in merged_data.keys()],
            values=list(merged_data.values()),
            branchvalues="total",
        ))
        
        fig_sunburst.update_layout(
            title="Robot Taxonomy Sunburst Chart",
            font_size=12,
            height=800
        )
        
        return fig_sunburst

    def create_network_graph(self):
        """Create network graph showing robot relationships"""
        G = nx.Graph()
        
        # Add nodes and edges
        for robot in self.robots_data:
            robot_id = str(robot['id'])
            domain = self.dict_data['domain'][robot['d']] if robot['d'] < len(self.dict_data['domain']) else 'Unknown'
            cls = self.dict_data['class'][robot['c']] if robot['c'] < len(self.dict_data['class']) else 'Unknown'
            
            # Add robot node
            G.add_node(robot_id, 
                      type='robot',
                      name=robot['n'],
                      domain=domain,
                      robot_class=cls,
                      year=robot.get('yr', 0),
                      region=robot.get('rg', 'UN'))
            
            # Add classification nodes
            domain_node = f"domain_{domain}"
            class_node = f"class_{cls}"
            
            if not G.has_node(domain_node):
                G.add_node(domain_node, type='domain', name=domain)
            if not G.has_node(class_node):
                G.add_node(class_node, type='class', name=cls)
            
            # Add edges
            G.add_edge(robot_id, class_node)
            G.add_edge(class_node, domain_node)
        
        # Use spring layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Prepare plotting data
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create edge traces
        edge_trace = go.Scatter(x=edge_x, y=edge_y,
                               line=dict(width=0.5, color='#888'),
                               hoverinfo='none',
                               mode='lines')
        
        # Create node traces
        node_traces = []
        for node_type in ['domain', 'class', 'robot']:
            nodes = [n for n in G.nodes() if G.nodes[n]['type'] == node_type]
            if not nodes:
                continue
                
            node_x = [pos[node][0] for node in nodes]
            node_y = [pos[node][1] for node in nodes]
            
            node_trace = go.Scatter(x=node_x, y=node_y,
                                   mode='markers',
                                   hoverinfo='text',
                                   name=node_type,
                                   text=[G.nodes[node]['name'] for node in nodes],
                                   marker=dict(size=10 if node_type == 'robot' else 20,
                                             color=px.colors.qualitative.Set1[['domain', 'class', 'robot'].index(node_type)]))
            node_traces.append(node_trace)
        
        # Create figure
        fig_network = go.Figure(data=[edge_trace] + node_traces,
                               layout=go.Layout(
                                   title='Robot Classification Network Graph',
                                   titlefont_size=16,
                                   showlegend=True,
                                   hovermode='closest',
                                   margin=dict(b=20,l=5,r=5,t=40),
                                   annotations=[ dict(
                                       text="Node size indicates importance, color indicates type",
                                       showarrow=False,
                                       xref="paper", yref="paper",
                                       x=0.005, y=-0.002,
                                       xanchor='left', yanchor='bottom',
                                       font=dict(color='#888', size=12)
                                   )],
                                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        return fig_network

    def create_feature_analysis(self):
        """Create feature analysis charts"""
        # Feature statistics
        feature_stats = Counter()
        
        for robot_id, features in self.id_to_features.items():
            feat_indices = features.get('feat', [])
            for idx in feat_indices:
                if idx < len(self.vocab):
                    feature_stats[self.vocab[idx]] += 1
        
        # Create feature distribution chart
        features = list(feature_stats.keys())[:20]  # Take top 20 features
        counts = [feature_stats[f] for f in features]
        
        fig_features = px.bar(
            x=counts,
            y=features,
            orientation='h',
            title="Robot Morphological Feature Distribution (Top 20)",
            labels={'x': 'Number of Robots', 'y': 'Morphological Features'},
            color=counts,
            color_continuous_scale='viridis'
        )
        
        fig_features.update_layout(height=600)
        
        return fig_features

    def create_dashboard(self):
        """Create interactive dashboard"""
        app = dash.Dash(__name__)
        
        # Create various charts
        fig_timeline = self.create_timeline_visualization()
        fig_map, fig_bar = self.create_regional_distribution()
        fig_sunburst = self.create_taxonomy_sunburst()
        fig_network = self.create_network_graph()
        fig_features = self.create_feature_analysis()
        
        app.layout = html.Div([
            html.H1("Robot Taxonomy Visualization Analysis Dashboard", 
                   style={'textAlign': 'center', 'marginBottom': 30}),
            
            # Control panel
            html.Div([
                html.Div([
                    html.Label("Select Domain:"),
                    dcc.Dropdown(
                        id='domain-dropdown',
                        options=[{'label': d, 'value': i} for i, d in enumerate(self.dict_data['domain'])],
                        value=None,
                        multi=True
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Select Class:"),
                    dcc.Dropdown(
                        id='class-dropdown',
                        options=[{'label': c, 'value': i} for i, c in enumerate(self.dict_data['class'])],
                        value=None,
                        multi=True
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Year Range:"),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=1960,
                        max=2025,
                        step=1,
                        value=[1960, 2025],
                        marks={i: str(i) for i in range(1960, 2026, 10)}
                    )
                ], style={'width': '35%', 'display': 'inline-block'})
            ], style={'marginBottom': 30}),
            
            # Chart area
            dcc.Tabs([
                dcc.Tab(label='Timeline Analysis', children=[
                    dcc.Graph(figure=fig_timeline)
                ]),
                
                dcc.Tab(label='Regional Distribution', children=[
                    html.Div([
                        dcc.Graph(figure=fig_map, style={'width': '60%', 'display': 'inline-block'}),
                        dcc.Graph(figure=fig_bar, style={'width': '40%', 'display': 'inline-block'})
                    ])
                ]),
                
                dcc.Tab(label='Taxonomy System', children=[
                    html.Div([
                        dcc.Graph(figure=fig_sunburst, style={'width': '50%', 'display': 'inline-block'}),
                        dcc.Graph(figure=fig_network, style={'width': '50%', 'display': 'inline-block'})
                    ])
                ]),
                
                dcc.Tab(label='Feature Analysis', children=[
                    dcc.Graph(figure=fig_features)
                ]),
                
                dcc.Tab(label='Statistical Overview', children=[
                    html.Div([
                        html.H3("Data Statistics Overview"),
                        html.P(f"Total Robots: {len(self.robots_data)}"),
                        html.P(f"Year Range: {min([r.get('yr', 2000) for r in self.robots_data if r.get('yr', 0) > 0])}-{max([r.get('yr', 2000) for r in self.robots_data if r.get('yr', 0) > 0])}"),
                        html.P(f"Regions Covered: {len(set([r['rg'] for r in self.robots_data]))}"),
                        html.P(f"Robot Categories: {len(self.dict_data['class'])}"),
                        html.P(f"Application Sectors: {len(self.dict_data['sector'])}")
                    ])
                ])
            ])
        ])
        
        return app

    def save_static_visualizations(self, output_dir="outputs/figures/"):
        """Save static visualization charts as PNG images only"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Create and save various charts as PNG only
        print("Generating PNG visualization charts...")
        
        try:
            # Timeline chart
            print("Creating timeline visualization...")
            fig_timeline = self.create_timeline_visualization()
            fig_timeline.update_layout(
                title="Robot Technology Development Timeline Analysis",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_timeline.write_image(f"{output_dir}03_timeline.png", 
                                   width=1600, height=1200, scale=2, 
                                   engine="kaleido")
            print("✅ Timeline visualization saved")
            
            # Regional distribution charts
            print("Creating regional distribution visualizations...")
            fig_map, fig_bar = self.create_regional_distribution()
            
            # World map
            fig_map.update_layout(
                title="Global Robot Technology Distribution Map",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_map.write_image(f"{output_dir}01_regional_map.png", 
                              width=1600, height=1000, scale=2,
                              engine="kaleido")
            
            # Regional bar chart
            fig_bar.update_layout(
                title="Robot Distribution by Major Regions",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_bar.write_image(f"{output_dir}02_regional_distribution.png", 
                              width=1600, height=800, scale=2,
                              engine="kaleido")
            print("✅ Regional distribution visualizations saved")
            
            # Taxonomy sunburst chart
            print("Creating taxonomy sunburst visualization...")
            fig_sunburst = self.create_taxonomy_sunburst()
            fig_sunburst.update_layout(
                title="Robot Taxonomy Sunburst Chart",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_sunburst.write_image(f"{output_dir}04_taxonomy_sunburst.png", 
                                   width=1200, height=1200, scale=2,
                                   engine="kaleido")
            print("✅ Taxonomy sunburst visualization saved")
            
            # Network graph
            print("Creating network graph visualization...")
            fig_network = self.create_network_graph()
            fig_network.update_layout(
                title="Robot Classification Network Graph",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_network.write_image(f"{output_dir}05_network_graph.png", 
                                  width=1600, height=1200, scale=2,
                                  engine="kaleido")
            print("✅ Network graph visualization saved")
            
            # Feature analysis chart
            print("Creating feature analysis visualization...")
            fig_features = self.create_feature_analysis()
            fig_features.update_layout(
                title="Robot Morphological Feature Distribution (Top 20)",
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_features.write_image(f"{output_dir}06_feature_analysis.png", 
                                   width=1600, height=1000, scale=2,
                                   engine="kaleido")
            print("✅ Feature analysis visualization saved")
            
        except Exception as e:
            print(f"Error creating PNG visualizations with Plotly: {e}")
            print("Attempting fallback to Matplotlib...")
            self._create_matplotlib_fallbacks(output_dir)
        
        print(f"All visualization charts saved as PNG to {output_dir} directory")

    def _create_matplotlib_fallbacks(self, output_dir):
        """Create matplotlib fallback visualizations"""
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from collections import Counter
        
        print("Creating matplotlib fallback visualizations...")
        
        # Set style
        plt.style.use('default')
        
        try:
            # 1. Regional distribution bar chart
            region_counts = Counter()
            for robot in self.robots_data:
                region = self.region_mapping.get(robot['rg'], robot['rg'])
                region_counts[region] += 1
            
            top_regions = dict(region_counts.most_common(15))
            
            plt.figure(figsize=(16, 10))
            bars = plt.bar(range(len(top_regions)), list(top_regions.values()))
            plt.title('Robot Distribution by Major Regions', fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('Region', fontsize=14)
            plt.ylabel('Number of Robots', fontsize=14)
            plt.xticks(range(len(top_regions)), list(top_regions.keys()), rotation=45, ha='right')
            
            # Color bars
            colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}02_regional_distribution.png", dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            print("✅ Regional distribution fallback saved")
            
            # 2. Class distribution pie chart
            class_counts = Counter()
            for robot in self.robots_data:
                if robot['c'] < len(self.dict_data['class']):
                    class_counts[self.dict_data['class'][robot['c']]] += 1
            
            plt.figure(figsize=(12, 12))
            plt.pie(list(class_counts.values()), labels=list(class_counts.keys()), 
                   autopct='%1.1f%%', startangle=90)
            plt.title('Robot Class Distribution', fontsize=20, fontweight='bold', pad=20)
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig(f"{output_dir}04_taxonomy_sunburst.png", dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            print("✅ Class distribution fallback saved")
            
            # 3. Timeline analysis
            timeline_data = []
            for robot in self.robots_data:
                if robot.get('yr') and robot.get('yr') > 0:
                    timeline_data.append({
                        'year': robot['yr'],
                        'class': self.dict_data['class'][robot['c']] if robot['c'] < len(self.dict_data['class']) else 'Unknown'
                    })
            
            if timeline_data:
                df_timeline = pd.DataFrame(timeline_data)
                year_counts = df_timeline.groupby('year').size()
                
                plt.figure(figsize=(16, 8))
                plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, markersize=6)
                plt.title('Robot Development Timeline', fontsize=20, fontweight='bold', pad=20)
                plt.xlabel('Year', fontsize=14)
                plt.ylabel('Number of Robots Developed', fontsize=14)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(f"{output_dir}03_timeline.png", dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                plt.close()
                print("✅ Timeline fallback saved")
            
            # 4. Feature analysis (if available)
            if self.id_to_features and self.vocab:
                feature_stats = Counter()
                for robot_id, features in self.id_to_features.items():
                    feat_indices = features.get('feat', [])
                    for idx in feat_indices:
                        if idx < len(self.vocab):
                            feature_stats[self.vocab[idx]] += 1
                
                top_features = dict(feature_stats.most_common(20))
                
                plt.figure(figsize=(16, 10))
                bars = plt.barh(range(len(top_features)), list(top_features.values()))
                plt.title('Robot Morphological Feature Distribution (Top 20)', 
                         fontsize=20, fontweight='bold', pad=20)
                plt.xlabel('Number of Robots', fontsize=14)
                plt.ylabel('Morphological Features', fontsize=14)
                plt.yticks(range(len(top_features)), list(top_features.keys()))
                
                # Color bars
                colors = plt.cm.plasma(np.linspace(0, 1, len(bars)))
                for bar, color in zip(bars, colors):
                    bar.set_color(color)
                
                plt.tight_layout()
                plt.savefig(f"{output_dir}06_feature_analysis.png", dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                plt.close()
                print("✅ Feature analysis fallback saved")
            
        except Exception as e:
            print(f"Error in matplotlib fallback: {e}")


def main():
    """Main function"""
    print("Initializing enhanced robot visualizer...")
    visualizer = EnhancedRobotVisualizer()
    
    print("Saving static visualization charts...")
    visualizer.save_static_visualizations()
    
    print("Starting interactive dashboard...")
    app = visualizer.create_dashboard()
    app.run_server(debug=True, host='0.0.0.0', port=8050)


if __name__ == "__main__":
    main()
