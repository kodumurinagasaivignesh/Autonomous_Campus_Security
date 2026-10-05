class BatteryManager:
    """Manages battery consumption and charging for a security agent."""

    def __init__(self, capacity=100, initial_charge=100, low_battery_threshold=20):
        if capacity <= 0:
            raise ValueError("Battery capacity must be greater than 0.")

        if not 0 <= initial_charge <= capacity:
            raise ValueError("Initial charge must be between 0 and capacity.")

        if not 0 <= low_battery_threshold <= capacity:
            raise ValueError("Low battery threshold is invalid.")

        self.capacity = capacity
        self.charge = initial_charge
        self.low_battery_threshold = low_battery_threshold

    def consume(self, amount):
        """Consume battery energy."""

        if amount < 0:
            raise ValueError("Battery consumption cannot be negative.")

        if amount > self.charge:
            self.charge = 0
            return False

        self.charge -= amount
        return True

    def recharge(self):
        """Fully recharge the battery."""

        self.charge = self.capacity

    def is_low(self):
        """Check whether the battery is below the low-battery threshold."""

        return self.charge <= self.low_battery_threshold

    def get_percentage(self):
        """Return the current battery percentage."""

        return (self.charge / self.capacity) * 100

    def status(self):
        """Display the current battery status."""

        print("\n--- Battery Status ---")
        print(f"Charge: {self.charge}/{self.capacity}")
        print(f"Percentage: {self.get_percentage():.1f}%")
        print(f"Low battery: {'YES' if self.is_low() else 'NO'}")


if __name__ == "__main__":
    battery = BatteryManager(
        capacity=100,
        initial_charge=100,
        low_battery_threshold=20,
    )

    print("=== BATTERY SYSTEM TEST ===")

    battery.status()

    print("\nConsuming 30 units...")
    battery.consume(30)
    battery.status()

    print("\nConsuming 55 units...")
    battery.consume(55)
    battery.status()

    print("\nRecharging...")
    battery.recharge()
    battery.status()