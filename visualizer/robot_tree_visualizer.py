import json
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from typing import Dict, List, Any, Optional
import pandas as pd
import kaleido  # For PNG export
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from collections import defaultdict

class RobotTreeVisualizer:
    def __init__(self):
        self.graph = nx.Graph()
        self.robots_data = []
        self.taxonomy_hierarchy = {}
        
    def load_data(self, filename: str = 'classified_robots_gpt.json'):
        """
        Load classified robot data from GPT classification
        """
        try:
            with open(f'./data/{filename}', 'r', encoding='utf-8') as f:
                self.robots_data = json.load(f)
            print(f"Loaded {len(self.robots_data)} robots from GPT classification")
        except FileNotFoundError:
            print(f"File {filename} not found")
            self.robots_data = []
    
    def build_taxonomy_tree(self) -> nx.Graph:
        """
        Build a hierarchical tree structure based on the GPT taxonomy
        """
        # Define the GPT hierarchical taxonomy structure
        taxonomy = {
            "Robots": {
                "Domain": {
                    "Physical": "Material world operation with direct environmental interaction",
                    "Virtual": "Digital environment operation (software agents, simulated systems)",
                    "Hybrid": "Bridging physical and virtual domains (AR/VR robotics, telepresence)"
                },
                "Kingdom": {
                    "Industrial": "Manufacturing, production, factory automation",
                    "Service": "Human assistance, domestic, commercial applications",
                    "Medical": "Healthcare, surgical assistance, therapeutic applications",
                    "Military": "Defense, security, tactical operations",
                    "Research": "Scientific investigation and experimentation",
                    "Entertainment": "Recreation, education, social interaction",
                    "Agriculture": "Farming, crop management, agricultural automation",
                    "Space": "Extraterrestrial exploration and operations",
                    "Marine": "Underwater and surface water operations"
                },
                "Morpho_Motion_Class": {
                    "Wheeled-Mobile": "Wheel-based mobile systems",
                    "Tracked-Mobile": "Track-based mobile systems", 
                    "Legged-Humanoid": "Human-like bipedal systems",
                    "Legged-Animaloid": "Animal-like legged systems",
                    "Flying-Drone": "Aerial systems",
                    "Swimming-Soft": "Aquatic soft robotics",
                    "Modular-Lattice": "Reconfigurable modular systems",
                    "Swarm-Agent": "Collective swarm systems"
                },
                "Order": {
                    "Manual": "Human-controlled operation",
                    "Teleoperated": "Remote human-controlled operation",
                    "Autonomous": "Fully autonomous operation",
                    "Semi-Autonomous": "Partial autonomous operation with human oversight",
                    "Collaborative": "Human-robot collaborative operation",
                    "Swarm-Based": "Collective swarm operation"
                },
                "Sensing_Family": {
                    "Vision-Based": "Cameras and visual processing systems",
                    "LiDAR-Based": "Laser-based distance and mapping systems",
                    "Tactile-Based": "Touch and force sensing systems",
                    "GPS-Based": "Satellite-based positioning systems",
                    "Acoustic-Based": "Sound and ultrasonic sensing systems",
                    "Chemical-Based": "Detection of chemical compounds and gases",
                    "Multimodal": "Integration of multiple sensing technologies",
                    "Minimal Sensing": "Simple sensors with basic environmental awareness"
                },
                "Actuation_Genus": {
                    "Electric": "Electric motors and servo systems",
                    "Hydraulic": "Fluid pressure-based actuation",
                    "Pneumatic": "Compressed air actuation",
                    "Smart Materials": "Shape memory alloys, piezoelectric actuators",
                    "Bio-Hybrid": "Integration of biological and artificial components",
                    "Magnetic": "Magnetic field-based actuation",
                    "Passive": "No active actuation, gravity or environmental forces",
                    "Hybrid Actuation": "Combination of multiple actuation methods"
                },
                "Cognition_Class": {
                    "None": "No cognitive capabilities",
                    "Rule-Based": "Simple rule-based decision making",
                    "Model-Based AI": "Model-based artificial intelligence",
                    "AI-Powered": "General AI-powered systems",
                    "Adaptive Learning": "Systems with adaptive learning capabilities",
                    "Reinforcement Learning": "Reinforcement learning systems",
                    "Generative AI": "Generative artificial intelligence systems"
                },
                "Application_Species": {
                    "Surgery": "Medical procedures requiring extreme precision",
                    "Inspection": "Quality control and monitoring applications",
                    "Transport": "Material handling and logistics operations",
                    "Assembly": "Manufacturing assembly line tasks",
                    "Exploration": "Discovery and reconnaissance missions",
                    "Surveillance": "Surveillance and monitoring tasks",
                    "Companionship": "Social interaction and emotional support",
                    "Education": "Teaching and learning assistance",
                    "Mapping": "Environmental mapping and surveying",
                    "Rescue": "Emergency response and disaster relief",
                    "Entertainment": "Shows, games, interactive experiences",
                    "Agricultural Task": "Farming and crop management",
                    "Construction": "Building and infrastructure development",
                    "Maintenance": "Repair and upkeep operations",
                    "Environmental Monitoring": "Ecosystem and pollution monitoring"
                }
            }
        }
        
        self.taxonomy_hierarchy = taxonomy
        self.graph = nx.Graph()
        
        # Build the tree structure
        self._add_taxonomy_nodes(taxonomy, parent="")
        
        # Add robot nodes and connect them to taxonomy
        self._add_robot_nodes()
        
        return self.graph
    
    def _add_taxonomy_nodes(self, taxonomy: Dict, parent: str):
        """
        Recursively add taxonomy nodes to the graph
        """
        for key, value in taxonomy.items():
            node_id = f"{parent}.{key}" if parent else key
            self.graph.add_node(node_id, type="taxonomy", level=len(node_id.split('.'))-1)
            
            if parent:
                self.graph.add_edge(parent, node_id)
            
            if isinstance(value, dict):
                self._add_taxonomy_nodes(value, node_id)
            elif isinstance(value, str):
                # For the new structure, values are descriptions
                pass
    
    def _add_robot_nodes(self):
        """
        Add robot nodes and connect them to appropriate taxonomy nodes for GPT classification
        """
        for robot in self.robots_data:
            robot_id = f"robot_{robot['name'].replace(' ', '_')}"
            self.graph.add_node(robot_id, 
                              type="robot", 
                              name=robot['name'],
                              description=robot.get('description', ''),
                              manufacturer=robot.get('manufacturer', ''),
                              level=10)  # Robots are at the bottom level
            
            # Connect robot to taxonomy based on GPT classification
            # Map GPT fields to taxonomy levels
            field_mapping = {
                'domain': 'Domain',
                'kingdom': 'Kingdom', 
                'morpho_motion_class': 'Morpho_Motion_Class',
                'order': 'Order',
                'sensing_family': 'Sensing_Family',
                'actuation_genus': 'Actuation_Genus',
                'cognition_class': 'Cognition_Class',
                'application_species': 'Application_Species'
            }
            
            for gpt_field, taxonomy_level in field_mapping.items():
                if gpt_field in robot:
                    category = robot[gpt_field]
                    if category and category != "MISSING":
                        # Handle list for application_species
                        if isinstance(category, list):
                            for app in category:
                                if app and app != "MISSING":
                                    level_node = f"Robots.{taxonomy_level}.{app}"
                                    if level_node in self.graph:
                                        self.graph.add_edge(level_node, robot_id, weight=1.0)
                        else:
                            level_node = f"Robots.{taxonomy_level}.{category}"
                            if level_node in self.graph:
                                self.graph.add_edge(level_node, robot_id, weight=1.0)
    
    def create_radial_tree_of_life(self) -> go.Figure:
        """
        Create a radial tree of life visualization similar to biological taxonomy
        """
        if not self.graph.nodes():
            self.build_taxonomy_tree()
        
        # Use radial layout for tree of life effect
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Convert to radial coordinates
        radial_pos = {}
        for node, (x, y) in pos.items():
            # Convert to polar coordinates
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            radial_pos[node] = (r, theta)
        
        # Separate nodes by type and level
        taxonomy_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'taxonomy']
        robot_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'robot']
        
        # Create the figure
        fig = go.Figure()
        
        # Add edges with curved lines for tree effect
        edge_x = []
        edge_y = []
        edge_colors = []
        
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Create curved edges
            t = np.linspace(0, 1, 50)
            x_curve = x0 + (x1 - x0) * t
            y_curve = y0 + (y1 - y0) * t
            
            edge_x.extend(x_curve)
            edge_y.extend(y_curve)
            edge_colors.extend(['#888'] * len(t))
            
            edge_x.append(None)
            edge_y.append(None)
            edge_colors.append(None)
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add taxonomy nodes by level with different colors
        level_colors = {
            0: '#1f77b4',  # Root
            1: '#ff7f0e',  # Domain
            2: '#2ca02c',  # Kingdom
            3: '#d62728',  # Morpho_Motion_Class
            4: '#9467bd',  # Order
            5: '#8c564b',  # Sensing_Family
            6: '#e377c2',  # Actuation_Genus
            7: '#7f7f7f',  # Cognition_Class
            8: '#bcbd22'   # Application_Species
        }
        
        for level in range(9):
            level_nodes = [n for n, d in self.graph.nodes(data=True) 
                          if d.get('type') == 'taxonomy' and d.get('level') == level]
            
            if level_nodes:
                x_coords = [pos[node][0] for node in level_nodes]
                y_coords = [pos[node][1] for node in level_nodes]
                node_names = [node.split('.')[-1] for node in level_nodes]
                
                fig.add_trace(go.Scatter(
                    x=x_coords, y=y_coords,
                    mode='markers+text',
                    marker=dict(
                        size=15 + level * 2,
                        color=level_colors.get(level, '#1f77b4'),
                        symbol='circle',
                        line=dict(width=2, color='white')
                    ),
                    text=node_names,
                    textposition="middle center",
                    textfont=dict(size=8 + level),
                    name=f'Level {level}',
                    hovertemplate='<b>%{text}</b><br>Level: %{customdata}<extra></extra>',
                    customdata=[level] * len(level_nodes),
                    showlegend=(level < 3)  # Only show first 3 levels in legend
                ))
        
        # Add robot nodes as leaves
        if robot_nodes:
            robot_x = [pos[node][0] for node in robot_nodes]
            robot_y = [pos[node][1] for node in robot_nodes]
            robot_names = [self.graph.nodes[node]['name'] for node in robot_nodes]
            
            fig.add_trace(go.Scatter(
                x=robot_x, y=robot_y,
                mode='markers',
                marker=dict(
                    size=6,
                    color='red',
                    symbol='circle',
                    opacity=0.7
                ),
                name='Robots',
                hovertemplate='<b>%{text}</b><extra></extra>',
                text=robot_names,
                showlegend=True
            ))
        
        fig.update_layout(
            title="Tree of Robotic Life - Radial View",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            width=1400,
            height=1000,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_phylogenetic_tree(self) -> go.Figure:
        """
        Create a phylogenetic-style tree visualization
        """
        if not self.graph.nodes():
            self.build_taxonomy_tree()
        
        # Create hierarchical layout
        pos = nx.spring_layout(self.graph, k=3, iterations=100)
        
        # Separate nodes by type
        taxonomy_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'taxonomy']
        robot_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'robot']
        
        fig = go.Figure()
        
        # Add edges with phylogenetic style
        edge_x = []
        edge_y = []
        
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Create straight phylogenetic-style edges
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#333'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add taxonomy nodes with phylogenetic colors
        level_colors = {
            0: '#1f77b4',  # Root
            1: '#ff7f0e',  # Domain
            2: '#2ca02c',  # Kingdom
            3: '#d62728',  # Morpho_Motion_Class
            4: '#9467bd',  # Order
            5: '#8c564b',  # Sensing_Family
            6: '#e377c2',  # Actuation_Genus
            7: '#7f7f7f',  # Cognition_Class
            8: '#bcbd22'   # Application_Species
        }
        
        for level in range(9):
            level_nodes = [n for n, d in self.graph.nodes(data=True) 
                          if d.get('type') == 'taxonomy' and d.get('level') == level]
            
            if level_nodes:
                x_coords = [pos[node][0] for node in level_nodes]
                y_coords = [pos[node][1] for node in level_nodes]
                node_names = [node.split('.')[-1] for node in level_nodes]
                
                fig.add_trace(go.Scatter(
                    x=x_coords, y=y_coords,
                    mode='markers+text',
                    marker=dict(
                        size=20 + level * 3,
                        color=level_colors.get(level, '#1f77b4'),
                        symbol='circle',
                        line=dict(width=2, color='white')
                    ),
                    text=node_names,
                    textposition="middle center",
                    textfont=dict(size=10 + level),
                    name=f'Taxonomic Level {level}',
                    hovertemplate='<b>%{text}</b><br>Level: %{customdata}<extra></extra>',
                    customdata=[level] * len(level_nodes)
                ))
        
        # Add robot nodes as terminal taxa
        if robot_nodes:
            robot_x = [pos[node][0] for node in robot_nodes]
            robot_y = [pos[node][1] for node in robot_nodes]
            robot_names = [self.graph.nodes[node]['name'] for node in robot_nodes]
            
            fig.add_trace(go.Scatter(
                x=robot_x, y=robot_y,
                mode='markers',
                marker=dict(
                    size=8,
                    color='red',
                    symbol='circle',
                    opacity=0.8
                ),
                name='Robot Species',
                hovertemplate='<b>%{text}</b><extra></extra>',
                text=robot_names
            ))
        
        fig.update_layout(
            title="Tree of Robotic Life - Phylogenetic View",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            width=1400,
            height=1000
        )
        
        return fig
    
    def create_hierarchical_dendrogram(self) -> go.Figure:
        """
        Create a hierarchical dendrogram visualization
        """
        if not self.graph.nodes():
            self.build_taxonomy_tree()
        
        # Use hierarchical layout
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Separate nodes by type
        taxonomy_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'taxonomy']
        robot_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'robot']
        
        fig = go.Figure()
        
        # Add edges with dendrogram style
        edge_x = []
        edge_y = []
        
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Create dendrogram-style edges
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#666'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add taxonomy nodes with hierarchical colors
        level_colors = {
            0: '#1f77b4',  # Root
            1: '#ff7f0e',  # Domain
            2: '#2ca02c',  # Kingdom
            3: '#d62728',  # Morpho_Motion_Class
            4: '#9467bd',  # Order
            5: '#8c564b',  # Sensing_Family
            6: '#e377c2',  # Actuation_Genus
            7: '#7f7f7f',  # Cognition_Class
            8: '#bcbd22'   # Application_Species
        }
        
        for level in range(9):
            level_nodes = [n for n, d in self.graph.nodes(data=True) 
                          if d.get('type') == 'taxonomy' and d.get('level') == level]
            
            if level_nodes:
                x_coords = [pos[node][0] for node in level_nodes]
                y_coords = [pos[node][1] for node in level_nodes]
                node_names = [node.split('.')[-1] for node in level_nodes]
                
                fig.add_trace(go.Scatter(
                    x=x_coords, y=y_coords,
                    mode='markers+text',
                    marker=dict(
                        size=18 + level * 2,
                        color=level_colors.get(level, '#1f77b4'),
                        symbol='diamond' if level < 3 else 'circle',
                        line=dict(width=2, color='white')
                    ),
                    text=node_names,
                    textposition="middle center",
                    textfont=dict(size=9 + level),
                    name=f'Level {level}',
                    hovertemplate='<b>%{text}</b><br>Hierarchical Level: %{customdata}<extra></extra>',
                    customdata=[level] * len(level_nodes)
                ))
        
        # Add robot nodes as leaves
        if robot_nodes:
            robot_x = [pos[node][0] for node in robot_nodes]
            robot_y = [pos[node][1] for node in robot_nodes]
            robot_names = [self.graph.nodes[node]['name'] for node in robot_nodes]
            
            fig.add_trace(go.Scatter(
                x=robot_x, y=robot_y,
                mode='markers',
                marker=dict(
                    size=6,
                    color='red',
                    symbol='circle',
                    opacity=0.7
                ),
                name='Robot Leaves',
                hovertemplate='<b>%{text}</b><extra></extra>',
                text=robot_names
            ))
        
        fig.update_layout(
            title="Tree of Robotic Life - Hierarchical Dendrogram",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            width=1400,
            height=1000
        )
        
        return fig

    def create_taxonomy_bar_charts(self) -> go.Figure:
        """
        Create bar charts showing the distribution of robots across taxonomic levels
        """
        if not self.robots_data:
            return go.Figure()
        
        # Define taxonomic levels
        taxonomic_levels = ['Domain', 'Kingdom', 'Morpho_Motion_Class', 'Order', 'Sensing_Family', 'Actuation_Genus', 'Cognition_Class', 'Application_Species']
        
        # Create subplots for each taxonomic level
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=taxonomic_levels,
            vertical_spacing=0.08,
            horizontal_spacing=0.1
        )
        
        # Define colors for each level
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        
        for i, level in enumerate(taxonomic_levels):
            # Count robots in each category for this level
            category_counts = defaultdict(int)
            
            # Map taxonomy level to GPT field
            field_mapping = {
                'Domain': 'domain',
                'Kingdom': 'kingdom',
                'Morpho_Motion_Class': 'morpho_motion_class',
                'Order': 'order',
                'Sensing_Family': 'sensing_family',
                'Actuation_Genus': 'actuation_genus',
                'Cognition_Class': 'cognition_class',
                'Application_Species': 'application_species'
            }
            
            gpt_field = field_mapping.get(level)
            if gpt_field:
                for robot in self.robots_data:
                    if gpt_field in robot:
                        category = robot[gpt_field]
                        if category and category != "MISSING":
                            # Handle list for application_species
                            if isinstance(category, list):
                                for app in category:
                                    if app and app != "MISSING":
                                        category_counts[app] += 1
                            else:
                                category_counts[category] += 1
            
            # Sort categories by count
            sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            categories = [cat for cat, count in sorted_categories]
            counts = [count for cat, count in sorted_categories]
            
            # Calculate row and column for subplot
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            # Add bar chart
            fig.add_trace(
                go.Bar(
                    x=categories,
                    y=counts,
                    name=level,
                    marker_color=colors[i],
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Update layout for this subplot
            fig.update_xaxes(title_text="Categories", row=row, col=col, tickangle=45)
            fig.update_yaxes(title_text="Count", row=row, col=col)
        
        fig.update_layout(
            title="Robot Distribution Across Taxonomic Levels",
            height=1200,
            width=1400,
            showlegend=False
        )
        
        return fig
    
    def create_simplified_tree(self) -> go.Figure:
        """
        Create a simplified tree showing only the taxonomic structure without individual robots
        """
        # Define the taxonomic hierarchy structure
        taxonomy_structure = {
            "Robots": {
                "Physical": {
                    "Industrial": {
                        "Manipulator": {
                            "Static": {
                                "Teleoperated": {
                                    "Vision_Based": {
                                        "Electric": {
                                            "Assembly": {},
                                            "Inspection": {},
                                            "Transport": {}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "Service": {
                        "Mobile": {
                            "Wheeled": {
                                "Semi_Autonomous": {
                                    "LiDAR_Based": {
                                        "Electric": {
                                            "Transport": {},
                                            "Security": {}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "Medical": {
                        "Manipulator": {
                            "Static": {
                                "Teleoperated": {
                                    "Vision_Based": {
                                        "Electric": {
                                            "Surgery": {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "Virtual": {
                    "Research": {
                        "Modular": {
                            "Static": {
                                "Autonomous": {
                                    "Multimodal": {
                                        "Electric": {
                                            "Education": {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "Hybrid": {
                    "Space": {
                        "Mobile": {
                            "Wheeled": {
                                "Autonomous": {
                                    "Vision_Based": {
                                        "Electric": {
                                            "Exploration": {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Create hierarchical layout
        fig = go.Figure()
        
        # Define node positions manually for better control
        node_positions = {
            "Robots": (0, 0),
            "Physical": (-2, -1), "Virtual": (0, -1), "Hybrid": (2, -1),
            "Industrial": (-3, -2), "Service": (-1, -2), "Medical": (1, -2),
            "Research": (0, -2), "Space": (2, -2),
            "Manipulator": (-3.5, -3), "Mobile": (-1.5, -3), "Modular": (0.5, -3),
            "Static": (-3.5, -4), "Wheeled": (-1.5, -4),
            "Teleoperated": (-3.5, -5), "Semi_Autonomous": (-1.5, -5), "Autonomous": (0.5, -5),
            "Vision_Based": (-3.5, -6), "LiDAR_Based": (-1.5, -6), "Multimodal": (0.5, -6),
            "Electric": (-3.5, -7), "Electric2": (-1.5, -7), "Electric3": (0.5, -7),
            "Assembly": (-4, -8), "Inspection": (-3, -8), "Transport": (-2, -8),
            "Transport2": (-1, -8), "Security": (0, -8), "Surgery": (1, -8),
            "Education": (0.5, -8), "Exploration": (2.5, -8)
        }
        
        # Add edges
        edges = [
            ("Robots", "Physical"), ("Robots", "Virtual"), ("Robots", "Hybrid"),
            ("Physical", "Industrial"), ("Physical", "Service"), ("Physical", "Medical"),
            ("Virtual", "Research"), ("Hybrid", "Space"),
            ("Industrial", "Manipulator"), ("Service", "Mobile"), ("Research", "Modular"),
            ("Manipulator", "Static"), ("Mobile", "Wheeled"),
            ("Static", "Teleoperated"), ("Wheeled", "Semi_Autonomous"), ("Modular", "Autonomous"),
            ("Teleoperated", "Vision_Based"), ("Semi_Autonomous", "LiDAR_Based"), ("Autonomous", "Multimodal"),
            ("Vision_Based", "Electric"), ("LiDAR_Based", "Electric2"), ("Multimodal", "Electric3"),
            ("Electric", "Assembly"), ("Electric", "Inspection"), ("Electric", "Transport"),
            ("Electric2", "Transport2"), ("Electric2", "Security"), ("Electric", "Surgery"),
            ("Electric3", "Education"), ("Electric", "Exploration")
        ]
        
        # Add edges
        edge_x = []
        edge_y = []
        for edge in edges:
            if edge[0] in node_positions and edge[1] in node_positions:
                x0, y0 = node_positions[edge[0]]
                x1, y1 = node_positions[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#333'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add nodes with different colors by level
        level_colors = {
            0: '#1f77b4',  # Root
            1: '#ff7f0e',  # Domain
            2: '#2ca02c',  # Kingdom
            3: '#d62728',  # Morpho_Motion_Class
            4: '#9467bd',  # Order
            5: '#8c564b',  # Sensing_Family
            6: '#e377c2',  # Actuation_Genus
            7: '#7f7f7f',  # Cognition_Class
            8: '#bcbd22'   # Application_Species
        }
        
        for node, (x, y) in node_positions.items():
            # Determine level based on node name
            level = 0
            if node in ["Physical", "Virtual", "Hybrid"]:
                level = 1
            elif node in ["Industrial", "Service", "Medical", "Research", "Space"]:
                level = 2
            elif node in ["Manipulator", "Mobile", "Modular"]:
                level = 3
            elif node in ["Static", "Wheeled"]:
                level = 4
            elif node in ["Teleoperated", "Semi_Autonomous", "Autonomous"]:
                level = 5
            elif node in ["Vision_Based", "LiDAR_Based", "Multimodal"]:
                level = 6
            elif node.startswith("Electric"):
                level = 7
            else:
                level = 8
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=20 + level * 3,
                    color=level_colors.get(level, '#1f77b4'),
                    symbol='circle',
                    line=dict(width=2, color='white')
                ),
                text=[node],
                textposition="middle center",
                textfont=dict(size=10 + level),
                name=f'Level {level}',
                showlegend=False,
                hovertemplate=f'<b>{node}</b><br>Level: {level}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Simplified Tree of Robotic Life - Taxonomic Structure",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            width=1400,
            height=1000
        )
        
        return fig
    
    def create_taxonomy_summary_chart(self) -> go.Figure:
        """
        Create a summary chart showing the top categories at each taxonomic level
        """
        if not self.robots_data:
            return go.Figure()
        
        # Define taxonomic levels
        taxonomic_levels = ['Domain', 'Kingdom', 'Morpho_Motion_Class', 'Order', 'Sensing_Family', 'Actuation_Genus', 'Cognition_Class', 'Application_Species']
        
        # Get top 5 categories for each level
        top_categories = {}
        
        for level in taxonomic_levels:
            category_counts = defaultdict(int)
            
            # Map taxonomy level to GPT field
            field_mapping = {
                'Domain': 'domain',
                'Kingdom': 'kingdom',
                'Morpho_Motion_Class': 'morpho_motion_class',
                'Order': 'order',
                'Sensing_Family': 'sensing_family',
                'Actuation_Genus': 'actuation_genus',
                'Cognition_Class': 'cognition_class',
                'Application_Species': 'application_species'
            }
            
            gpt_field = field_mapping.get(level)
            if gpt_field:
                for robot in self.robots_data:
                    if gpt_field in robot:
                        category = robot[gpt_field]
                        if category and category != "MISSING":
                            # Handle list for application_species
                            if isinstance(category, list):
                                for app in category:
                                    if app and app != "MISSING":
                                        category_counts[app] += 1
                            else:
                                category_counts[category] += 1
            
            # Get top 5 categories
            sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            top_categories[level] = sorted_categories[:5]
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        
        for i, level in enumerate(taxonomic_levels):
            if level in top_categories:
                categories = [cat for cat, count in top_categories[level]]
                counts = [count for cat, count in top_categories[level]]
                
                fig.add_trace(go.Bar(
                    y=[f"{level}: {cat}" for cat in categories],
                    x=counts,
                    orientation='h',
                    name=level,
                    marker_color=colors[i],
                    showlegend=False
                ))
        
        fig.update_layout(
            title="Top Categories at Each Taxonomic Level",
            xaxis_title="Number of Robots",
            yaxis_title="Taxonomic Categories",
            height=800,
            width=1200,
            showlegend=False
        )
        
        return fig

    def save_radial_tree_as_png(self, filename: str = 'robot_radial_tree.png'):
        """
        Save the radial tree visualization as a PNG file
        """
        fig = self.create_radial_tree_of_life()
        fig.write_image(f"./data/{filename}", width=1400, height=1000)
        print(f"✅ Radial tree visualization saved as PNG: data/{filename}")
    
    def save_phylogenetic_tree_as_png(self, filename: str = 'robot_phylogenetic_tree.png'):
        """
        Save the phylogenetic tree visualization as a PNG file
        """
        fig = self.create_phylogenetic_tree()
        fig.write_image(f"./data/{filename}", width=1400, height=1000)
        print(f"✅ Phylogenetic tree visualization saved as PNG: data/{filename}")
    
    def save_dendrogram_as_png(self, filename: str = 'robot_dendrogram.png'):
        """
        Save the hierarchical dendrogram visualization as a PNG file
        """
        fig = self.create_hierarchical_dendrogram()
        fig.write_image(f"./data/{filename}", width=1400, height=1000)
        print(f"✅ Dendrogram visualization saved as PNG: data/{filename}")
    
    def create_cluster_visualization(self) -> go.Figure:
        """
        Create a cluster visualization based on robot similarities
        """
        if not self.robots_data:
            return go.Figure()
        
        # Extract features for clustering visualization
        features = []
        robot_names = []
        
        for robot in self.robots_data:
            robot_names.append(robot['name'])
            
            # Create feature vector
            feature_vector = []
            
            # Domain features (one-hot encoding)
            domain = robot.get('domain', '')
            feature_vector.extend([
                1.0 if domain == 'Physical' else 0.0,
                1.0 if domain == 'Virtual' else 0.0,
                1.0 if domain == 'Hybrid' else 0.0
            ])
            
            # Kingdom features (one-hot encoding)
            kingdom = robot.get('kingdom', '')
            feature_vector.extend([
                1.0 if kingdom == 'Industrial' else 0.0,
                1.0 if kingdom == 'Service' else 0.0,
                1.0 if kingdom == 'Medical' else 0.0,
                1.0 if kingdom == 'Military' else 0.0,
                1.0 if kingdom == 'Research' else 0.0,
                1.0 if kingdom == 'Entertainment' else 0.0,
                1.0 if kingdom == 'Agriculture' else 0.0,
                1.0 if kingdom == 'Space' else 0.0,
                1.0 if kingdom == 'Marine' else 0.0
            ])
            
            # Morpho_Motion_Class features (one-hot encoding)
            morpho_motion = robot.get('morpho_motion_class', '')
            feature_vector.extend([
                1.0 if morpho_motion == 'Wheeled-Mobile' else 0.0,
                1.0 if morpho_motion == 'Tracked-Mobile' else 0.0,
                1.0 if morpho_motion == 'Legged-Humanoid' else 0.0,
                1.0 if morpho_motion == 'Legged-Animaloid' else 0.0,
                1.0 if morpho_motion == 'Flying-Drone' else 0.0,
                1.0 if morpho_motion == 'Swimming-Soft' else 0.0,
                1.0 if morpho_motion == 'Modular-Lattice' else 0.0,
                1.0 if morpho_motion == 'Swarm-Agent' else 0.0
            ])
            
            # Order features (one-hot encoding)
            order = robot.get('order', '')
            feature_vector.extend([
                1.0 if order == 'Manual' else 0.0,
                1.0 if order == 'Teleoperated' else 0.0,
                1.0 if order == 'Autonomous' else 0.0,
                1.0 if order == 'Semi-Autonomous' else 0.0,
                1.0 if order == 'Collaborative' else 0.0,
                1.0 if order == 'Swarm-Based' else 0.0
            ])
            
            # Sensing_Family features (one-hot encoding)
            sensing_family = robot.get('sensing_family', '')
            feature_vector.extend([
                1.0 if sensing_family == 'Vision-Based' else 0.0,
                1.0 if sensing_family == 'LiDAR-Based' else 0.0,
                1.0 if sensing_family == 'Tactile-Based' else 0.0,
                1.0 if sensing_family == 'GPS-Based' else 0.0,
                1.0 if sensing_family == 'Acoustic-Based' else 0.0,
                1.0 if sensing_family == 'Chemical-Based' else 0.0,
                1.0 if sensing_family == 'Multimodal' else 0.0,
                1.0 if sensing_family == 'Minimal Sensing' else 0.0
            ])
            
            # Actuation_Genus features (one-hot encoding)
            actuation_genus = robot.get('actuation_genus', '')
            feature_vector.extend([
                1.0 if actuation_genus == 'Electric' else 0.0,
                1.0 if actuation_genus == 'Hydraulic' else 0.0,
                1.0 if actuation_genus == 'Pneumatic' else 0.0,
                1.0 if actuation_genus == 'Smart Materials' else 0.0,
                1.0 if actuation_genus == 'Bio-Hybrid' else 0.0,
                1.0 if actuation_genus == 'Magnetic' else 0.0,
                1.0 if actuation_genus == 'Passive' else 0.0,
                1.0 if actuation_genus == 'Hybrid Actuation' else 0.0
            ])
            
            # Cognition_Class features (one-hot encoding)
            cognition_class = robot.get('cognition_class', '')
            feature_vector.extend([
                1.0 if cognition_class == 'None' else 0.0,
                1.0 if cognition_class == 'Rule-Based' else 0.0,
                1.0 if cognition_class == 'Model-Based AI' else 0.0,
                1.0 if cognition_class == 'AI-Powered' else 0.0,
                1.0 if cognition_class == 'Adaptive Learning' else 0.0,
                1.0 if cognition_class == 'Reinforcement Learning' else 0.0,
                1.0 if cognition_class == 'Generative AI' else 0.0
            ])
            
            # Application_Species features (multi-hot encoding for list)
            application_species = robot.get('application_species', [])
            if not isinstance(application_species, list):
                application_species = [application_species] if application_species else []
            
            feature_vector.extend([
                1.0 if 'Surgery' in application_species else 0.0,
                1.0 if 'Inspection' in application_species else 0.0,
                1.0 if 'Transport' in application_species else 0.0,
                1.0 if 'Assembly' in application_species else 0.0,
                1.0 if 'Exploration' in application_species else 0.0,
                1.0 if 'Surveillance' in application_species else 0.0,
                1.0 if 'Companionship' in application_species else 0.0,
                1.0 if 'Education' in application_species else 0.0,
                1.0 if 'Mapping' in application_species else 0.0,
                1.0 if 'Rescue' in application_species else 0.0,
                1.0 if 'Entertainment' in application_species else 0.0,
                1.0 if 'Agricultural Task' in application_species else 0.0,
                1.0 if 'Construction' in application_species else 0.0,
                1.0 if 'Maintenance' in application_species else 0.0,
                1.0 if 'Environmental Monitoring' in application_species else 0.0
            ])
            
            features.append(feature_vector)
        
        # Create 2D visualization using PCA or t-SNE
        # For simplicity, we'll use the first two features
        x_coords = [f[0] for f in features]  # Physical score
        y_coords = [f[1] for f in features]  # Virtual score
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            marker=dict(size=10, color='red'),
            text=robot_names,
            textposition="top center",
            hovertemplate='<b>%{text}</b><br>Physical: %{x}<br>Virtual: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Robot Clusters by Classification",
            xaxis_title="Physical Score",
            yaxis_title="Virtual Score",
            plot_bgcolor='white',
            width=1200,
            height=800
        )
        
        return fig
    
    def save_cluster_as_png(self, filename: str = 'robot_clusters.png'):
        """
        Save the cluster visualization as a PNG file
        """
        fig = self.create_cluster_visualization()
        fig.write_image(f"./data/{filename}", width=1200, height=800)
        print(f"✅ Cluster visualization saved as PNG: data/{filename}")
    
    def save_taxonomy_bar_charts_as_png(self, filename: str = 'robot_taxonomy_bars.png'):
        """
        Save the taxonomy bar charts as a PNG file
        """
        fig = self.create_taxonomy_bar_charts()
        fig.write_image(f"./data/{filename}", width=1400, height=1200)
        print(f"✅ Taxonomy bar charts saved as PNG: data/{filename}")
    
    def save_simplified_tree_as_png(self, filename: str = 'robot_simplified_tree.png'):
        """
        Save the simplified tree visualization as a PNG file
        """
        fig = self.create_simplified_tree()
        fig.write_image(f"./data/{filename}", width=1400, height=1000)
        print(f"✅ Simplified tree visualization saved as PNG: data/{filename}")
    
    def save_taxonomy_summary_as_png(self, filename: str = 'robot_taxonomy_summary.png'):
        """
        Save the taxonomy summary chart as a PNG file
        """
        fig = self.create_taxonomy_summary_chart()
        fig.write_image(f"./data/{filename}", width=1200, height=800)
        print(f"✅ Taxonomy summary chart saved as PNG: data/{filename}")

    def create_dashboard(self) -> dash.Dash:
        """
        Create an interactive dashboard for exploring the robot taxonomy
        """
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        
        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Robot Taxonomy Tree of Life", className="text-center mb-4"),
                    html.P("Explore the evolutionary relationships between different types of robots", 
                           className="text-center text-muted")
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Taxonomy Tree"),
                        dbc.CardBody([
                            dcc.Graph(id='tree-graph', style={'height': '600px'})
                        ])
                    ])
                ], width=8),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Statistics"),
                        dbc.CardBody(id='stats-content')
                    ]),
                    
                    dbc.Card([
                        dbc.CardHeader("Filters"),
                        dbc.CardBody([
                            html.Label("Domain:"),
                            dcc.Dropdown(
                                id='domain-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Physical', 'value': 'Physical'},
                                    {'label': 'Virtual', 'value': 'Virtual'},
                                    {'label': 'Hybrid', 'value': 'Hybrid'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Kingdom:"),
                            dcc.Dropdown(
                                id='kingdom-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Industrial', 'value': 'Industrial'},
                                    {'label': 'Service', 'value': 'Service'},
                                    {'label': 'Medical', 'value': 'Medical'},
                                    {'label': 'Military', 'value': 'Military'},
                                    {'label': 'Research', 'value': 'Research'},
                                    {'label': 'Entertainment', 'value': 'Entertainment'},
                                    {'label': 'Agriculture', 'value': 'Agriculture'},
                                    {'label': 'Space', 'value': 'Space'},
                                    {'label': 'Marine', 'value': 'Marine'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Morpho_Motion_Class:"),
                            dcc.Dropdown(
                                id='morpho_motion_filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Wheeled-Mobile', 'value': 'Wheeled-Mobile'},
                                    {'label': 'Tracked-Mobile', 'value': 'Tracked-Mobile'},
                                    {'label': 'Legged-Humanoid', 'value': 'Legged-Humanoid'},
                                    {'label': 'Legged-Animaloid', 'value': 'Legged-Animaloid'},
                                    {'label': 'Flying-Drone', 'value': 'Flying-Drone'},
                                    {'label': 'Swimming-Soft', 'value': 'Swimming-Soft'},
                                    {'label': 'Modular-Lattice', 'value': 'Modular-Lattice'},
                                    {'label': 'Swarm-Agent', 'value': 'Swarm-Agent'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Order:"),
                            dcc.Dropdown(
                                id='order-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Manual', 'value': 'Manual'},
                                    {'label': 'Teleoperated', 'value': 'Teleoperated'},
                                    {'label': 'Autonomous', 'value': 'Autonomous'},
                                    {'label': 'Semi-Autonomous', 'value': 'Semi-Autonomous'},
                                    {'label': 'Collaborative', 'value': 'Collaborative'},
                                    {'label': 'Swarm-Based', 'value': 'Swarm-Based'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Sensing_Family:"),
                            dcc.Dropdown(
                                id='sensing_family-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Vision-Based', 'value': 'Vision-Based'},
                                    {'label': 'LiDAR-Based', 'value': 'LiDAR-Based'},
                                    {'label': 'Tactile-Based', 'value': 'Tactile-Based'},
                                    {'label': 'GPS-Based', 'value': 'GPS-Based'},
                                    {'label': 'Acoustic-Based', 'value': 'Acoustic-Based'},
                                    {'label': 'Chemical-Based', 'value': 'Chemical-Based'},
                                    {'label': 'Multimodal', 'value': 'Multimodal'},
                                    {'label': 'Minimal Sensing', 'value': 'Minimal Sensing'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Actuation_Genus:"),
                            dcc.Dropdown(
                                id='actuation_genus-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Electric', 'value': 'Electric'},
                                    {'label': 'Hydraulic', 'value': 'Hydraulic'},
                                    {'label': 'Pneumatic', 'value': 'Pneumatic'},
                                    {'label': 'Smart Materials', 'value': 'Smart Materials'},
                                    {'label': 'Bio-Hybrid', 'value': 'Bio-Hybrid'},
                                    {'label': 'Magnetic', 'value': 'Magnetic'},
                                    {'label': 'Passive', 'value': 'Passive'},
                                    {'label': 'Hybrid Actuation', 'value': 'Hybrid Actuation'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Cognition_Class:"),
                            dcc.Dropdown(
                                id='cognition_class-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'None', 'value': 'None'},
                                    {'label': 'Rule-Based', 'value': 'Rule-Based'},
                                    {'label': 'Model-Based AI', 'value': 'Model-Based AI'},
                                    {'label': 'AI-Powered', 'value': 'AI-Powered'},
                                    {'label': 'Adaptive Learning', 'value': 'Adaptive Learning'},
                                    {'label': 'Reinforcement Learning', 'value': 'Reinforcement Learning'},
                                    {'label': 'Generative AI', 'value': 'Generative AI'}
                                ],
                                value='all'
                            ),
                            
                            html.Br(),
                            
                            html.Label("Application_Species:"),
                            dcc.Dropdown(
                                id='application_species-filter',
                                options=[
                                    {'label': 'All', 'value': 'all'},
                                    {'label': 'Surgery', 'value': 'Surgery'},
                                    {'label': 'Inspection', 'value': 'Inspection'},
                                    {'label': 'Transport', 'value': 'Transport'},
                                    {'label': 'Assembly', 'value': 'Assembly'},
                                    {'label': 'Exploration', 'value': 'Exploration'},
                                    {'label': 'Surveillance', 'value': 'Surveillance'},
                                    {'label': 'Companionship', 'value': 'Companionship'},
                                    {'label': 'Education', 'value': 'Education'},
                                    {'label': 'Mapping', 'value': 'Mapping'},
                                    {'label': 'Rescue', 'value': 'Rescue'},
                                    {'label': 'Entertainment', 'value': 'Entertainment'},
                                    {'label': 'Agricultural Task', 'value': 'Agricultural Task'},
                                    {'label': 'Construction', 'value': 'Construction'},
                                    {'label': 'Maintenance', 'value': 'Maintenance'},
                                    {'label': 'Environmental Monitoring', 'value': 'Environmental Monitoring'}
                                ],
                                value='all'
                            )
                        ])
                    ])
                ], width=4)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Robot Details"),
                        dbc.CardBody(id='robot-details')
                    ])
                ])
            ])
        ], fluid=True)
        
        @app.callback(
            Output('tree-graph', 'figure'),
            [Input('domain-filter', 'value'),
             Input('kingdom-filter', 'value'),
             Input('morpho_motion_filter', 'value'),
             Input('order-filter', 'value'),
             Input('sensing_family-filter', 'value'),
             Input('actuation_genus-filter', 'value'),
             Input('cognition_class-filter', 'value'),
             Input('application_species-filter', 'value')]
        )
        def update_tree(domain_filter, kingdom_filter, morpho_motion_filter, order_filter, sensing_family_filter, actuation_genus_filter, cognition_class_filter, application_species_filter):
            # Rebuild graph with filters
            self.build_taxonomy_tree()
            
            # Apply filters (simplified - in a real implementation, you'd filter the graph)
            fig = self.create_radial_tree_of_life()
            return fig
        
        @app.callback(
            Output('stats-content', 'children'),
            [Input('tree-graph', 'figure')]
        )
        def update_stats(figure):
            stats = [
                html.P(f"Total Robots: {len(self.robots_data)}"),
                html.P(f"Total Taxonomy Nodes: {len([n for n, d in self.graph.nodes(data=True) if d.get('type') == 'taxonomy'])}"),
                html.P(f"Total Connections: {len(self.graph.edges())}")
            ]
            return stats
        
        @app.callback(
            Output('robot-details', 'children'),
            [Input('tree-graph', 'clickData')]
        )
        def display_robot_details(click_data):
            if not click_data:
                return "Click on a robot node to see details"
            
            point = click_data['points'][0]
            node_name = point['text']
            
            # Find robot data
            for robot in self.robots_data:
                if robot['name'] == node_name:
                    return [
                        html.H5(robot['name']),
                        html.P(f"Manufacturer: {robot.get('manufacturer', 'Unknown')}"),
                        html.P(f"Description: {robot.get('description', 'No description available')}"),
                        html.H6("Classification:"),
                        html.Ul([
                            html.Li(f"Domain: {robot.get('domain', 'Unknown')}"),
                            html.Li(f"Kingdom: {robot.get('kingdom', 'Unknown')}"),
                            html.Li(f"Morpho_Motion_Class: {robot.get('morpho_motion_class', 'Unknown')}"),
                            html.Li(f"Order: {robot.get('order', 'Unknown')}"),
                            html.Li(f"Sensing_Family: {robot.get('sensing_family', 'Unknown')}"),
                            html.Li(f"Actuation_Genus: {robot.get('actuation_genus', 'Unknown')}"),
                            html.Li(f"Cognition_Class: {robot.get('cognition_class', 'Unknown')}"),
                            html.Li(f"Application_Species: {', '.join(robot.get('application_species', [])) if isinstance(robot.get('application_species'), list) else robot.get('application_species', 'Unknown')}")
                        ])
                    ]
            
            return f"Details for {node_name}"
        
        return app

if __name__ == "__main__":
    visualizer = RobotTreeVisualizer()
    visualizer.load_data('classified_robots_gpt.json')  # Loads GPT classification data
    visualizer.build_taxonomy_tree()  # Builds tree with GPT taxonomy
    
    if visualizer.robots_data:
        # Create PNG visualizations
        visualizer.save_radial_tree_as_png()
        visualizer.save_phylogenetic_tree_as_png()
        visualizer.save_dendrogram_as_png()
        visualizer.save_cluster_as_png()
        visualizer.save_taxonomy_bar_charts_as_png()
        visualizer.save_simplified_tree_as_png()
        visualizer.save_taxonomy_summary_as_png()
        print("✅ PNG visualizations created successfully!")
        
        # Create and run interactive dashboard
        print("\n🚀 Starting interactive dashboard...")
        print("Open your browser and go to: http://127.0.0.1:8050")
        app = visualizer.create_dashboard()
        app.run_server(debug=True, host='127.0.0.1', port=8050)
    else:
        print("No robot data found. Please run the scraper and classifier first.") 