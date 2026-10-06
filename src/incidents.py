class Incident:
    """Represents a security incident detected on campus."""

    def __init__(
        self,
        incident_type,
        location,
        priority,
        description,
        detected_at_step=0,
    ):
        self.incident_type = incident_type
        self.location = location
        self.priority = priority
        self.description = description

        # Patrol step at which the incident was detected.
        self.detected_at_step = detected_at_step

        # Patrol step at which the incident was resolved.
        self.resolved_at_step = None

        self.active = True

    def resolve(self, current_step=None):
        """Resolve the incident and record response time."""

        self.active = False
        self.resolved_at_step = current_step

    def get_response_time(self):
        """Return patrol steps taken to resolve the incident."""

        if self.resolved_at_step is None:
            return None

        return (
            self.resolved_at_step
            - self.detected_at_step
        )

    def __str__(self):
        status = (
            "ACTIVE"
            if self.active
            else "RESOLVED"
        )

        response_time = self.get_response_time()

        response_text = ""

        if response_time is not None:
            response_text = (
                f" | Response Time: "
                f"{response_time} steps"
            )

        return (
            f"[{status}] "
            f"{self.incident_type} | "
            f"Location: {self.location} | "
            f"Priority: {self.priority} | "
            f"{self.description}"
            f"{response_text}"
        )


class IncidentManager:
    """Manages security incidents on campus."""

    INCIDENT_PRIORITIES = {
        "Unauthorized Entry": 7,
        "Suspicious Activity": 5,
        "Fire Alert": 10,
        "Emergency": 10,
    }

    def __init__(self, campus):
        self.campus = campus
        self.active_incidents = []

    def create_incident(
        self,
        incident_type,
        location,
        description,
        detected_at_step=0,
    ):
        """Create a new campus security incident."""

        if location not in self.campus.graph:
            raise ValueError(
                f"Unknown campus location: {location}"
            )

        if incident_type not in self.INCIDENT_PRIORITIES:
            raise ValueError(
                f"Unknown incident type: {incident_type}"
            )

        priority = self.INCIDENT_PRIORITIES[
            incident_type
        ]

        incident = Incident(
            incident_type=incident_type,
            location=location,
            priority=priority,
            description=description,
            detected_at_step=detected_at_step,
        )

        self.active_incidents.append(incident)

        print("\n🚨 NEW SECURITY INCIDENT")
        print(incident)

        return incident

    def get_active_incidents(self):
        """Return all active incidents."""

        return [
            incident
            for incident in self.active_incidents
            if incident.active
        ]

    def get_highest_priority_incident(self):
        """Return the highest-priority active incident."""

        active_incidents = (
            self.get_active_incidents()
        )

        if not active_incidents:
            return None

        return max(
            active_incidents,
            key=lambda incident: incident.priority,
        )

    def resolve_incident(
        self,
        incident,
        current_step=None,
    ):
        """Resolve an incident."""

        incident.resolve(
            current_step=current_step
        )

        print("\n✅ INCIDENT RESOLVED")
        print(incident)

    def display_active_incidents(self):
        """Display currently active incidents."""

        active_incidents = (
            self.get_active_incidents()
        )

        print("\n=== ACTIVE INCIDENTS ===")

        if not active_incidents:
            print("No active incidents.")
            return

        for incident in active_incidents:
            print(incident)
            