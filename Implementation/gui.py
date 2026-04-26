import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx

class CityVisualizer:
    def __init__(self, city_graph, on_dispatch_callback, on_emergency_callback):
        self.city_graph = city_graph
        self.on_dispatch = on_dispatch_callback
        self.on_emergency = on_emergency_callback
        self.pending_emergencies = set()
        
        plt.ion()
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.patch.set_facecolor('#121212')
        self.ax.set_facecolor('#121212')

        # Neon Color Palette
        self.colors = {
            "Residential": "#2ecc71", "Hospital": "#e74c3c", 
            "School": "#f1c40f", "Industrial": "#e67e22", 
            "Power Plant": "#95a5a6", "Ambulance Depot": "#3498db"
        }

        # Setup "Launch" Button
        ax_dispatch = plt.axes([0.82, 0.05, 0.15, 0.08])
        self.btn_dispatch = Button(ax_dispatch, '🚀 DISPATCH AI', color='#27ae60', hovercolor='#2ecc71')
        self.btn_dispatch.label.set_color('white')
        self.btn_dispatch.label.set_fontweight('bold')
        self.btn_dispatch.on_clicked(self.handle_dispatch)

        # Connection for clicks
        self.fig.canvas.mpl_connect('button_press_event', self.handle_click)

    def handle_click(self, event):
        if event.inaxes != self.ax: return
        x, y = round(event.xdata), round(event.ydata)
        if 0 <= x < self.city_graph.size and 0 <= y < self.city_graph.size:
            self.pending_emergencies.add((x, y))
            self.on_emergency(x, y)
            self.draw_city(title=f"NEW ALERT: Emergency at ({x}, {y})")

    def handle_dispatch(self, event):
        self.on_dispatch()

    def draw_city(self, ambulance_path=None, title="CITYMIND: EMERGENCY COMMAND CENTER"):
        self.ax.clear()
        pos = {node_id: node_id for node_id in self.city_graph.nodes}
        
        # 1. Draw Roads
        for u, v, d in self.city_graph.graph.edges(data=True):
            if d.get('blocked'):
                nx.draw_networkx_edges(self.city_graph.graph, pos, edgelist=[(u,v)], 
                                       width=3, edge_color="#ff4757", style="dotted", ax=self.ax)
            else:
                nx.draw_networkx_edges(self.city_graph.graph, pos, edgelist=[(u,v)], 
                                       width=1, edge_color="#2f3542", alpha=0.5, ax=self.ax)

        # 2. Draw Nodes (Buildings)
        for b_type, color in self.colors.items():
            nodes = [n for n, d in self.city_graph.nodes.items() if d.location_type == b_type]
            nx.draw_networkx_nodes(self.city_graph.graph, pos, nodelist=nodes, 
                                   node_color=color, node_size=400, label=b_type, ax=self.ax)

        # 3. Highlight Pending Emergencies (Pulse Effect)
        if self.pending_emergencies:
            nx.draw_networkx_nodes(self.city_graph.graph, pos, nodelist=list(self.pending_emergencies), 
                                   node_color="none", edgecolors="#ff4757", linewidths=3, node_size=800, ax=self.ax)

        # 4. Animate Ambulance Movement
        if ambulance_path:
            self.animate_movement(ambulance_path, pos)
            if ambulance_path[-1] in self.pending_emergencies:
                self.pending_emergencies.remove(ambulance_path[-1])

        # 5. UI Elements: Title, Legend, Instructions
        self.ax.set_title(title, color='white', fontsize=20, fontweight='bold', pad=25)
        self.ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12, frameon=True, facecolor='#1e1e1e')
        
        # Add "How to use" text box
        instruction_text = "HELP:\n- CLICK MAP: Trigger Emergency\n- CLICK DISPATCH: Send nearest AI Ambulance"
        self.ax.text(0, -1.5, instruction_text, color='#f1c40f', fontsize=12, fontweight='bold', 
                     bbox=dict(facecolor='black', alpha=0.5))

        self.ax.set_xticks([]); self.ax.set_yticks([])
        self.fig.canvas.draw_idle()

    def animate_movement(self, path, pos):
        """ Visually moves the ambulance along the path. """
        for i in range(len(path)):
            # Draw current path trail
            if i > 0:
                trail = path[:i+1]
                edges = [(trail[j], trail[j+1]) for j in range(len(trail)-1)]
                nx.draw_networkx_edges(self.city_graph.graph, pos, edgelist=edges, 
                                       width=5, edge_color="#f1c40f", ax=self.ax)
            
            # Draw the Ambulance Icon (A bright yellow square)
            amb = nx.draw_networkx_nodes(self.city_graph.graph, pos, nodelist=[path[i]], 
                                         node_color="#f1c40f", node_size=700, node_shape='s', ax=self.ax)
            
            plt.pause(0.2) # Pause briefly to show movement
            
            # Remove ambulance for next frame (except for the last position)
            if i < len(path) - 1:
                amb.remove()

    def run(self):
        plt.show(block=True)
