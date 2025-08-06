#!/usr/bin/env python3
"""
GPT-based Robot Classifier

This standalone script uses OpenAI's GPT models to classify robots according to
a hierarchical taxonomy system. It processes robot data and outputs classified
results in JSON format.

Requirements:
- OpenAI API key set as environment variable OPENAI_API_KEY
- robots_data.json file in the data/ directory
"""

import json
import os
import sys
import argparse
from typing import Dict, Any, List
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    import openai
except ImportError:
    print("❌ Error: openai package not found. Install with: pip install openai")
    sys.exit(1)

class GPTClassifier:
    """GPT-based robot classifier using OpenAI's API."""
    
    def __init__(self, api_key: str, taxonomy_template: Dict[str, Any]):
        """
        Initialize the GPT classifier.
        
        Args:
            api_key: OpenAI API key
            taxonomy_template: Template defining the taxonomy structure
        """
        openai.api_key = api_key
        self.taxonomy_template = taxonomy_template

    def classify_robot(self, robot_info: Dict[str, Any], model: str = "gpt-4") -> Dict[str, Any]:
        """
        Classify a single robot using GPT.
        
        Args:
            robot_info: Robot information dictionary
            model: GPT model to use for classification
            
        Returns:
            Dictionary containing classification results
        """
        prompt = self._build_prompt(robot_info)

        try:
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a robotic classification assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            content = response.choices[0].message.content
            classification = json.loads(content)
        except json.JSONDecodeError as e:
            classification = {
                "error": f"JSON parsing error: {str(e)}",
                "raw_response": content if 'content' in locals() else "",
                "name": robot_info.get('name', 'Unknown')
            }
        except Exception as e:
            classification = {
                "error": f"API error: {str(e)}",
                "raw_response": content if 'content' in locals() else "",
                "name": robot_info.get('name', 'Unknown')
            }

        # Ensure all required fields exist
        for field, template_val in self.taxonomy_template.items():
            if field not in classification:
                classification[field] = [] if isinstance(template_val, list) else "MISSING"

        return classification

    def _build_prompt(self, robot_info: Dict[str, Any]) -> str:
        """
        Build the classification prompt for GPT.
        
        Args:
            robot_info: Robot information dictionary
            
        Returns:
            Formatted prompt string
        """
        info_text = json.dumps(robot_info, indent=2, ensure_ascii=False)
        schema = json.dumps(self.taxonomy_template, indent=2, ensure_ascii=False)
        
        return f"""
You are an expert in robotic systems taxonomy. Given the following robot metadata:

{info_text}

Classify the robot according to the **8-level robotic taxonomy** below.
You **MUST** return **only** a valid JSON object with **exactly** these 10 fields (no extra keys, no explanation):

{schema}

- "name": string (the robot's name)
- "url": string (the robot's url)
- "domain": one of (Physical | Virtual | Hybrid)
- "kingdom": one of (Industrial | Medical | Service | Military | Agriculture | Space | Marine | Research | Entertainment)
- "morpho_motion_class": one of (Wheeled-Mobile | Tracked-Mobile | Legged-Humanoid | Legged-Animaloid | Flying-Drone | Swimming-Soft | Modular-Lattice | Swarm-Agent)
- "order": one of (Manual | Teleoperated | Autonomous | Semi-Autonomous | Collaborative | Swarm-Based)
- "sensing_family": one of (Vision-Based | LiDAR-Based | Tactile-Based | GPS-Based | Acoustic-Based | Chemical-Based | Multimodal | Minimal Sensing)
- "actuation_genus": one of (Electric | Hydraulic | Pneumatic | Smart Materials | Bio-Hybrid | Magnetic | Passive | Hybrid Actuation)
- "cognition_class": one of (None | Rule-Based | Model-Based AI | AI-Powered | Adaptive Learning | Reinforcement Learning | Generative AI)
- "application_species": list of one or more from [Surgery, Inspection, Transport, Assembly, Exploration, Surveillance, Companionship, Education, Mapping, Rescue, Entertainment, Agricultural Task, Construction, Maintenance, Environmental Monitoring]

Ensure **all** fields appear, even if guessed. Output **only** the JSON.
""".strip()

def load_robot_data(data_path: str) -> List[Dict[str, Any]]:
    """
    Load robot data from JSON file.
    
    Args:
        data_path: Path to the JSON file
        
    Returns:
        List of robot dictionaries
        
    Raises:
        FileNotFoundError: If the data file doesn't exist
        json.JSONDecodeError: If the JSON is invalid
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Robot data file not found: {data_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {data_path}: {str(e)}", e.doc, e.pos)

def save_classified_data(results: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save classified data to JSON file.
    
    Args:
        results: List of classified robot dictionaries
        output_path: Path to save the output file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    """Main entry point for the GPT classifier script."""
    parser = argparse.ArgumentParser(
        description="GPT-based Robot Classifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gptclassifier.py
  python gptclassifier.py --input data/robots_data.json --output data/classified_robots_gpt.json
  python gptclassifier.py --model gpt-3.5-turbo
        """
    )
    
    parser.add_argument(
        '--input', 
        default='../data/robots_data.json',
        help='Input JSON file with robot data (default: ../data/robots_data.json)'
    )
    parser.add_argument(
        '--output', 
        default='../data/classified_robots_gpt.json',
        help='Output JSON file for classified data (default: ../data/classified_robots_gpt.json)'
    )
    parser.add_argument(
        '--model', 
        default='gpt-4',
        help='GPT model to use for classification (default: gpt-4)'
    )
    parser.add_argument(
        '--limit', 
        type=int,
        help='Limit number of robots to classify (for testing)'
    )
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Define taxonomy template
    taxonomy_template = {
        "name": "Robot Name",
        "url": "https://example.com",
        "domain": "Physical",
        "kingdom": "Medical",
        "morpho_motion_class": "Legged-Humanoid",
        "order": "Autonomous",
        "sensing_family": "Vision-Based",
        "actuation_genus": "Electric",
        "cognition_class": "AI-Powered",
        "application_species": ["Surgery"]
    }
    
    try:
        # Load robot data
        print(f"📂 Loading robot data from {args.input}...")
        robot_list = load_robot_data(args.input)
        
        if args.limit:
            robot_list = robot_list[:args.limit]
            print(f"🔢 Limiting to {args.limit} robots for testing")
        
        print(f"🤖 Found {len(robot_list)} robots to classify")
        
        # Initialize classifier
        classifier = GPTClassifier(api_key, taxonomy_template)
        
        # Classify robots
        print(f"🧠 Classifying robots using {args.model}...")
        results = []
        errors = 0
        
        for i, robot in enumerate(robot_list, 1):
            print(f"  Processing {i}/{len(robot_list)}: {robot.get('name', 'Unknown')}")
            
            res = classifier.classify_robot(robot, model=args.model)
            if "error" in res:
                errors += 1
                print(f"    ❌ Error: {res['error']}")
            
            results.append(res)
        
        # Save results
        print(f"💾 Saving results to {args.output}...")
        save_classified_data(results, args.output)
        
        # Print summary
        print(f"\n✅ Classification complete!")
        print(f"   Total robots: {len(results)}")
        print(f"   Successful: {len(results) - errors}")
        print(f"   Errors: {errors}")
        print(f"   Results saved to: {args.output}")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Classification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

