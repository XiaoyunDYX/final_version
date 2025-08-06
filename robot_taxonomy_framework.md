# 🤖 Robot Linnaean-Inspired Taxonomy Framework (Optimized 8-Level Structure)

This framework describes a principled, hierarchical taxonomy for classifying robots, inspired by biological Linnaean classification. Each level represents a distinct dimension of robotic identity or capability.

---

## 🧭 Level 1: Domain (Ontology Level)

**Definition:** The operational substrate where the robot exists and acts.

| Type     | Description                                                                                     |
| -------- | ----------------------------------------------------------------------------------------------- |
| Physical | Exists entirely in the real, physical world                                                     |
| Virtual  | Exists entirely in simulation or software                                                       |
| Hybrid   | Combines physical presence with virtual control or interface (e.g., telepresence, AR/VR robots) |

---

## 🏢 Level 2: Kingdom (Application Domain)

**Definition:** The societal or industrial domain in which the robot primarily operates.

| Type          | Description                                    |
| ------------- | ---------------------------------------------- |
| Industrial    | Manufacturing, logistics, warehouse            |
| Medical       | Surgery, rehabilitation, diagnostics           |
| Service       | Domestic, hospitality, customer service        |
| Military      | Surveillance, bomb disposal, tactical support  |
| Agriculture   | Crop monitoring, spraying, harvesting          |
| Space         | Planetary exploration, satellite servicing     |
| Marine        | Underwater operation, environmental monitoring |
| Research      | Academic or experimental robotics              |
| Entertainment | Games, education, social robots                |

---

## 🧱 Level 3: Morpho-Motion Class (Body Plan + Locomotion)

**Definition:** The physical configuration and its mode of movement.

| Type             | Description                                       |
| ---------------- | ------------------------------------------------- |
| Wheeled-Mobile   | Uses wheels for locomotion on flat terrain        |
| Tracked-Mobile   | Uses tracks for better traction and rough terrain |
| Legged-Humanoid  | Bipedal form, humanlike appearance and gait       |
| Legged-Animaloid | Quadruped or hexapod animal-inspired motion       |
| Flying-Drone     | Uses rotors or wings for aerial mobility          |
| Swimming-Soft    | Soft-bodied underwater mobility like an octopus   |
| Modular-Lattice  | Interconnected units that reshape structure       |
| Swarm-Agent      | Many small robots acting as one system            |
| Articulated Arm  | Jointed Manipulator, Mechanical Arm               |
| others-Static    | Any other static robots                           |
| others-Mobie     | some special robots like snake, Spherical-Rolling..|


---

## 🔧 Level 4: Order (Cognitive Agency Level)

**Definition:** The degree and method of control over the robot.

| Type            | Description                                              |
| --------------- | -------------------------------------------------------- |
| Manual          | Human physically operates or directly controls the robot |
| Teleoperated    | Controlled remotely by human input                       |
| Autonomous      | Makes decisions independently                            |
| Semi-Autonomous | Shared decision-making with human supervision            |
| Collaborative   | Works side-by-side with humans, adjusting based on input |
| Swarm-Based     | Collective behavior from decentralized agents            |

---

## 👁️ Level 5: Sensing Family (Primary Sensory Modality)

**Definition:** The dominant sensing modality enabling perception.

| Type            | Description                            |
| --------------- | -------------------------------------- |
| Vision-Based    | Uses cameras and image processing      |
| LiDAR-Based     | Uses laser scanning for depth mapping  |
| Tactile-Based   | Uses pressure, force, or touch sensors |
| GPS-Based       | Uses satellite navigation systems      |
| Acoustic-Based  | Uses sound/ultrasound sensors          |
| Chemical-Based  | Detects gases or chemical compounds    |
| Multimodal      | Integrates multiple sensing types      |
| Minimal Sensing | Limited or basic sensory capability    |

---

## 🔋 Level 6: Actuation Genus (Energetic-Mechanical Driver)

**Definition:** The primary actuation method for motion or action.

| Type             | Description                                                       |
| ---------------- | ----------------------------------------------------------------- |
| Electric         | Motors or servos powered by electricity                           |
| Hydraulic        | Uses pressurized fluid for force/motion                           |
| Pneumatic        | Uses compressed air for motion                                    |
| Smart Materials  | Uses shape-memory alloys, piezoelectrics, etc.                    |
| Bio-Hybrid       | Integrates living tissue or biological components                 |
| Magnetic         | Uses magnetic force to actuate or position                        |
| Passive          | Moves through gravity, external forces, or minimal internal power |
| Hybrid Actuation | Combines multiple actuation types                                 |

---

## 🧠 Level 7: Cognition Class (Cognitive Capability Level)

**Definition:** The internal processing, adaptation, and learning capacity of the robot.

| Type                   | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| None                   | No computation or intelligent behavior                         |
| Rule-Based             | Operates via predefined logic or decision trees                |
| Model-Based AI         | Uses planning or symbolic reasoning models                     |
| AI-Powered             | Uses machine learning models or inference systems              |
| Adaptive Learning      | Learns from new data or changes in the environment             |
| Reinforcement Learning | Optimizes behavior through feedback loops                      |
| Generative AI          | Capable of generating new outputs (e.g., conversation, images) |

---

## 🎯 Level 8: Application Species (Task Specialization)

**Definition:** The robot’s primary real-world function(s), supporting multi-label classification.

| Type                     | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| Surgery                  | Conducts or assists in medical operations            |
| Inspection               | Monitors structures, systems, or conditions          |
| Transport                | Moves goods or objects                               |
| Assembly                 | Builds or puts components together                   |
| Exploration              | Navigates unknown or remote environments             |
| Surveillance             | Observes or monitors areas and targets               |
| Companionship            | Provides social or emotional support                 |
| Education                | Aids in teaching or learning                         |
| Mapping                  | Creates spatial representations of environments      |
| Rescue                   | Participates in emergency or disaster response       |
| Entertainment            | Engages users in interactive experiences             |
| Agricultural Task        | Performs farm-specific jobs like spraying or seeding |
| Construction             | Assists in building infrastructure                   |
| Maintenance              | Conducts repair or upkeep operations                 |
| Environmental Monitoring | Tracks environmental parameters and hazards          |

---

## ✅ JSON Template for Classification

```json
{
  "name": "Robot Name",
  "domain": "Physical",
  "kingdom": "Medical",
  "morpho_motion_class": "Legged-Humanoid",
  "order": "Autonomous",
  "sensing_family": "Vision-Based",
  "actuation_genus": "Electric",
  "cognition_class": "AI-Powered",
  "application_species": ["Surgery"]
}
```

---

This classification framework supports robot discovery, clustering, visualization, and ontology construction for large-scale taxonomy projects such as "The Tree of Robotic Life."