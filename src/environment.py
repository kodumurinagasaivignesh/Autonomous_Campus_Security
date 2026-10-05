import networkx as nx


class CampusEnvironment:
    """Represents the virtual campus as a weighted graph."""

    def __init__(self):
        self.graph = nx.Graph()
        self._create_campus()

    def _create_campus(self):
        # Campus locations
        locations = [
            "Main Gate",
            "Academic Block",
            "Library",
            "Hostel",
            "Canteen",
            "Parking",
            "Sports Ground",
            "Administration",
            "Security Office",
        ]

        # Add locations as graph nodes
        self.graph.add_nodes_from(locations)

        # Add paths between locations.
        # The weight represents approximate travel distance.
        paths = [
            ("Main Gate", "Academic Block", 4),
            ("Main Gate", "Parking", 3),
            ("Academic Block", "Library", 2),
            ("Academic Block", "Administration", 3),
            ("Library", "Canteen", 2),
            ("Library", "Hostel", 5),
            ("Canteen", "Hostel", 3),
            ("Canteen", "Sports Ground", 4),
            ("Parking", "Sports Ground", 5),
            ("Administration", "Security Office", 2),
            ("Security Office", "Hostel", 4),
            ("Sports Ground", "Hostel", 3),
        ]

        self.graph.add_weighted_edges_from(paths)

    def get_locations(self):
        """Return all campus locations."""
        return list(self.graph.nodes)

    def get_neighbors(self, location):
        """Return locations directly connected to a given location."""
        if location not in self.graph:
            raise ValueError(f"Unknown campus location: {location}")

        return list(self.graph.neighbors(location))

    def get_distance(self, start, destination):
        """Return the shortest travel distance between two locations."""
        if start not in self.graph:
            raise ValueError(f"Unknown campus location: {start}")

        if destination not in self.graph:
            raise ValueError(f"Unknown campus location: {destination}")

        return nx.shortest_path_length(
            self.graph,
            start,
            destination,
            weight="weight",
        )

    def get_shortest_path(self, start, destination):
        """Return the shortest path between two campus locations."""
        if start not in self.graph:
            raise ValueError(f"Unknown campus location: {start}")

        if destination not in self.graph:
            raise ValueError(f"Unknown campus location: {destination}")

        return nx.shortest_path(
            self.graph,
            start,
            destination,
            weight="weight",
        )


if __name__ == "__main__":
    campus = CampusEnvironment()

    print("Campus locations:")
    for location in campus.get_locations():
        print("-", location)

    print("\nNeighbors of Academic Block:")
    print(campus.get_neighbors("Academic Block"))

    print("\nShortest path from Main Gate to Hostel:")
    print(campus.get_shortest_path("Main Gate", "Hostel"))

    print("\nDistance from Main Gate to Hostel:")
    print(campus.get_distance("Main Gate", "Hostel"))