Autonomous Patrol & Surveillance Agent for Campus Security

<p align="center">
  <strong>An AI-powered autonomous campus security patrol simulation with intelligent decision-making, incident response, battery management, explainable AI, and multi-agent coordination.</strong>
</p>

<p align="center">
  <a href="https://autonomous-campus-security.onrender.com/">Live Dashboard</a> •
  <a href="https://github.com/kodumurinagasaivignesh/Autonomous_Campus_Security">GitHub Repository</a>
</p>

1. Project Overview

The Autonomous Patrol & Surveillance Agent for Campus Security is an AI-based academic project that simulates autonomous security patrol operations in a university campus environment.

The system models a campus as a weighted graph and uses intelligent agents to select patrol destinations, monitor simulated security incidents, manage battery resources, and coordinate patrol activities.

It implements and compares three patrol strategies:

Random Patrol

Fixed Route Patrol

Utility-Based Patrol

The project also introduces a two-agent patrol system in which agents operate in assigned campus territories to improve area coverage and reduce overlapping patrols.

An interactive Streamlit dashboard provides real-time visualization of the simulated environment, patrol activity, incidents, battery status, AI decisions, and experimental results.

2. Project Objectives

Develop a graph-based virtual campus environment.

Implement autonomous security patrol agents.

Compare random, fixed-route, and utility-based strategies.

Simulate security incidents and incident response.

Implement battery consumption and automatic charging.

Explain the reasoning behind autonomous decisions.

Develop a coordinated multi-agent patrol system.

Evaluate patrol performance using repeated experiments.

Build an interactive monitoring dashboard.

Validate system functionality through automated testing.

3. System Architecture

The system follows this general workflow:

              Campus Environment
                      |
                      v
             Autonomous Patrol Agent
                      |
                      v
          Risk, Coverage and Live Alerts
                      |
                      v
              Utility Calculation
                      |
                      v
             Destination Selection
                      |
                      v
                Patrol Movement
                 /     |      \
                /      |       \
               v       v        v
          Battery   Incident   Explainable
          Manager   Response      AI
                \      |       /
                 \     |      /
                      v
              Performance Evaluation
                      |
                      v
             Multi-Agent Coordination
                      |
                      v
              Streamlit Dashboard

Main components

Component

Responsibility

Campus Environment

Represents campus locations and paths as a weighted graph

Patrol Agent

Selects destinations and performs patrol movements

Utility Agent

Evaluates possible destinations using utility scores

Incident Manager

Creates and manages simulated security incidents

Battery Manager

Tracks battery consumption and charging

Explainability Module

Provides human-readable explanations for decisions

Multi-Agent Module

Coordinates two patrol agents

Experiment Module

Evaluates patrol strategies and calculates metrics

Dashboard

Visualizes system operations and results

4. Campus Environment

The campus is represented using a weighted graph implemented with NetworkX.

The simulated environment contains nine locations:

Main Gate

Academic Block

Library

Hostel

Canteen

Parking

Sports Ground

Administration

Security Office

Graph edges represent connections between campus locations. Edge weights represent travel distance or movement cost.

Shortest-path calculations are used to determine movement between locations.

5. AI Decision-Making Approach

The primary intelligent decision-making approach is Utility-Based Agent Design.

Instead of following only a fixed route, the utility-based agent evaluates possible destinations using multiple factors and selects the destination with the highest utility score.

Utility function

The implemented utility function is:

[
U(d)=0.25R(d)+0.20C(d)+0.40A(d)-0.10T(d)-0.05B(d)
]

Where:

Symbol

Factor

Weight

R(d)

Security Risk

0.25

C(d)

Patrol Coverage

0.20

A(d)

Live Alert Priority

0.40

T(d)

Travel Cost

0.10

B(d)

Battery Cost

0.05

The weights sum to 1.00.

Positive factors increase destination utility, while travel and battery costs reduce it.

The agent considers these factors to make context-aware patrol decisions rather than selecting destinations randomly or following only a predefined route.

Note: The utility factors use predefined scoring and cost values in the current simulation. The weights are configurable design parameters, not a claim of experimentally optimized weights.

6. Patrol Strategies

Three patrol strategies are implemented and evaluated.

6.1 Random Patrol

Selects patrol destinations randomly.

Provides a stochastic baseline.

Helps evaluate performance without intelligent destination prioritization.

6.2 Fixed Route Patrol

Follows a predefined sequence of campus locations.

Provides a deterministic baseline.

Provides consistent patrol coverage under the configured route.

6.3 Utility-Based Patrol

Calculates destination utility scores.

Considers security risk and patrol coverage.

Prioritizes active security alerts.

Considers travel and battery costs.

Selects the highest-utility reachable destination.

7. Security Incident Management

The system supports four simulated security incident types:

Incident

Description

Unauthorized Entry

Simulates unauthorized access to a campus location

Suspicious Activity

Represents suspicious behavior requiring attention

Fire Alert

Simulates a fire-related emergency

Emergency

Represents a high-priority emergency situation

The incident management system records:

Incident type

Incident location

Priority

Detection step

Resolution step

Response time

Incident response time is measured in simulation patrol steps.

The utility-based agent considers active incidents when selecting its next destination.

When an agent reaches an active incident location, the incident can be resolved by the simulation.

8. Battery Management

Battery management ensures that patrol agents operate within available energy constraints.

The system supports:

Battery capacity

Initial battery charge

Battery consumption

Low-battery detection

Charging station navigation

Automatic recharging

Movement consumes battery according to travel distance.

If an agent does not have sufficient battery to complete a movement, that movement is prevented. Agents can return to the charging station to recharge.

9. Explainable AI

The system includes an explainability component to make autonomous decisions understandable.

For each utility-based decision, the system can display:

Selected destination

Final utility score

Security risk score

Patrol coverage score

Live alert score

Revisit information

Travel cost

Battery cost

Utility weights

The dashboard also presents human-readable explanations describing why a particular destination was selected.

This improves transparency and helps users understand the factors influencing autonomous patrol decisions.

10. Multi-Agent Coordination

The project extends single-agent patrol into a two-agent coordinated system.

Two utility-based agents are used:

Agent

Starting Location

Agent 1

Main Gate

Agent 2

Security Office

The campus is divided into territories, and each agent prioritizes locations assigned to its territory.

The multi-agent system tracks:

Individual territory coverage

Total campus coverage

Visited locations

Patrol distance

Battery consumption

Overlapping locations

The coordination mechanism also attempts to prevent both agents from selecting the same destination.

11. Experimental Evaluation

The project evaluates patrol performance using repeated simulation trials.

Experimental configuration

Parameter

Configuration

Patrol strategies

3

Trials per strategy

10

Steps per trial

10

Campus locations

9

Multi-agent trials

10

Evaluation metrics

Average patrol distance

Average unique campus areas visited

Average total visits

Average final battery

Campus coverage percentage

Individual territory coverage

Average overlap count

11.1 Patrol Strategy Comparison

The following table presents the measured average results from the 10-trial evaluation.

Metric

Random Patrol

Fixed Route

Utility-Based

Average Distance

62.30

30.00

50.00

Average Unique Areas

6.70

7.00

6.00

Average Total Visits

10.00

10.00

10.00

Average Final Battery

37.70

70.00

50.00

Campus Coverage

74.44%

77.78%

66.67%

Campus coverage is calculated as:

[
\text{Coverage}=\frac{\text{Average Unique Areas Visited}}{9}\times100
]

11.2 Experimental Result Charts

Average Patrol Distance



Average Unique Areas Covered



Average Final Battery



11.3 Result Analysis

The experimental results show that:

Fixed Route Patrol achieved the lowest average travel distance of 30.00.

Fixed Route Patrol also achieved the highest average number of unique areas visited, at 7.00.

Fixed Route Patrol retained the highest average final battery of 70.00.

Utility-Based Patrol achieved a lower average distance and higher remaining battery than Random Patrol.

Random Patrol achieved 6.70 unique areas, compared with 6.00 for Utility-Based Patrol.

Under the current simulation configuration, Fixed Route Patrol performed best across the three reported comparison metrics.

Utility-Based Patrol demonstrates adaptive decision-making capabilities, particularly through its consideration of risk, alerts, coverage, and resource constraints. However, these results do not establish it as the overall best-performing strategy.

11.4 Multi-Agent Evaluation

The two-agent patrol system was evaluated over 10 simulation trials.

Metric

Average Result

Total Campus Coverage

44.44%

Agent 1 Territory Coverage

50.00%

Agent 2 Territory Coverage

40.00%

Average Total Distance

60.00

Average Battery Remaining

70.00

Average Overlap Count

0.00

The results demonstrate territory-based patrol coordination with zero average overlapping locations in the evaluated trials.

The total campus coverage of 44.44% also indicates that further improvements are needed to increase overall campus coverage.

11.5 Result Files

Experimental data and summary files are available in the results/ directory.

File

Description

patrol_results.csv

Individual patrol evaluation results

multi_agent_results.csv

Individual multi-agent evaluation results

patrol_summary.csv

Aggregated patrol strategy comparison

multi_agent_summary.csv

Aggregated multi-agent evaluation

12. Interactive Dashboard

The project includes an interactive dashboard developed using Streamlit.

Live Dashboard:
https://autonomous-campus-security.onrender.com/

The dashboard provides:

System Monitoring

Current agent location

Battery level

Patrol distance

Patrol steps

Active security alerts

Campus Visualization

Campus locations

Campus paths

Current agent position

Patrol history

Incident Monitoring

Active incidents

Incident priorities

Incident response status

Incident response time

AI Decision Analysis

Utility scores

Selected destination

Decision factors

Explainability information

Strategy Comparison

Random Patrol

Fixed Route Patrol

Utility-Based Patrol

Average distance

Average unique areas covered

Average final battery

Multi-Agent Analysis

Total campus coverage

Agent-specific territory coverage

Average patrol distance

Average battery remaining

Average overlap

13. Dashboard Screenshots

The following screenshots demonstrate the implemented dashboard and its main features.

Dashboard Overview



Campus Map



Command Center



Incident Monitoring



Multi-Agent Command Center



Additional Command Center Views





14. Technologies Used

Technology

Purpose

Python

Core application development

NetworkX

Campus graph and shortest-path calculations

Streamlit

Interactive dashboard

Plotly

Interactive data visualization

Pandas

Experimental data processing

Pytest

Automated testing

Git

Version control

GitHub

Source-code hosting

Render

Dashboard deployment

15. Project Structure

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
│   ├── evaluate_multi_agent.py
│   ├── analyze_results.py
│   └── plot_results.py
│
├── results/
│   ├── patrol_results.csv
│   ├── multi_agent_results.csv
│   ├── patrol_summary.csv
│   └── multi_agent_summary.csv
│
├── tests/
│   └── test_project.py
│
├── screenshots/
│   ├── dashboard.png
│   ├── map.png
│   ├── commandcenter2.png
│   ├── incidentcenter.png
│   └── multiagent command centre.png
│
├── docs/
│   └── images/
│       ├── patrol_distance.png
│       ├── unique_areas.png
│       └── final_battery.png
│
├── requirements.txt
├── README.md
└── .gitignore

16. Installation and Setup

Prerequisites

Python 3.10 or later recommended

Git

Internet connection for installing dependencies

Step 1: Clone the repository

git clone https://github.com/kodumurinagasaivignesh/Autonomous_Campus_Security.git

Step 2: Navigate to the project directory

cd Autonomous_Campus_Security

Step 3: Create a virtual environment

python -m venv venv

Step 4: Activate the virtual environment

Windows PowerShell:

venv\Scripts\Activate.ps1

Step 5: Install dependencies

pip install -r requirements.txt

17. Running the Project

Launch the dashboard

streamlit run dashboard/app.py

Open the local dashboard in your browser:

http://localhost:8501

Run the utility-based patrol agent

python src/utility_agent.py

Run the multi-agent patrol system

python src/multi_agent.py

Run patrol strategy evaluation

python experiments/evaluate_patrol.py

Run multi-agent evaluation

python experiments/evaluate_multi_agent.py

Analyze experimental results

python experiments/analyze_results.py

Generate comparison charts

python experiments/plot_results.py

18. Automated Testing

The project uses Pytest for automated testing.

The test suite covers major system components, including:

Campus environment

Battery management

Security agent

Incident management

Utility-based agent

Multi-agent coordination

Incident response metrics

Complete patrol functionality

Run the test suite:

pytest -q

Verified test result:

21 passed

All 21 tests passed in the completed project test run.

19. Responsible AI Considerations

The project considers important responsible AI principles.

Explainability

The system provides human-readable explanations for utility-based destination selection.

Transparency

Utility factors and their weights are documented and visible.

Human Oversight

The project is designed as an academic decision-support prototype, not a replacement for human security personnel.

Privacy

The current simulation does not process real CCTV footage, biometric information, or personal data.

Safety

The prototype operates in a simulated campus environment and does not directly control physical security infrastructure.

20. Limitations

The current implementation has the following limitations:

The campus environment is simulated.

Security risk values are predefined.

Security incidents are simulated.

Battery consumption is simplified.

Patrol movement occurs in discrete simulation steps.

Real camera and sensor feeds are not connected.

Multi-agent communication is simulated.

The system has not been deployed on a physical robot.

Experimental results depend on the configured campus environment and simulation settings.

The current evaluation does not establish performance under all possible real-world security conditions.

Therefore, this project should be considered an academic and research prototype rather than a production-ready campus security system.

21. Future Improvements

Potential future improvements include:

Real campus map integration

GPS and indoor localization

Computer vision-based incident detection

CCTV integration with appropriate privacy safeguards

Real-time sensor streams

Dynamic security risk prediction

Reinforcement learning for patrol optimization

Advanced multi-agent coordination

Physical autonomous robot integration

Real-time security notifications

Edge AI deployment

Privacy-preserving surveillance

Human-in-the-loop decision-making

Fail-safe mechanisms

22. Project Outcomes

The completed project demonstrates an end-to-end simulated autonomous campus security patrol system capable of:

Modeling a campus using a weighted graph.

Implementing multiple autonomous patrol strategies.

Selecting destinations using utility-based decision-making.

Simulating and responding to security incidents.

Managing battery constraints and charging.

Explaining autonomous agent decisions.

Coordinating two patrol agents using territory-based patrol.

Comparing performance through repeated experiments.

Visualizing patrol operations through an interactive dashboard.

Validating core functionality through automated tests.

23. Team Information

Group 13

Team Member

Kodumuri Naga Sai Vignesh

Dhruv Choudhary

Nandavarapu Mohan Venkat Maniram

Academic Information

Detail

Information

Institution

Lovely Professional University

Course

CSE276 – Artificial Intelligence Foundations

Project Title

Autonomous Patrol & Surveillance Agent for Campus Security

Group

13

Academic Session

2026–27

24. Repository and Deployment

GitHub Repository:
https://github.com/kodumurinagasaivignesh/Autonomous_Campus_Security

Live Dashboard:
https://autonomous-campus-security.onrender.com/

25. License

This project is developed for academic and educational purposes.

<p align="center">
  <strong>Autonomous Patrol & Surveillance Agent for Campus Security</strong><br>
  Group 13 | CSE276 – Artificial Intelligence Foundations<br>
  Lovely Professional University | 2026–27
</p>