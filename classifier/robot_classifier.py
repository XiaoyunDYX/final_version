#!/usr/bin/env python3
"""
Robot Classifier - Rule-based Classification System

This module provides rule-based classification of robots according to a hierarchical
taxonomy system. It uses keyword matching and heuristic rules to classify robots
into the appropriate taxonomic categories.
"""

import json
import re
from typing import Dict, List, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from collections import Counter, defaultdict

class RobotTaxonomy:
    """Manages the robot taxonomy structure and classification rules."""
    
    def __init__(self, taxonomy_file: str = "robot_taxonomy_framework.md"):
        """
        Initialize taxonomy from markdown file or use default taxonomy.
        
        Args:
            taxonomy_file: Path to the taxonomy markdown file
        """
        self.taxonomy_file = taxonomy_file
        self.taxonomy = self._parse_taxonomy_from_markdown()
        self.keywords = self._extract_keywords()
        
    def _parse_taxonomy_from_markdown(self) -> Dict[str, Any]:
        """
        Parse the taxonomy structure from the markdown file.
        
        Returns:
            Dictionary containing the taxonomy structure
        """
        try:
            with open(self.taxonomy_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Warning: Taxonomy file {self.taxonomy_file} not found. Using default taxonomy.")
            return self._get_default_taxonomy()
        
        # Parse the hierarchical structure from markdown
        taxonomy = {
            "Domain": {},
            "Kingdom": {},
            "Phylum": {},
            "Class": {},
            "Order": {},
            "Family": {},
            "Genus": {},
            "Species": {}
        }
        
        # Extract Domain level
        domain_match = re.search(r'### Domain Level: Operational Environment\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if domain_match:
            domain_section = domain_match.group(1)
            domains = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', domain_section)
            for domain, description in domains:
                taxonomy["Domain"][domain.strip()] = description.strip()
        
        # Extract Kingdom level
        kingdom_match = re.search(r'### Kingdom Level: Application Domains\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if kingdom_match:
            kingdom_section = kingdom_match.group(1)
            kingdoms = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', kingdom_section)
            for kingdom, description in kingdoms:
                taxonomy["Kingdom"][kingdom.strip()] = description.strip()
        
        # Extract Phylum level
        phylum_match = re.search(r'### Phylum Level: Morphological Structure\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if phylum_match:
            phylum_section = phylum_match.group(1)
            phyla = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', phylum_section)
            for phylum, description in phyla:
                taxonomy["Phylum"][phylum.strip()] = description.strip()
        
        # Extract Class level
        class_match = re.search(r'### Class Level: Locomotion Mechanism\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if class_match:
            class_section = class_match.group(1)
            classes = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', class_section)
            for class_type, description in classes:
                taxonomy["Class"][class_type.strip()] = description.strip()
        
        # Extract Order level
        order_match = re.search(r'### Order Level: Autonomy and Control\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if order_match:
            order_section = order_match.group(1)
            orders = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', order_section)
            for order, description in orders:
                taxonomy["Order"][order.strip()] = description.strip()
        
        # Extract Family level
        family_match = re.search(r'### Family Level: Sensing Modalities\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if family_match:
            family_section = family_match.group(1)
            families = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', family_section)
            for family, description in families:
                taxonomy["Family"][family.strip()] = description.strip()
        
        # Extract Genus level
        genus_match = re.search(r'### Genus Level: Actuation Systems\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if genus_match:
            genus_section = genus_match.group(1)
            genera = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', genus_section)
            for genus, description in genera:
                taxonomy["Genus"][genus.strip()] = description.strip()
        
        # Extract Species level
        species_match = re.search(r'### Species Level: Application Specialization\s*\n\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if species_match:
            species_section = species_match.group(1)
            species_list = re.findall(r'\*\*(.*?)\*\*: (.*?)(?=\n|$)', species_section)
            for species, description in species_list:
                taxonomy["Species"][species.strip()] = description.strip()
        
        return taxonomy
    
    def _get_default_taxonomy(self) -> Dict[str, Any]:
        """
        Get default taxonomy structure when markdown file is not available.
        
        Returns:
            Default taxonomy dictionary
        """
        return {
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
            "Phylum": {
                "Manipulator": "Articulated arm systems with fixed bases",
                "Mobile": "Systems capable of translocation and navigation",
                "Humanoid": "Human-like bipedal morphology",
                "Modular": "Reconfigurable systems with interchangeable components",
                "Swarm": "Collective systems operating as coordinated groups",
                "Soft": "Compliant, deformable structures with flexible materials",
                "Hybrid_Morphology": "Combined rigid-soft or multi-modal body plans"
            },
            "Class": {
                "Static": "Fixed position systems",
                "Wheeled": "Wheel-based locomotion",
                "Legged": "Leg-based locomotion",
                "Flying": "Aerial locomotion",
                "Swimming": "Aquatic locomotion",
                "Morphing": "Shape-changing locomotion"
            },
            "Order": {
                "Teleoperated": "Human-controlled operation",
                "Semi_Autonomous": "Partial autonomous operation with human oversight",
                "Autonomous": "Fully autonomous operation",
                "Collaborative": "Human-robot collaborative operation"
            },
            "Family": {
                "Vision_Based": "Cameras and visual processing systems",
                "LiDAR_Based": "Laser-based distance and mapping systems",
                "Tactile_Based": "Touch and force sensing systems",
                "Multimodal": "Integration of multiple sensing technologies",
                "Minimal_Sensing": "Simple sensors with basic environmental awareness",
                "GPS_Navigation": "Satellite-based positioning systems",
                "Acoustic_Based": "Sound and ultrasonic sensing systems",
                "Chemical_Sensing": "Detection of chemical compounds and gases"
            },
            "Genus": {
                "Electric": "Electric motors and servo systems",
                "Hydraulic": "Fluid pressure-based actuation",
                "Pneumatic": "Compressed air actuation",
                "Hybrid_Actuation": "Combination of multiple actuation methods",
                "Smart_Materials": "Shape memory alloys, piezoelectric actuators",
                "Bio_Hybrid": "Integration of biological and artificial components",
                "Passive": "No active actuation, gravity or environmental forces",
                "Magnetic": "Magnetic field-based actuation"
            },
            "Species": {
                "Surgery": "Surgical procedures and medical interventions",
                "Inspection": "Quality control and inspection tasks",
                "Transport": "Material and object transportation",
                "Assembly": "Manufacturing and assembly operations",
                "Exploration": "Environmental and spatial exploration",
                "Surveillance": "Monitoring and security applications",
                "Companionship": "Social interaction and companionship",
                "Education": "Educational and training applications",
                "Mapping": "Environmental mapping and surveying",
                "Rescue": "Search and rescue operations",
                "Entertainment": "Recreational and entertainment purposes",
                "Agricultural_Task": "Farming and agricultural operations",
                "Construction": "Building and construction tasks",
                "Maintenance": "Equipment and infrastructure maintenance",
                "Environmental_Monitoring": "Environmental data collection and monitoring"
            }
        }
    
    def _extract_keywords(self) -> Dict[str, List[str]]:
        """
        Extract keywords for each taxonomy level for classification.
        
        Returns:
            Dictionary mapping taxonomy levels to keyword lists
        """
        keywords = {
            "Domain": {
                "Physical": ["physical", "real", "hardware", "mechanical", "material"],
                "Virtual": ["virtual", "software", "simulation", "digital", "computer"],
                "Hybrid": ["hybrid", "mixed", "augmented", "telepresence", "ar", "vr"]
            },
            "Kingdom": {
                "Industrial": ["industrial", "manufacturing", "factory", "production", "assembly"],
                "Service": ["service", "domestic", "household", "assistance", "help"],
                "Medical": ["medical", "surgical", "healthcare", "hospital", "therapy"],
                "Military": ["military", "defense", "security", "tactical", "combat"],
                "Research": ["research", "experimental", "laboratory", "scientific"],
                "Entertainment": ["entertainment", "toy", "game", "recreation", "fun"],
                "Agriculture": ["agriculture", "farming", "crop", "harvest", "agricultural"],
                "Space": ["space", "satellite", "planetary", "extraterrestrial", "orbit"],
                "Marine": ["marine", "underwater", "submarine", "aquatic", "ocean"]
            },
            "Phylum": {
                "Manipulator": ["manipulator", "arm", "articulated", "fixed", "stationary"],
                "Mobile": ["mobile", "moving", "navigation", "locomotion"],
                "Humanoid": ["humanoid", "human-like", "bipedal", "anthropomorphic"],
                "Modular": ["modular", "reconfigurable", "interchangeable", "adaptable"],
                "Swarm": ["swarm", "collective", "multiple", "coordinated", "group"],
                "Soft": ["soft", "flexible", "deformable", "compliant", "elastic"],
                "Hybrid_Morphology": ["hybrid", "combined", "multi-modal", "mixed"]
            },
            "Class": {
                "Static": ["static", "fixed", "stationary", "immobile"],
                "Wheeled": ["wheel", "wheeled", "rolling", "car", "vehicle"],
                "Legged": ["leg", "legged", "walking", "bipedal", "quadrupedal"],
                "Flying": ["flying", "aerial", "drone", "helicopter", "aircraft"],
                "Swimming": ["swimming", "aquatic", "underwater", "submarine"],
                "Morphing": ["morphing", "shape-changing", "transformable"]
            },
            "Order": {
                "Teleoperated": ["teleoperated", "remote", "controlled", "manual", "human-controlled"],
                "Semi_Autonomous": ["semi-autonomous", "partial", "assisted", "supervised"],
                "Autonomous": ["autonomous", "independent", "self-driving", "automatic"],
                "Collaborative": ["collaborative", "cooperative", "human-robot", "interactive"]
            },
            "Family": {
                "Vision_Based": ["vision", "camera", "visual", "image", "optical"],
                "LiDAR_Based": ["lidar", "laser", "radar", "distance", "scanning"],
                "Tactile_Based": ["tactile", "touch", "force", "pressure", "contact"],
                "Multimodal": ["multimodal", "multiple", "sensors", "integrated"],
                "Minimal_Sensing": ["minimal", "simple", "basic", "limited"],
                "GPS_Navigation": ["gps", "navigation", "positioning", "satellite"],
                "Acoustic_Based": ["acoustic", "sound", "audio", "ultrasonic"],
                "Chemical_Sensing": ["chemical", "gas", "sensor", "detection"]
            },
            "Genus": {
                "Electric": ["electric", "motor", "servo", "battery", "electronic"],
                "Hydraulic": ["hydraulic", "fluid", "pressure", "pump"],
                "Pneumatic": ["pneumatic", "air", "compressed", "pneumatic"],
                "Hybrid_Actuation": ["hybrid", "mixed", "combined", "actuation"],
                "Smart_Materials": ["smart", "material", "shape", "memory", "piezoelectric"],
                "Bio_Hybrid": ["bio", "biological", "organic", "living"],
                "Passive": ["passive", "gravity", "environmental", "no actuation"],
                "Magnetic": ["magnetic", "magnet", "field", "electromagnetic"]
            },
            "Species": {
                "Surgery": ["surgery", "surgical", "medical", "operation", "procedure"],
                "Inspection": ["inspection", "quality", "control", "check", "examine"],
                "Transport": ["transport", "carry", "move", "delivery", "logistics"],
                "Assembly": ["assembly", "manufacturing", "production", "build"],
                "Exploration": ["exploration", "explore", "discovery", "investigation"],
                "Surveillance": ["surveillance", "monitor", "security", "watch"],
                "Companionship": ["companionship", "social", "interaction", "companion"],
                "Education": ["education", "teaching", "learning", "training"],
                "Mapping": ["mapping", "survey", "map", "topography"],
                "Rescue": ["rescue", "emergency", "search", "save"],
                "Entertainment": ["entertainment", "fun", "game", "recreation"],
                "Agricultural_Task": ["agriculture", "farming", "crop", "harvest"],
                "Construction": ["construction", "building", "construction"],
                "Maintenance": ["maintenance", "repair", "service", "upkeep"],
                "Environmental_Monitoring": ["environmental", "monitoring", "climate", "pollution"]
            }
        }
        return keywords

class RobotClassifier:
    """Main robot classification system using rule-based approach."""
    
    def __init__(self, taxonomy_file: str = "robot_taxonomy_framework.md"):
        """
        Initialize the robot classifier.
        
        Args:
            taxonomy_file: Path to the taxonomy markdown file
        """
        self.taxonomy = RobotTaxonomy(taxonomy_file)
        self.classified_robots = []
        
    def classify_robots(self, robots_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classify a list of robots according to the taxonomy.
        
        Args:
            robots_data: List of robot dictionaries to classify
            
        Returns:
            List of classified robot dictionaries
        """
        classified_robots = []
        
        for robot in robots_data:
            classified_robot = self.classify_robot(robot)
            classified_robots.append(classified_robot)
        
        self.classified_robots = classified_robots
        return classified_robots
    
    def classify_robot(self, robot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a single robot according to the taxonomy.
        
        Args:
            robot_data: Robot information dictionary
            
        Returns:
            Classified robot dictionary with taxonomy fields
        """
        # Extract text for analysis
        text = self._extract_text(robot_data)
        
        # Classify each taxonomic level
        classification = {
            "name": robot_data.get("name", "Unknown"),
            "url": robot_data.get("url", ""),
            "description": robot_data.get("description", ""),
            "domain": self._classify_domain(text, robot_data),
            "kingdom": self._classify_kingdom(text, robot_data),
            "phylum": self._classify_phylum(text, robot_data),
            "class": self._classify_class(text, robot_data),
            "order": self._classify_order(text, robot_data),
            "family": self._classify_family(text, robot_data),
            "genus": self._classify_genus(text, robot_data),
            "species": self._classify_species(text, robot_data)
        }
        
        return classification
    
    def _extract_text(self, robot_data: Dict[str, Any]) -> str:
        """
        Extract all text content from robot data for analysis.
        
        Args:
            robot_data: Robot information dictionary
            
        Returns:
            Combined text string for analysis
        """
        text_parts = []
        
        # Add name
        if robot_data.get("name"):
            text_parts.append(robot_data["name"])
        
        # Add description
        if robot_data.get("description"):
            text_parts.append(robot_data["description"])
        
        # Add any additional text fields
        for key, value in robot_data.items():
            if isinstance(value, str) and key not in ["name", "description", "url"]:
                text_parts.append(value)
        
        return " ".join(text_parts).lower()
    
    def _classify_domain(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the domain level."""
        text_lower = text.lower()
        
        # Check for virtual/software robots
        if any(word in text_lower for word in ["virtual", "software", "simulation", "digital"]):
            return "Virtual"
        
        # Check for hybrid systems
        if any(word in text_lower for word in ["hybrid", "mixed", "augmented", "telepresence"]):
            return "Hybrid"
        
        # Default to physical
        return "Physical"
    
    def _classify_kingdom(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the kingdom level."""
        text_lower = text.lower()
        
        # Check each kingdom with keywords
        kingdom_keywords = self.taxonomy.keywords["Kingdom"]
        
        for kingdom, keywords in kingdom_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return kingdom
        
        # Default classification based on common patterns
        if any(word in text_lower for word in ["surgery", "medical", "hospital"]):
            return "Medical"
        elif any(word in text_lower for word in ["factory", "manufacturing", "industrial"]):
            return "Industrial"
        elif any(word in text_lower for word in ["service", "assistance", "help"]):
            return "Service"
        else:
            return "Research"  # Default fallback
    
    def _classify_phylum(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the phylum level."""
        text_lower = text.lower()
        
        # Check each phylum with keywords
        phylum_keywords = self.taxonomy.keywords["Phylum"]
        
        for phylum, keywords in phylum_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return phylum
        
        # Default classification
        if any(word in text_lower for word in ["humanoid", "human-like", "bipedal"]):
            return "Humanoid"
        elif any(word in text_lower for word in ["arm", "manipulator", "gripper"]):
            return "Manipulator"
        else:
            return "Mobile"  # Default fallback
    
    def _classify_class(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the class level."""
        text_lower = text.lower()
        
        # Check each class with keywords
        class_keywords = self.taxonomy.keywords["Class"]
        
        for class_type, keywords in class_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return class_type
        
        # Default classification
        if any(word in text_lower for word in ["wheel", "car", "vehicle"]):
            return "Wheeled"
        elif any(word in text_lower for word in ["leg", "walking", "bipedal"]):
            return "Legged"
        else:
            return "Static"  # Default fallback
    
    def _classify_order(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the order level."""
        text_lower = text.lower()
        
        # Check each order with keywords
        order_keywords = self.taxonomy.keywords["Order"]
        
        for order, keywords in order_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return order
        
        # Default classification
        if any(word in text_lower for word in ["autonomous", "automatic", "self"]):
            return "Autonomous"
        elif any(word in text_lower for word in ["remote", "controlled", "manual"]):
            return "Teleoperated"
        else:
            return "Semi_Autonomous"  # Default fallback
    
    def _classify_family(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the family level."""
        text_lower = text.lower()
        
        # Check each family with keywords
        family_keywords = self.taxonomy.keywords["Family"]
        
        for family, keywords in family_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return family
        
        # Default classification
        if any(word in text_lower for word in ["camera", "vision", "image"]):
            return "Vision_Based"
        else:
            return "Minimal_Sensing"  # Default fallback
    
    def _classify_genus(self, text: str, robot_data: Dict[str, Any]) -> str:
        """Classify the genus level."""
        text_lower = text.lower()
        
        # Check each genus with keywords
        genus_keywords = self.taxonomy.keywords["Genus"]
        
        for genus, keywords in genus_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return genus
        
        # Default classification
        if any(word in text_lower for word in ["motor", "electric", "battery"]):
            return "Electric"
        else:
            return "Electric"  # Default fallback
    
    def _classify_species(self, text: str, robot_data: Dict[str, Any]) -> List[str]:
        """Classify the species level (can be multiple)."""
        text_lower = text.lower()
        species_list = []
        
        # Check each species with keywords
        species_keywords = self.taxonomy.keywords["Species"]
        
        for species, keywords in species_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                species_list.append(species)
        
        # If no species found, add default based on kingdom
        if not species_list:
            kingdom = self._classify_kingdom(text, robot_data)
            if kingdom == "Medical":
                species_list.append("Surgery")
            elif kingdom == "Industrial":
                species_list.append("Assembly")
            elif kingdom == "Service":
                species_list.append("Companionship")
            else:
                species_list.append("Research")
        
        return species_list
    
    def cluster_robots(self, n_clusters: int = 5) -> Dict[str, Any]:
        """
        Perform clustering analysis on classified robots.
        
        Args:
            n_clusters: Number of clusters to create
            
        Returns:
            Dictionary containing clustering information
        """
        if not self.classified_robots:
            return {"error": "No classified robots available"}
        
        # Prepare data for clustering
        texts = []
        for robot in self.classified_robots:
            text = f"{robot.get('name', '')} {robot.get('description', '')}"
            texts.append(text)
        
        # Vectorize text data
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        try:
            X = vectorizer.fit_transform(texts)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X)
            
            # Organize results
            clusters = defaultdict(list)
            for i, label in enumerate(cluster_labels):
                clusters[f"cluster_{label}"].append(self.classified_robots[i])
            
            return {
                "n_clusters": n_clusters,
                "cluster_labels": cluster_labels.tolist(),
                "clusters": dict(clusters),
                "feature_names": vectorizer.get_feature_names_out().tolist()
            }
            
        except Exception as e:
            return {"error": f"Clustering failed: {str(e)}"}
    
    def save_classified_data(self, filename: str = 'data/classified_robots.json'):
        """Save classified robot data to JSON file."""
        if not self.classified_robots:
            print("Warning: No classified robots to save")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.classified_robots, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(self.classified_robots)} classified robots to {filename}")
    
    def get_taxonomy_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the classification.
        
        Returns:
            Dictionary containing taxonomy summary statistics
        """
        if not self.classified_robots:
            return {"error": "No classified robots available"}
        
        summary = {
            "total_robots": len(self.classified_robots),
            "domain_distribution": Counter(robot.get('domain', 'Unknown') for robot in self.classified_robots),
            "kingdom_distribution": Counter(robot.get('kingdom', 'Unknown') for robot in self.classified_robots),
            "phylum_distribution": Counter(robot.get('phylum', 'Unknown') for robot in self.classified_robots),
            "class_distribution": Counter(robot.get('class', 'Unknown') for robot in self.classified_robots),
            "order_distribution": Counter(robot.get('order', 'Unknown') for robot in self.classified_robots),
            "family_distribution": Counter(robot.get('family', 'Unknown') for robot in self.classified_robots),
            "genus_distribution": Counter(robot.get('genus', 'Unknown') for robot in self.classified_robots),
            "species_distribution": Counter()
        }
        
        # Count species (can be multiple per robot)
        for robot in self.classified_robots:
            species_list = robot.get('species', [])
            if isinstance(species_list, list):
                for species in species_list:
                    summary["species_distribution"][species] += 1
            elif species_list:
                summary["species_distribution"][species_list] += 1
        
        return summary
    
    def get_taxonomy_structure(self) -> Dict[str, Any]:
        """
        Get the complete taxonomy structure.
        
        Returns:
            Dictionary containing the taxonomy structure
        """
        return self.taxonomy.taxonomy 