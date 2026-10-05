class Incident:
    """Represents a security incident detected on campus."""

    def __init__(self, incident_type, location, priority, description):
        self.incident_type = incident_type
        self.location = location
        self.priority = priority
        self.description = description
        self.active = True

    def resolve(self):
        """Mark the incident as resolved."""
        self.active = False

    def __str__(self):
        status = "ACTIVE" if self.active else "RESOLVED"

        return (
            f"[{status}] {self.incident_type} | "
            f"Location: {self.location} | "
            f"Priority: {self.priority} | "
            f"{self.description}"
        )


class IncidentManager:
    """Creates and manages campus security incidents."""

    INCIDENT_PRIORITIES = {
        "Unauthorized Entry": 7,
        "Suspicious Activity": 5,
        "Fire Alert": 10,
        "Emergency": 10,
    }

    def __init__(self, campus):
        self.campus = campus
        self.active_incidents = []

    def create_incident(self, incident_type, location, description):
        """Create a new campus security incident."""

        if location not in self.campus.graph:
            raise ValueError(f"Unknown campus location: {location}")

        if incident_type not in self.INCIDENT_PRIORITIES:
            raise ValueError(f"Unknown incident type: {incident_type}")

        priority = self.INCIDENT_PRIORITIES[incident_type]

        incident = Incident(
            incident_type=incident_type,
            location=location,
            priority=priority,
            description=description,
        )

        self.active_incidents.append(incident)

        print("\n🚨 NEW SECURITY INCIDENT")
        print(incident)

        return incident

    def get_active_incidents(self):
        """Return all unresolved incidents."""

        return [
            incident
            for incident in self.active_incidents
            if incident.active
        ]

    def get_highest_priority_incident(self):
        """Return the highest-priority active incident."""

        active_incidents = self.get_active_incidents()

        if not active_incidents:
            return None

        return max(
            active_incidents,
            key=lambda incident: incident.priority,
        )

    def resolve_incident(self, incident):
        """Resolve a specific incident."""

        incident.resolve()

        print("\n✅ INCIDENT RESOLVED")
        print(incident)

    def display_active_incidents(self):
        """Display all currently active incidents."""

        active_incidents = self.get_active_incidents()

        print("\n=== ACTIVE INCIDENTS ===")

        if not active_incidents:
            print("No active incidents.")
            return

        for incident in active_incidents:
            print(incident)


if __name__ == "__main__":
    from environment import CampusEnvironment

    campus = CampusEnvironment()
    manager = IncidentManager(campus)

    manager.create_incident(
        "Unauthorized Entry",
        "Main Gate",
        "Unauthorized person detected near the main entrance.",
    )

    manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Possible fire detected in the canteen area.",
    )

    manager.display_active_incidents()

    highest_priority = manager.get_highest_priority_incident()

    if highest_priority:
        print("\n🔥 Highest priority incident:")
        print(highest_priority)

        manager.resolve_incident(highest_priority)

    manager.display_active_incidents()