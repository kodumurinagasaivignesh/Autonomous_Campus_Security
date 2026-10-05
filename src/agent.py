from environment import CampusEnvironment
from battery import BatteryManager


class SecurityAgent:
    """Basic autonomous security patrol agent with battery management."""

    def __init__(
        self,
        campus,
        start_location="Main Gate",
        battery=100,
        charging_station="Security Office",
    ):
        self.campus = campus
        self.current_location = start_location

        # Battery management
        self.battery_manager = BatteryManager(
            capacity=battery,
            initial_charge=battery,
            low_battery_threshold=20,
        )

        # Keep battery as a simple number for compatibility
        # with the utility-based patrol code.
        self.battery = battery

        self.charging_station = charging_station

        self.patrol_history = [start_location]
        self.total_distance = 0

    def sync_battery(self):
        """Synchronize the agent battery value with BatteryManager."""
        self.battery = self.battery_manager.charge

    def move_to(self, destination):
        """Move the agent to a connected destination."""

        if destination not in self.campus.graph:
            raise ValueError(
                f"Unknown destination: {destination}"
            )

        if destination == self.current_location:
            print("Agent is already at this location.")
            return True

        distance = self.campus.get_distance(
            self.current_location,
            destination,
        )

        if distance > self.battery:
            print(
                f"Not enough battery to reach {destination}. "
                f"Required: {distance}, Available: {self.battery}"
            )
            return False

        path = self.campus.get_shortest_path(
            self.current_location,
            destination,
        )

        # Consume battery
        self.battery_manager.consume(distance)
        self.sync_battery()

        self.current_location = destination
        self.total_distance += distance
        self.patrol_history.append(destination)

        print(f"Agent moved: {' -> '.join(path)}")
        print(f"Current location: {self.current_location}")
        print(f"Battery remaining: {self.battery}")
        print(f"Total distance: {self.total_distance}")

        if self.battery_manager.is_low():
            print("⚠️ WARNING: Battery is low.")

        return True

    def go_to_charging_station(self):
        """Move to the charging station and recharge."""

        if self.current_location == self.charging_station:
            print("\n🔋 Agent is already at the charging station.")
            self.battery_manager.recharge()
            self.sync_battery()
            print(f"Battery recharged to {self.battery}.")
            return True

        print("\n🔋 LOW BATTERY — Going to charging station...")
        print(f"Charging station: {self.charging_station}")

        success = self.move_to(self.charging_station)

        if not success:
            print("❌ Agent cannot reach the charging station.")
            return False

        self.battery_manager.recharge()
        self.sync_battery()

        print("✅ Battery fully recharged.")
        print(f"Battery: {self.battery}")

        return True

    def check_battery(self):
        """Check whether the agent needs charging."""

        self.sync_battery()

        if self.battery_manager.is_low():
            print("\n⚠️ Battery level is low.")
            return False

        return True

    def status(self):
        """Display the current agent status."""

        print("\n--- Security Agent Status ---")
        print(f"Location: {self.current_location}")
        print(f"Battery: {self.battery}/{self.battery_manager.capacity}")
        print(f"Charging station: {self.charging_station}")
        print(f"Total distance: {self.total_distance}")
        print(f"Patrol history: {self.patrol_history}")

        self.battery_manager.status()


if __name__ == "__main__":
    campus = CampusEnvironment()

    agent = SecurityAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
        charging_station="Security Office",
    )

    print("=== SECURITY AGENT WITH BATTERY MANAGEMENT ===")

    agent.status()

    print("\nMoving to Library...")
    agent.move_to("Library")

    print("\nMoving to Hostel...")
    agent.move_to("Hostel")

    agent.status()

    if not agent.check_battery():
        agent.go_to_charging_station()

    print("\n=== FINAL AGENT STATUS ===")
    agent.status()