import heapq
import networkx as nx

class RoutingEngine:
    """ 
    Implements Informed Search strategies for optimal navigation in a dynamic 
    environment. Primary algorithm: A* with Admissible Heuristics.
    """
    def __init__(self, city_graph):
        self.city_graph = city_graph

    def get_manhattan_distance(self, node_a, node_b):
        """ 
        The Admissible Heuristic h(n) for grid-based navigation. 
        Calculates the L1 norm (Manhattan Distance) between two nodes.
        """
        x1, y1 = node_a
        x2, y2 = node_b
        return abs(x1 - x2) + abs(y1 - y2)

    def find_fastest_path(self, start_node, end_node):
        """ 
        Computes the optimal path using A* Search: f(n) = g(n) + h(n).
        Justification: Guarantees optimality while minimizing node expansion 
        compared to uninformed strategies like Dijkstra.
        """
        try:
            path = nx.astar_path(
                self.city_graph.graph, 
                start_node, 
                end_node, 
                heuristic=self.get_manhattan_distance, 
                weight='weight'
            )
            return path
        except nx.NetworkXNoPath:
            # Handles environmental uncertainty when target is unreachable
            return None

    def find_nearest_depot(self, emergency_location):
        """ 
        Implements Greedy Nearest-Neighbor Allocation.
        Minimizes response latency by selecting the closest available resource node.
        """
        closest_depot = None
        min_distance = float('inf')

        for node_id, node_data in self.city_graph.nodes.items():
            if node_data.location_type == "Ambulance Depot" and node_data.accessible:
                dist = self.get_manhattan_distance(node_id, emergency_location)
                if dist < min_distance:
                    min_distance = dist
                    closest_depot = node_id
        
        return closest_depot

class RiskAnalyzer:
    """ 
    Implements a Weighted Heuristic Risk Model to simulate real-time 
    environmental awareness and hazard prediction.
    """
    @staticmethod
    def update_risk(city_graph):
        # Weight parameters for the risk formula
        W_BASE = 0.5
        W_DENSITY = 0.3
        
        for node_id, node in city_graph.nodes.items():
            # Base risk assignment based on Location Type
            score = 0.1 
            if node.location_type == "Industrial":
                score = 0.4
            elif node.location_type == "Power Plant":
                score = 0.6
            
            # Incorporating Population Density into the Weighted Heuristic
            density_factor = node.population_density / 100.0
            node.risk_index = (score * W_BASE) + (density_factor * W_DENSITY)

class PriorityManager:
    """ 
    Implements a Multi-Criteria Decision Prioritization engine using a 
    Max-Heap data structure for efficient O(log n) scheduling.
    """
    def __init__(self):
        self.emergencies = []

    def add_emergency(self, location, risk_level, density):
        """ 
        Calculates Priority using a weighted linear combination:
        Priority = (alpha * Risk) + (beta * Density).
        Ensures high-impact incidents are addressed optimally.
        """
        ALPHA = 0.7
        BETA = 0.3
        
        # Negative value for Max-Heap simulation using heapq (min-heap)
        priority_score = -(risk_level * ALPHA + (density / 100.0) * BETA)
        heapq.heappush(self.emergencies, (priority_score, location))

    def get_next_emergency(self):
        """ Retrieves the most critical emergency incident from the prioritized queue. """
        if len(self.emergencies) > 0:
            score, location = heapq.heappop(self.emergencies)
            return location
        return None
