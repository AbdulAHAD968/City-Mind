import networkx as nx
import random

class CityNode:
    """ 
    Represents a discrete geospatial unit within the urban graph model.
    Stores multi-dimensional state data: Type, Density, Risk, and Accessibility.
    """
    def __init__(self, node_id, position, location_type):
        self.id = node_id
        self.pos = position
        self.location_type = location_type
        
        # Stochastic initialization of population density
        self.population_density = random.randint(10, 100)
        self.risk_index = 0.0
        self.accessible = True

class CityGraph:
    """ 
    Implements a discrete graph-based city model G = (V, E).
    Enables dynamic environment simulation and topological analysis.
    """
    def __init__(self, size=10):
        self.size = size
        self.graph = nx.Graph() # Mathematical graph structure
        self.nodes = {}         # Node state mapping
        
        self.initialize_topology()

    def initialize_topology(self):
        """ 
        Constructs the urban grid topology and assigns stochastic location types.
        """
        building_types = ["Residential", "Hospital", "School", "Industrial", "Power Plant", "Ambulance Depot"]
        
        # 1. Discrete Vertex Generation
        for x in range(self.size):
            for y in range(self.size):
                node_id = (x, y)
                my_type = random.choice(building_types)
                
                new_node = CityNode(node_id, (x, y), my_type)
                self.nodes[node_id] = new_node
                self.graph.add_node(node_id)

        # 2. Edge Connectivity (Lattice Topology)
        for x in range(self.size):
            for y in range(self.size):
                current = (x, y)
                
                # Horizontal adjacency
                if x + 1 < self.size:
                    neighbor = (x + 1, y)
                    self.add_edge_with_cost(current, neighbor)
                
                # Vertical adjacency
                if y + 1 < self.size:
                    neighbor = (x, y + 1)
                    self.add_edge_with_cost(current, neighbor)

    def add_edge_with_cost(self, node_a, node_b):
        """ 
        Assigns traversal costs (edge weights) based on urban zoning heuristics.
        """
        cost = 1.0
        type_a = self.nodes[node_a].location_type
        type_b = self.nodes[node_b].location_type
        
        # Heuristic cost reduction for Residential zones
        if type_a == "Residential" or type_b == "Residential":
            cost = 0.8
        
        self.graph.add_edge(node_a, node_b, weight=cost, blocked=False)

    def dynamic_reweighting(self, node_a, node_b):
        """ 
        Implements Dynamic Graph Reweighting.
        Assigns an effectively infinite traversal cost to simulate road failure 
        (e.g., flooding, structural damage).
        """
        if self.graph.has_edge(node_a, node_b):
            self.graph[node_a][node_b]['blocked'] = True
            # Infinite cost effectively removes the edge from optimal path search
            self.graph[node_a][node_b]['weight'] = float('inf')

    def get_node_data(self, node_id):
        """ Retrieves state data for a specific vertex. """
        return self.nodes.get(node_id)
