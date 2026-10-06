# Autonomous Patrol & Surveillance Agent for Campus Security

## Project Overview

An AI-based autonomous campus security system that intelligently selects patrol destinations, responds to security incidents, manages battery constraints, explains its decisions, and coordinates multiple patrol agents.

The system uses a utility-based decision-making approach to select patrol destinations by considering security risk, patrol coverage, live alerts, travel cost, revisit time, and battery constraints.

The project also compares random, fixed-route, and utility-based patrol strategies and extends the system to multiple coordinated agents.

---

## Objectives

The main objectives of this project are:

1. Develop a virtual campus environment.
2. Implement an autonomous security patrol agent.
3. Implement a random patrol baseline.
4. Implement a fixed-route patrol baseline.
5. Implement a utility-based patrol strategy.
6. Incorporate live security incidents and alerts.
7. Implement battery consumption and charging.
8. Provide explainable AI decisions.
9. Extend the system to multiple coordinated patrol agents.
10. Measure and compare patrol performance experimentally.
11. Develop an interactive monitoring dashboard.
12. Test the system using automated tests.

---

## AI Approach

The primary decision-making component is a utility-based autonomous agent.

For every possible destination, the agent evaluates multiple factors and calculates an overall utility score.

The current utility weights are:

| Factor | Weight |
|---|---:|
| Security Risk | 0.25 |
| Patrol Coverage | 0.20 |
| Live Alert | 0.40 |
| Travel Cost | 0.10 |
| Battery Constraint | 0.05 |

The destination with the highest utility score among reachable locations is selected.

This allows the agent to dynamically adapt its patrol decisions instead of following only a predetermined route.

---

## Campus Environment

The campus is represented as a weighted graph using NetworkX.

The simulated campus contains the following locations:

- Main Gate
- Academic Block
- Library
- Hostel
- Canteen
- Parking
- Sports Ground
- Administration
- Security Office

The edges between locations represent paths, and their weights represent travel distance or movement cost.

Shortest-path calculations are used when the agent moves between locations.

---

## Patrol Strategies

The project implements three patrol strategies.

### 1. Random Patrol

The random patrol agent selects a destination randomly.

This provides a stochastic baseline for comparison.

### 2. Fixed Route Patrol

The fixed-route agent follows a predefined sequence of campus locations.

This provides a deterministic baseline.

### 3. Utility-Based Patrol

The utility-based agent dynamically selects destinations using:

- Security risk
- Patrol coverage
- Area revisit time
- Live security alerts
- Travel cost
- Battery constraints

The three strategies are evaluated using repeated simulation trials.

---

## Security Incident Management

The system supports the following incident types:

- Unauthorized Entry
- Suspicious Activity
- Fire Alert
- Emergency

Each incident has a priority level.

The utility-based agent considers active incidents when selecting its next destination.

When the agent reaches the location of an active incident, the incident is automatically resolved.

The system records:

- Incident type
- Incident location
- Priority
- Detection step
- Resolution step
- Response time

Response time is measured in patrol steps.

---

## Battery Management

The autonomous agent operates under a battery constraint.

The battery management system supports:

- Battery capacity
- Initial battery charge
- Battery consumption
- Low-battery detection
- Charging station
- Automatic recharging

Movement consumes battery based on travel distance.

If the agent does not have sufficient battery to reach a destination, the movement is prevented.

The agent can travel to the charging station and recharge its battery.

---

## Explainable AI

The system provides an explanation for the autonomous agent's decisions.

For each decision, the system can display:

- Selected destination
- Final utility score
- Security risk score
- Coverage score
- Live alert score
- Revisit time
- Travel cost
- Battery cost
- Utility weights

The system also generates a human-readable explanation describing the important factors behind the selected destination.

This improves transparency and allows users to understand why the autonomous agent selected a particular location.

---

## Multi-Agent Coordination

The project extends the autonomous patrol system to multiple agents.

Two utility-based patrol agents are used.

### Agent 1

Starting location:

`Main Gate`

### Agent 2

Starting location:

`Security Office`

The campus is divided into territories.

Each agent prioritizes destinations belonging to its assigned territory.

The system tracks:

- Agent-specific territory coverage
- Total campus coverage
- Visited locations
- Patrol distance
- Battery usage
- Overlapping locations

The coordination mechanism also attempts to prevent both agents from selecting the same destination.

---

## Experimental Evaluation

The project uses repeated simulation trials to compare patrol strategies.

The main metrics include:

- Average patrol distance
- Average unique areas covered
- Total patrol visits
- Average final battery
- Campus coverage
- Territory coverage
- Average overlap

Experimental results are stored as CSV files in the `results` directory.

The project does not assume that one strategy is universally superior.

Instead, the strategies are compared using multiple performance metrics.

---

## Interactive Dashboard

The project includes a Streamlit dashboard for monitoring and demonstrating the autonomous security system.

The dashboard provides:

### System Monitoring

- Current agent location
- Battery level
- Patrol distance
- Patrol steps
- Active security alerts

### Campus Visualization

- Campus locations
- Campus paths
- Current agent position
- Patrol history

### Security Monitoring

- Active incidents
- Incident priorities
- Incident response status
- Incident response time

### AI Analysis

- Utility scores
- Selected destination
- Decision factors
- Explainability information

### Patrol Strategy Comparison

- Random Patrol
- Fixed Route
- Utility Based
- Average distance
- Average unique areas covered
- Average final battery

### Multi-Agent Analysis

- Total campus coverage
- Agent 1 territory coverage
- Agent 2 territory coverage
- Average patrol distance
- Average battery remaining
- Average overlap

---

## Testing

The project includes an automated test suite using Pytest.

The tests cover major components including:

- Campus environment
- Battery management
- Security agent
- Incident management
- Utility-based agent
- Multi-agent coordination
- Incident response metrics
- Full patrol functionality

Run the tests using:

```bash
pytest -q

Project Structure
Autonomous_Campus_Security/
│
├── src/
│   ├── environment.py
│   ├── agent.py
│   ├── battery.py
│   ├── incidents.py
│   ├── random_patrol.py
│   ├── fixed_patrol.py
│   ├── utility_agent.py
│   ├── explainability.py
│   └── multi_agent.py
│
├── dashboard/
│   └── app.py
│
├── experiments/
│   ├── evaluate_patrol.py
│   └── evaluate_multi_agent.py
│
├── results/
│   ├── patrol_results.csv
│   └── multi_agent_results.csv
│
├── tests/
│   └── test_project.py
│
├── data/
│
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore

Technologies Used
Technology	Purpose
Python	Core implementation
NetworkX	Campus graph and shortest-path calculations
Streamlit	Interactive dashboard
Plotly	Data visualization
Pandas	Experimental data processing
Pytest	Automated testing
Git	Version control
GitHub	Source-code management


Installation
1. Clone the repository
git clone https://github.com/kodumurinagasaivignesh/Autonomous_Campus_Security.git

2. Enter the project directory
cd Autonomous_Campus_Security

3. Create a virtual environment
python -m venv venv

4. Activate the virtual environment
For Windows PowerShell:
venv\Scripts\Activate.ps1

5. Install dependencies
pip install -r requirements.txt

Running the Project
Run the utility-based patrol agent
python src/utility_agent.py

Run the multi-agent patrol system
python src/multi_agent.py

Run patrol strategy evaluation
python experiments/evaluate_patrol.py

Run multi-agent evaluation
python experiments/evaluate_multi_agent.py

Run the dashboard
streamlit run dashboard/app.py

Running Tests
Run:
pytest -q

The test suite validates the major components of the autonomous security system.
Responsible AI
The project considers several responsible AI principles.
Explainability
The system provides explanations for autonomous patrol decisions.
Transparency
The utility factors and their weights are visible and documented.
Human Oversight
The system is designed as an academic prototype and decision-support system rather than a replacement for human security personnel.
Safety
The current system operates in a simulated campus environment and does not directly control physical security infrastructure.
Privacy
The current prototype does not process real CCTV footage, personal information, or biometric data.
Limitations
The current prototype has several limitations:
1. The campus environment is simulated.
2. Security risk values are predefined.
3. Security incidents are simulated.
4. Battery consumption is simplified.
5. Patrol movement occurs in a discrete simulation.
6. Real camera and sensor feeds are not connected.
7. Multi-agent communication is simulated.
8. The system has not been deployed on a physical robot.
9. Real-world security conditions may differ significantly from the simulation.
Therefore, the current implementation should be considered an academic and research prototype rather than a production security system.
Future Improvements
Future versions could include:
- Real campus map integration
- GPS or indoor localization
- Computer vision-based incident detection
- CCTV integration
- Real-time sensor streams
- Dynamic risk prediction
- Reinforcement learning for patrol optimization
- Advanced multi-agent coordination
- Real robot integration
- Real-time security notifications
- Edge AI deployment
- Privacy-preserving surveillance
- Human-in-the-loop decision making
- Fail-safe mechanisms
System Workflow
Campus Environment
        |
        v
Autonomous Patrol Agent
        |
        v
Risk + Coverage + Alerts
        |
        v
Utility Calculation
        |
        v
Destination Selection
        |
        v
Patrol Movement
        |
        +------> Battery Management
        |
        +------> Incident Response
        |
        v
Explainable Decision
        |
        v
Performance Evaluation
        |
        v
Multi-Agent Coordination
        |
        v
Dashboard Visualization

Project Outcome
The completed prototype demonstrates an end-to-end autonomous campus patrol system capable of:
- Modeling a campus environment
- Selecting patrol destinations autonomously
- Comparing different patrol strategies
- Responding to security incidents
- Managing battery constraints
- Explaining AI decisions
- Coordinating multiple patrol agents
- Measuring patrol performance
- Visualizing system behavior through an interactive dashboard
Team
Group 13
Student	Registration Number
Kodumuri Naga Sai Vignesh	12523653
Dhruv Choudhary	12523903
Third Team Member	To be added


Academic Information
Course: CSE276 - Artificial Intelligence Foundations
Project: Autonomous Patrol & Surveillance Agent for Campus Security
Institution: Lovely Professional University
Academic Session: 2026-27
License
This project is developed for academic and educational purposes.

