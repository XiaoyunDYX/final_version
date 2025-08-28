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
        
        # Save as PNG instead of HTML
        try:
            fig.write_image(f"{output_dir}07_sunburst_phylogenetic.png", 
                          width=1200, height=1200, scale=2, engine="kaleido")
            print(f"   ✅ Created: {output_dir}07_sunburst_phylogenetic.png")
        except Exception as e:
            print(f"   ⚠️ Kaleido error, using matplotlib fallback: {e}")
            self._create_sunburst_matplotlib_fallback(output_dir)
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
        
        # Save as PNG instead of HTML
        try:
            fig.write_image(f"{output_dir}08_treemap_phylogenetic.png", 
                          width=1600, height=1000, scale=2, engine="kaleido")
            print(f"   ✅ Created: {output_dir}08_treemap_phylogenetic.png")
        except Exception as e:
            print(f"   ⚠️ Kaleido error, using matplotlib fallback: {e}")
            self._create_treemap_matplotlib_fallback(output_dir)
        
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
        
        # Save as PNG instead of HTML
        try:
            fig.write_image(f"{output_dir}09_network_phylogenetic.png", 
                          width=1600, height=1200, scale=2, engine="kaleido")
            print(f"   ✅ Created: {output_dir}09_network_phylogenetic.png")
        except Exception as e:
            print(f"   ⚠️ Kaleido error, using matplotlib fallback: {e}")
            self._create_network_matplotlib_fallback(output_dir)
        
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
        
        # Save as PNG instead of HTML
        try:
            fig.write_image(f"{output_dir}10_class_distribution.png", 
                          width=1200, height=1000, scale=2, engine="kaleido")
            print(f"   ✅ Created: {output_dir}10_class_distribution.png")
        except Exception as e:
            print(f"   ⚠️ Kaleido error, using matplotlib fallback: {e}")
            self._create_class_distribution_matplotlib_fallback(output_dir)
        
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
        
        # Save as PNG instead of HTML
        try:
            fig.write_image(f"{output_dir}11_evolutionary_timeline.png", 
                          width=1600, height=1000, scale=2, engine="kaleido")
            print(f"   ✅ Created: {output_dir}11_evolutionary_timeline.png")
        except Exception as e:
            print(f"   ⚠️ Kaleido error, using matplotlib fallback: {e}")
            self._create_timeline_matplotlib_fallback(output_dir)
        
        return True
    
    def _create_sunburst_matplotlib_fallback(self, output_dir):
        """Create matplotlib fallback for sunburst chart"""
        import matplotlib.pyplot as plt
        from collections import Counter
        
        # Count by class for pie chart fallback
        class_counts = Counter()
        for robot in self.robots_data:
            class_id = robot.get('c', -1)
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_counts[self.dict_data['class'][class_id]] += 1
        
        plt.figure(figsize=(12, 12))
        plt.pie(list(class_counts.values()), labels=list(class_counts.keys()), 
               autopct='%1.1f%%', startangle=90)
        plt.title('Robot Taxonomy Distribution (Class Level)', fontsize=20, fontweight='bold', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(f"{output_dir}07_sunburst_phylogenetic.png", dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
    def _create_treemap_matplotlib_fallback(self, output_dir):
        """Create matplotlib fallback for treemap"""
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from collections import Counter
        
        # Count by class
        class_counts = Counter()
        for robot in self.robots_data:
            class_id = robot.get('c', -1)
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_counts[self.dict_data['class'][class_id]] += 1
        
        # Create horizontal bar chart as treemap alternative
        classes = list(class_counts.keys())
        counts = list(class_counts.values())
        
        plt.figure(figsize=(16, 10))
        bars = plt.barh(range(len(classes)), counts)
        plt.title('Robot Taxonomy Distribution (Treemap Alternative)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Number of Robots', fontsize=14)
        plt.ylabel('Robot Classes', fontsize=14)
        plt.yticks(range(len(classes)), classes)
        
        # Color bars
        colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}08_treemap_phylogenetic.png", dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
    def _create_network_matplotlib_fallback(self, output_dir):
        """Create matplotlib fallback for network graph"""
        import matplotlib.pyplot as plt
        import networkx as nx
        from collections import defaultdict, Counter
        
        G = nx.Graph()
        
        # Count occurrences
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
        
        # Add root node
        G.add_node("Robot Kingdom", node_type='root', count=len(self.robots_data))
        
        # Add domain nodes and edges
        for domain, count in domain_counts.items():
            G.add_node(domain, node_type='domain', count=count)
            G.add_edge("Robot Kingdom", domain)
        
        # Add class nodes and edges (limit to avoid overcrowding)
        for domain, classes in domain_class_counts.items():
            top_classes = sorted(classes.items(), key=lambda x: x[1], reverse=True)[:3]  # Top 3 classes per domain
            for class_name, count in top_classes:
                if count > 5:  # Only classes with more than 5 robots
                    G.add_node(class_name, node_type='class', count=count)
                    G.add_edge(domain, class_name)
        
        # Create layout
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        plt.figure(figsize=(16, 12))
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=1)
        
        # Draw nodes by type
        root_nodes = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'root']
        domain_nodes = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'domain']
        class_nodes = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'class']
        
        if root_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=root_nodes, node_color='red', 
                                 node_size=1000, alpha=0.8)
        if domain_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=domain_nodes, node_color='blue', 
                                 node_size=500, alpha=0.8)
        if class_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=class_nodes, node_color='green', 
                                 node_size=200, alpha=0.8)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        plt.title('Robot Taxonomy Network Graph', fontsize=20, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{output_dir}09_network_phylogenetic.png", dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
    def _create_class_distribution_matplotlib_fallback(self, output_dir):
        """Create matplotlib fallback for class distribution"""
        import matplotlib.pyplot as plt
        from collections import Counter
        
        class_counts = Counter()
        for robot in self.robots_data:
            class_id = robot.get('c', -1)
            if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                class_counts[self.dict_data['class'][class_id]] += 1
        
        plt.figure(figsize=(12, 12))
        plt.pie(list(class_counts.values()), labels=list(class_counts.keys()), 
               autopct='%1.1f%%', startangle=90)
        plt.title('Robot Class Distribution', fontsize=20, fontweight='bold', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(f"{output_dir}10_class_distribution.png", dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
    def _create_timeline_matplotlib_fallback(self, output_dir):
        """Create matplotlib fallback for timeline"""
        import matplotlib.pyplot as plt
        
        timeline_data = []
        for robot in self.robots_data:
            year = robot.get('yr')
            if year is not None and year > 0:
                class_id = robot.get('c', -1)
                class_name = 'Unknown'
                if class_id >= 0 and class_id < len(self.dict_data.get('class', [])):
                    class_name = self.dict_data['class'][class_id]
                
                timeline_data.append({'year': year, 'class': class_name})
        
        if timeline_data:
            df_timeline = pd.DataFrame(timeline_data)
            year_counts = df_timeline.groupby('year').size()
            
            plt.figure(figsize=(16, 8))
            plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, markersize=6)
            plt.title('Robot Evolution Timeline', fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Number of Robots Developed', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}11_evolutionary_timeline.png", dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
    
    def generate_all_separate_pages(self, output_dir="outputs/figures/"):
        """Generate all separate phylogenetic PNG images"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🌳 Phylogenetic Tree PNG Generator")
        print("=" * 60)
        
        try:
            # Create individual PNG images
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
            
            if success_count >= 5:  # At least 5 main visualizations
                print(f"\n🎉 SUCCESS! Created {success_count} phylogenetic PNG images!")
                print(f"📁 Images saved to: {output_dir}")
                return output_dir
            else:
                print(f"\n⚠️ Only {success_count} images created successfully.")
                return None
                
        except Exception as e:
            print(f"\n❌ Error generating PNG images: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main function to generate separate phylogenetic PNG images"""
    print("🔧 Phylogenetic PNG Generator")
    print("=" * 60)
    
    try:
        generator = SeparatePhylogeneticGenerator()
        output_dir = generator.generate_all_separate_pages()
        
        if output_dir:
            print(f"\n✅ All phylogenetic PNG images created successfully!")
            print(f"🌟 Images saved to: {output_dir}")
        else:
            print(f"\n💥 Failed to generate PNG images.")
            
        return output_dir is not None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
