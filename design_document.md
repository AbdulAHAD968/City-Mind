# Design Document: CityMind – Hybrid Urban Intelligence System

**Course:** Semester Project - ARTIFICIAL INTELLIGENCE  
**System Name:** CityMind  
**Architecture:** Hybrid Intelligent Decision-Making System

---

## 1. Project Overview
CityMind is a hybrid AI system designed to simulate intelligent urban management. The system integrates heuristic search, multi-criteria decision prioritization, and dynamic graph adaptation to handle real-world urban uncertainty, including infrastructure failure and emergency logistics.

---

## 2. System Architecture: A Hybrid Approach
The system is architected as a modular intelligent agent that combines multiple AI techniques to handle complex decision-making:

1.  **City Graph Module (`city_model.py`)**: A discrete geospatial representation using a grid-based graph.
2.  **Navigation Module (`intelligence_engine.py`)**: Uses **Heuristic Search (A*)** for optimal pathfinding.
3.  **Risk Prediction Module**: A **Weighted Heuristic Model** for environmental awareness.
4.  **Decision Module**: A **Max-Heap Priority Queue** for multi-objective optimization.

---

## 3. Algorithmic Implementation & Justification

### 3.1 Navigation Module: A* Search
**Algorithm:** $f(n) = g(n) + h(n)$  
**Heuristic:** Manhattan Distance ($h(n) = |x_1 - x_2| + |y_1 - y_2|$)

*   **Justification:** A* was selected because it guarantees optimal paths while significantly reducing the search space using an admissible heuristic. In a grid-based environment, Manhattan distance provides an efficient and computationally inexpensive estimate, making A* suitable for real-time emergency routing.
*   **Critical Comparison:** While Dijkstra’s algorithm guarantees optimal paths, it was not selected as the primary method due to its uninformed nature, which leads to unnecessary node exploration. A* improves upon this by incorporating domain-specific heuristics.

### 3.2 Risk Prediction Module: Weighted Heuristic Model
**Formula:** $Risk = w_1 \cdot \text{Population} + w_2 \cdot \text{LocationType}$

*   **Justification:** A weighted scoring model was used to approximate risk in the absence of labeled training data. This approach enables dynamic updates and interpretability, allowing the system to handle environmental uncertainty effectively.

### 3.3 Decision Module: Max-Heap Priority Queue
**Formula:** $Priority = \alpha \cdot \text{Risk} + \beta \cdot \text{Density} - \gamma \cdot \text{Distance}$

*   **Justification:** A max-heap structure ensures logarithmic-time prioritization ($\mathcal{O}(\log n)$) while enabling multi-factor decision-making. This balances urgency (risk), impact (population), and efficiency (distance), achieving a form of multi-objective optimization.

### 3.4 Adaptation Module: Dynamic Graph Reweighting
*   **Technique:** Real-time weight modification.
*   **Implementation:** Blocked roads are modeled by assigning an effectively infinite traversal cost ($w = \infty$), causing the routing algorithm to exclude them from feasible paths. This enables real-time environmental awareness without requiring costly reconstruction of the graph.

### 3.5 Resource Allocation: Greedy Nearest-Neighbor
*   **Technique:** Proximity-based greedy strategy.
*   **Justification:** A greedy strategy was implemented to assign the nearest available ambulance to each emergency, minimizing response latency while maintaining high computational efficiency.

---

## 4. Cyber Security & Resilience
As a mission-critical urban system, CityMind incorporates:
- **Data Integrity**: Guarding against "adversarial graph injection" (fake road blocks).
- **System Availability**: Optimized $\mathcal{O}(n \log n)$ pathfinding to ensure uptime during high-stress simulation events.

---

## 5. Technology Stack
- **Language**: Python 3.x
- **Libraries**: `NetworkX` (Graph Analytics), `Heapq` (Priority Management), `Matplotlib` (Visualization).
