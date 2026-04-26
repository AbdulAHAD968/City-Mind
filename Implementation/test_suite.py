import unittest
from city_model import CityGraph
from intelligence_engine import RoutingEngine, RiskAnalyzer, PriorityManager

class TestCityMindArchitecture(unittest.TestCase):
    """ 
    Unit Testing Suite to validate the architectural integrity and 
    algorithmic correctness of the CityMind hybrid system.
    """
    def setUp(self):
        
        self.city = CityGraph(size=5)
        self.router = RoutingEngine(self.city)
        self.priority_manager = PriorityManager()

    def test_topological_integrity(self):
        """ Validates vertex count and edge connectivity of the geospatial model. """
        self.assertEqual(len(self.city.nodes), 25)
        self.assertEqual(self.city.graph.number_of_edges(), 40)

    def test_heuristic_search_optimality(self):
        """ Verifies that A* Search (Informed Search) identifies valid paths. """
        path = self.router.find_fastest_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))

    def test_dynamic_graph_reweighting(self):
        """ Verifies the implementation of real-time edge weight failure simulation. """
        start = (0, 0)
        neighbor = (1, 0)
        self.city.dynamic_reweighting(start, neighbor)
        
        self.assertEqual(self.city.graph[start][neighbor]['weight'], float('inf'))

    def test_decision_prioritization(self):
        """ Validates the Multi-Criteria Decision logic for emergency ranking. """
        
        self.priority_manager.add_emergency((1, 1), 0.2, 10) 
        
        self.priority_manager.add_emergency((2, 2), 0.9, 90) 
        
        highest_priority_incident = self.priority_manager.get_next_emergency()
        self.assertEqual(highest_priority_incident, (2, 2))

    def test_weighted_risk_model(self):
        """ Validates that the RiskAnalyzer correctly propagates heuristic risk scores. """
        RiskAnalyzer.update_risk(self.city)
        for node in self.city.nodes.values():
            
            self.assertGreaterEqual(node.risk_index, 0.0)
            self.assertLessEqual(node.risk_index, 1.0)

if __name__ == "__main__":
    unittest.main()
