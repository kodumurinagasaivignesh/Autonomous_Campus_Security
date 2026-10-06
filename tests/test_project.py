import os
import sys

# Add src folder to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


from environment import CampusEnvironment
from battery import BatteryManager
from agent import SecurityAgent
from incidents import IncidentManager
from utility_agent import UtilityBasedPatrolAgent
from multi_agent import MultiAgentPatrolSystem


# ============================================================
# ENVIRONMENT TESTS
# ============================================================

def test_campus_has_locations():
    campus = CampusEnvironment()

    locations = campus.get_locations()

    assert len(locations) == 9
    assert "Main Gate" in locations
    assert "Security Office" in locations


def test_campus_distance():
    campus = CampusEnvironment()

    distance = campus.get_distance(
        "Main Gate",
        "Parking",
    )

    assert distance == 3


def test_shortest_path():
    campus = CampusEnvironment()

    path = campus.get_shortest_path(
        "Main Gate",
        "Parking",
    )

    assert path[0] == "Main Gate"
    assert path[-1] == "Parking"


# ============================================================
# BATTERY TESTS
# ============================================================

def test_battery_consumption():
    battery = BatteryManager(
        capacity=100,
        initial_charge=100,
    )

    result = battery.consume(20)

    assert result is True
    assert battery.charge == 80


def test_battery_recharge():
    battery = BatteryManager(
        capacity=100,
        initial_charge=30,
    )

    battery.recharge()

    assert battery.charge == 100


def test_low_battery_detection():
    battery = BatteryManager(
        capacity=100,
        initial_charge=15,
        low_battery_threshold=20,
    )

    assert battery.is_low() is True


# ============================================================
# SECURITY AGENT TESTS
# ============================================================

def test_agent_movement():
    campus = CampusEnvironment()

    agent = SecurityAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    result = agent.move_to("Parking")

    assert result is True
    assert agent.current_location == "Parking"
    assert agent.battery == 97


def test_agent_records_patrol_history():
    campus = CampusEnvironment()

    agent = SecurityAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    agent.move_to("Parking")

    assert "Parking" in agent.patrol_history


# ============================================================
# INCIDENT TESTS
# ============================================================

def test_incident_creation():
    campus = CampusEnvironment()

    manager = IncidentManager(campus)

    incident = manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Possible fire detected.",
    )

    assert incident.location == "Canteen"
    assert incident.priority == 10
    assert incident.active is True


def test_highest_priority_incident():
    campus = CampusEnvironment()

    manager = IncidentManager(campus)

    manager.create_incident(
        "Unauthorized Entry",
        "Main Gate",
        "Unauthorized person detected.",
    )

    fire = manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Possible fire detected.",
    )

    highest = manager.get_highest_priority_incident()

    assert highest == fire
    assert highest.priority == 10


def test_incident_resolution():
    campus = CampusEnvironment()

    manager = IncidentManager(campus)

    incident = manager.create_incident(
        "Emergency",
        "Hostel",
        "Emergency reported.",
    )

    manager.resolve_incident(incident)

    assert incident.active is False
    assert len(manager.get_active_incidents()) == 0


# ============================================================
# UTILITY AGENT TESTS
# ============================================================

def test_utility_agent_initialization():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    assert agent.current_location == "Main Gate"
    assert agent.battery == 100
    assert agent.patrol_step == 0


def test_utility_agent_calculates_utility():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    utility = agent.calculate_utility("Parking")

    assert isinstance(utility, (int, float))


def test_utility_agent_selects_destination():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    destination, scores = agent.choose_best_destination()

    assert destination is not None
    assert destination != "Main Gate"
    assert len(scores) > 0


def test_utility_agent_responds_to_alert():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    agent.incident_manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Fire detected.",
    )

    agent.update_alerts_from_incidents()

    assert agent.live_alerts["Canteen"] == 10


# ============================================================
# MULTI-AGENT TESTS
# ============================================================

def test_multi_agent_initialization():
    campus = CampusEnvironment()

    system = MultiAgentPatrolSystem(campus)

    assert system.agent_1 is not None
    assert system.agent_2 is not None

    assert (
        system.agent_1.current_location
        == "Main Gate"
    )

    assert (
        system.agent_2.current_location
        == "Security Office"
    )


def test_multi_agent_zone_assignment():
    campus = CampusEnvironment()

    system = MultiAgentPatrolSystem(campus)

    system.assign_zone(
        "Agent 1",
        "Library",
    )

    assert (
        "Library"
        in system.assigned_zones["Agent 1"]
    )


# ============================================================
# FULL PATROL TEST
# ============================================================

def test_utility_patrol_step():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    initial_location = agent.current_location

    result = agent.patrol_once()

    assert result is True

    assert agent.current_location != initial_location

    assert agent.patrol_step == 1

# ============================================================
# INCIDENT RESPONSE TEST
# ============================================================

def test_utility_agent_prioritizes_high_priority_alert():
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    agent.incident_manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Fire detected near the canteen.",
    )

    destination, scores = (
        agent.choose_best_destination()
    )

    assert destination == "Canteen"
    assert scores["Canteen"] == max(
        scores.values()
    )
    