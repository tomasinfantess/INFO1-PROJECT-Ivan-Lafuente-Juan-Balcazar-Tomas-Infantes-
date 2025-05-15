import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from graph import Graph, AddNode, AddSegment, Plot, PlotNode
from node import Node
from airSpace import AirSpace
import matplotlib.pyplot as plt


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Explorer")
        self.current_graph = None
        self.current_airspace = None
        self.airspace_data = {
            "Catalunya": {
                "nav": "Cat_nav.txt",
                "seg": "Cat_seg.txt",
                "airports": "Cat_aer.txt"
            },
            "España": {
                "nav": "Spa_nav.txt",
                "seg": "Spa_seg.txt",
                "airports": "Spa_ger.txt"
            },
            "Europe": {
                "nav": "Eur_nav.txt",
                "seg": "Eur_seg.txt",
                "airports": "Eur_ger.txt"
            }
        }

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Airspace selection
        self.airspace_frame = tk.LabelFrame(self.main_frame, text="Airspace Selection")
        self.airspace_frame.pack(fill=tk.X, pady=5)

        self.airspace_var = tk.StringVar()
        self.airspace_combobox = ttk.Combobox(self.airspace_frame,
                                              textvariable=self.airspace_var,
                                              values=list(self.airspace_data.keys()))
        self.airspace_combobox.pack(side=tk.LEFT, padx=5)
        self.airspace_combobox.bind("<<ComboboxSelected>>", self.load_airspace)

        # Buttons
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)

        self.btn_example = tk.Button(self.btn_frame, text="Show Example Graph", command=self.show_example)
        self.btn_example.pack(side=tk.LEFT, padx=5)

        self.btn_plot_node = tk.Button(self.btn_frame, text="Show Node Neighbors", command=self.plot_node_neighbors)
        self.btn_plot_node.pack(side=tk.LEFT, padx=5)

        self.btn_shortest_path = tk.Button(self.btn_frame, text="Shortest Path", command=self.find_shortest_path)
        self.btn_shortest_path.pack(side=tk.LEFT, padx=5)

        # Info area
        self.info_label = tk.Label(self.main_frame, text="Select an option to begin")
        self.info_label.pack(pady=10)

        # Example graph
        self.example_graph = self.create_example_graph()
        self.current_graph = self.example_graph

    def create_example_graph(self):
        G = Graph()
        AddNode(G, Node("A", 1, 20))
        AddNode(G, Node("B", 8, 17))
        AddNode(G, Node("C", 15, 20))
        AddNode(G, Node("D", 18, 15))
        AddNode(G, Node("E", 2, 4))
        AddNode(G, Node("F", 6, 5))
        AddNode(G, Node("G", 12, 12))
        AddNode(G, Node("H", 10, 3))
        AddNode(G, Node("I", 19, 1))
        AddNode(G, Node("J", 13, 5))
        AddNode(G, Node("K", 3, 15))
        AddNode(G, Node("L", 4, 10))

        AddSegment(G, "AB", "A", "B")
        AddSegment(G, "AE", "A", "E")
        AddSegment(G, "AK", "A", "K")
        AddSegment(G, "BA", "B", "A")
        AddSegment(G, "BC", "B", "C")
        AddSegment(G, "BF", "B", "F")
        AddSegment(G, "BK", "B", "K")
        AddSegment(G, "BG", "B", "G")
        AddSegment(G, "CD", "C", "D")
        AddSegment(G, "CG", "C", "G")
        AddSegment(G, "DG", "D", "G")
        AddSegment(G, "DH", "D", "H")
        AddSegment(G, "DI", "D", "I")
        AddSegment(G, "EF", "E", "F")
        AddSegment(G, "FL", "F", "L")
        AddSegment(G, "GB", "G", "B")
        AddSegment(G, "GF", "G", "F")
        AddSegment(G, "GH", "G", "H")
        AddSegment(G, "ID", "I", "D")
        AddSegment(G, "IJ", "I", "J")
        AddSegment(G, "JI", "J", "I")
        AddSegment(G, "KA", "K", "A")
        AddSegment(G, "KL", "K", "L")
        AddSegment(G, "LK", "L", "K")
        AddSegment(G, "LF", "L", "F")
        return G

    def load_airspace(self, event=None):
        selected = self.airspace_var.get()
        if selected in self.airspace_data:
            try:
                airspace = AirSpace()
                airspace.load_nav_points(self.airspace_data[selected]["nav"])
                airspace.load_nav_segments(self.airspace_data[selected]["seg"])
                airspace.load_nav_airports(self.airspace_data[selected]["airports"])
                airspace.build_neighbors()
                self.current_airspace = airspace
                self.info_label.config(text=f"{selected} airspace loaded successfully")
                self.plot_airspace(airspace)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {selected} airspace: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a valid airspace")

    def plot_airspace(self, airspace):
        plt.figure(figsize=(12, 8))

        # Plot segments
        for segment in airspace.nav_segments:
            origin = airspace.find_nav_point_by_number(segment.origin_number)
            destination = airspace.find_nav_point_by_number(segment.destination_number)
            if origin and destination:
                plt.plot([origin.longitude, destination.longitude],
                         [origin.latitude, destination.latitude],
                         'gray', linestyle='-', linewidth=0.5)

                mid_x = (origin.longitude + destination.longitude) / 2
                mid_y = (origin.latitude + destination.latitude) / 2
                plt.text(mid_x, mid_y, f"{segment.distance:.1f}", fontsize=6)

        # Plot nodes
        for point in airspace.nav_points:
            plt.plot(point.longitude, point.latitude, 'ro', markersize=3)
            plt.text(point.longitude, point.latitude, point.name, fontsize=8)

        # Plot airports
        for airport in airspace.nav_airports:
            if airport.sids:
                first_sid = airport.sids[0]
                plt.plot(first_sid.longitude, first_sid.latitude, 'bo', markersize=5)
                plt.text(first_sid.longitude, first_sid.latitude,
                         airport.name, fontsize=10, color='blue')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.title(f"Airspace: {self.airspace_var.get()}")
        plt.show()

    def show_example(self):
        self.current_graph = self.example_graph
        Plot(self.current_graph)
        self.info_label.config(text="Example graph displayed")

    def plot_node_neighbors(self):
        if self.current_airspace is None:
            self.info_label.config(text="First load an airspace")
            return

        node_window = tk.Toplevel(self.root)
        node_window.title("Select Node")

        tk.Label(node_window, text="Enter node name:").pack(padx=10, pady=5)
        self.node_entry = tk.Entry(node_window)
        self.node_entry.pack(padx=10, pady=5)

        tk.Button(node_window, text="Show Neighbors",
                  command=lambda: self.do_plot_node(node_window)).pack(pady=10)

    def do_plot_node(self, window):
        node_name = self.node_entry.get()
        if not node_name:
            self.info_label.config(text="Please enter a node name")
            return

        if self.current_airspace:
            point = self.current_airspace.find_nav_point_by_name(node_name)
            if point:
                self.plot_airspace_node(self.current_airspace, point)
                self.info_label.config(text=f"Showing neighbors of {node_name}")
            else:
                self.info_label.config(text=f"Node {node_name} not found")
        window.destroy()

    def plot_airspace_node(self, airspace, origin_point):
        plt.figure(figsize=(12, 8))

        # Plot all nodes in gray
        for point in airspace.nav_points:
            plt.plot(point.longitude, point.latitude, 'o', color='gray', markersize=3)
            plt.text(point.longitude, point.latitude, point.name, fontsize=8)

        # Plot origin node in blue
        plt.plot(origin_point.longitude, origin_point.latitude, 'bo', markersize=5)
        plt.text(origin_point.longitude, origin_point.latitude,
                 origin_point.name, fontsize=10, color='blue')

        # Plot neighbors in green and connections in red
        for neighbor in origin_point.neighbors:
            plt.plot(neighbor.longitude, neighbor.latitude, 'go', markersize=4)
            plt.text(neighbor.longitude, neighbor.latitude, neighbor.name, fontsize=9)

            plt.plot([origin_point.longitude, neighbor.longitude],
                     [origin_point.latitude, neighbor.latitude],
                     'r-', linewidth=1)

            mid_x = (origin_point.longitude + neighbor.longitude) / 2
            mid_y = (origin_point.latitude + neighbor.latitude) / 2

            # Find the segment distance
            distance = None
            for segment in airspace.nav_segments:
                if (segment.origin_number == origin_point.number and
                        segment.destination_number == neighbor.number):
                    distance = segment.distance
                    break

            if distance:
                plt.text(mid_x, mid_y, f"{distance:.1f}", fontsize=7)

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.title(f"Neighbors of {origin_point.name}")
        plt.show()

    def find_shortest_path(self):
        if self.current_airspace is None:
            self.info_label.config(text="First load an airspace")
            return

        path_window = tk.Toplevel(self.root)
        path_window.title("Find Shortest Path")

        tk.Label(path_window, text="Origin node:").pack(padx=10, pady=5)
        self.origin_entry = tk.Entry(path_window)
        self.origin_entry.pack(padx=10, pady=5)

        tk.Label(path_window, text="Destination node:").pack(padx=10, pady=5)
        self.destination_entry = tk.Entry(path_window)
        self.destination_entry.pack(padx=10, pady=5)

        tk.Button(path_window, text="Find Path",
                  command=lambda: self.do_find_shortest_path(path_window)).pack(pady=10)

    def do_find_shortest_path(self, window):
        origin_name = self.origin_entry.get()
        destination_name = self.destination_entry.get()

        if not origin_name or not destination_name:
            self.info_label.config(text="Please enter both nodes")
            return

        if self.current_airspace:
            origin = self.current_airspace.find_nav_point_by_name(origin_name)
            destination = self.current_airspace.find_nav_point_by_name(destination_name)

            if not origin:
                messagebox.showerror("Error", f"Origin node {origin_name} not found")
                return
            if not destination:
                messagebox.showerror("Error", f"Destination node {destination_name} not found")
                return

            # Convert airspace to graph for path finding
            graph = self.airspace_to_graph(self.current_airspace)
            path = FindShortestPath(graph, origin_name, destination_name)

            if path is None:
                messagebox.showinfo("Result", f"No path between {origin_name} and {destination_name}")
            else:
                self.plot_airspace_path(self.current_airspace, path)
                message = f"Path found:\n"
                for node in path.nodes:
                    message += f"{node.name} -> "
                message = message[:-4]  # Remove last arrow
                message += f"\nTotal cost: {path.cost:.2f} km"
                messagebox.showinfo("Result", message)

        window.destroy()

    def airspace_to_graph(self, airspace):
        graph = Graph()

        # Add nodes
        for point in airspace.nav_points:
            # Convert lat/long to x/y coordinates for plotting
            # Simple conversion for display purposes
            x = point.longitude * 10  # Scale for better visualization
            y = point.latitude * 10  # Scale for better visualization
            AddNode(graph, Node(point.name, x, y))

        # Add segments
        for segment in airspace.nav_segments:
            origin = airspace.find_nav_point_by_number(segment.origin_number)
            destination = airspace.find_nav_point_by_number(segment.destination_number)
            if origin and destination:
                segment_name = f"{origin.name}_{destination.name}"
                AddSegment(graph, segment_name, origin.name, destination.name)

        return graph

    def plot_airspace_path(self, airspace, path):
        plt.figure(figsize=(12, 8))

        # Plot all nodes and segments
        for segment in airspace.nav_segments:
            origin = airspace.find_nav_point_by_number(segment.origin_number)
            destination = airspace.find_nav_point_by_number(segment.destination_number)
            if origin and destination:
                plt.plot([origin.longitude, destination.longitude],
                         [origin.latitude, destination.latitude],
                         'gray', linestyle='-', linewidth=0.5)

        for point in airspace.nav_points:
            plt.plot(point.longitude, point.latitude, 'ro', markersize=3)
            plt.text(point.longitude, point.latitude, point.name, fontsize=8)

        # Plot the path
        for i in range(len(path.nodes) - 1):
            current_name = path.nodes[i].name
            next_name = path.nodes[i + 1].name

            current_point = airspace.find_nav_point_by_name(current_name)
            next_point = airspace.find_nav_point_by_name(next_name)

            if current_point and next_point:
                plt.plot([current_point.longitude, next_point.longitude],
                         [current_point.latitude, next_point.latitude],
                         'b-', linewidth=2)

                plt.plot(current_point.longitude, current_point.latitude, 'bo', markersize=5)
                plt.text(current_point.longitude, current_point.latitude,
                         current_point.name, fontsize=10, color='blue')

        # Plot the last node
        last_node = path.nodes[-1]
        last_point = airspace.find_nav_point_by_name(last_node.name)
        if last_point:
            plt.plot(last_point.longitude, last_point.latitude, 'bo', markersize=5)
            plt.text(last_point.longitude, last_point.latitude,
                     last_point.name, fontsize=10, color='blue')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()