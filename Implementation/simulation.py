import matplotlib.pyplot as plt
from city_model import CityGraph
from intelligence_engine import RoutingEngine, RiskAnalyzer, PriorityManager
from gui import CityVisualizer

# Singleton instances for the simulation environment
city = CityGraph(size=10)
RiskAnalyzer.update_risk(city) # Perform initial stochastic risk assessment
router = RoutingEngine(city)
priority_queue = PriorityManager()
visualizer = None

def handle_emergency_event(x, y):
    """ Processes an emergency incident and performs priority multi-criteria analysis. """
    node_data = city.get_node_data((x, y))
    priority_queue.add_emergency((x, y), node_data.risk_index, node_data.population_density)
    print(f"[EVENT] Emergency incident logged at ({x}, {y}). Awaiting AI Dispatch.")

def handle_dispatch_decision():
    """ 
    Executes the Decision-Making loop: Prioritization -> Allocation -> Routing.
    """
    # 1. Optimal Event Selection
    target = priority_queue.get_next_emergency()
    
    if target == None:
        print("[IDLE] No pending critical incidents. Monitoring city state.")
        visualizer.draw_city(title="STATUS: CITY MONITORING")
        return
        
    # 2. Greedy Resource Allocation
    depot = router.find_nearest_depot(target)
    if depot == None:
        print("[ERROR] Resource allocation failed: No available depots found.")
        return
        
    # 3. Heuristic Informed Search (A*)
    path = router.find_fastest_path(depot, target)
    if path == None:
        print(f"[FAILURE] Path traversal impossible to {target} due to topological disconnection.")
        visualizer.draw_city(title=f"ALERT: DISCONNECTED ZONE {target}")
    else:
        print(f"[SUCCESS] AI Dispatch optimized from {depot} to {target}")
        print(f"[ANALYSIS] Traversal Path: {path}")
        # Real-time visual feedback of the intelligent response
        visualizer.draw_city(ambulance_path=path, title=f"AI RESPONSE IN PROGRESS: {target}")

def main():
    global visualizer
    print("--- CITYMIND: HYBRID INTELLIGENT COMMAND CENTER ---")
    print("OPERATIONAL GUIDELINES:")
    print("1. INTERACT with the geospatial lattice (Click Nodes) to trigger incidents.")
    print("2. EXECUTE AI DISPATCH (Button) to trigger heuristic decision logic.")
    print("3. MONITOR console for architectural reasoning and log data.")
    
    # Initialize Visualizer with functional callback mapping
    visualizer = CityVisualizer(city, handle_dispatch_decision, handle_emergency_event)
    
    # Render initial city state
    visualizer.draw_city(title="CITYMIND: GEOSPATIAL INITIALIZATION COMPLETE")
    
    # Execute primary GUI event loop
    visualizer.run()

if __name__ == "__main__":
    main()
