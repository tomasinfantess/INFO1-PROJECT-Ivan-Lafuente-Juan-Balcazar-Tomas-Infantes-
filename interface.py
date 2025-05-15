import tkinter as tk
from tkinter import filedialog, messagebox
from graph import Graph, AddNode, AddSegment, Plot, PlotNode, FindShortestPath
from node import Node


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Explorer")
        self.current_graph = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Botones
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)

        self.btn_example = tk.Button(self.btn_frame, text="Mostrar grafo ejemplo", command=self.show_example)
        self.btn_example.pack(side=tk.LEFT, padx=5)

        self.btn_load = tk.Button(self.btn_frame, text="Cargar grafo desde archivo", command=self.load_graph)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_plot_node = tk.Button(self.btn_frame, text="Mostrar vecinos de nodo", command=self.plot_node_neighbors)
        self.btn_plot_node.pack(side=tk.LEFT, padx=5)

        self.btn_shortest_path = tk.Button(self.btn_frame, text="Camino más corto", command=self.find_shortest_path)
        self.btn_shortest_path.pack(side=tk.LEFT, padx=5)

        # Área de información
        self.info_label = tk.Label(self.main_frame, text="Seleccione una opción para comenzar")
        self.info_label.pack(pady=10)

        # Configurar el grafo ejemplo
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

    def show_example(self):
        self.current_graph = self.example_graph
        Plot(self.current_graph)
        self.info_label.config(text="Grafo ejemplo mostrado")

    def load_graph(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo de grafo")
        if file_path:
            try:
                # Aquí iría la lógica para cargar el grafo desde archivo
                # Por ahora solo mostramos un mensaje
                self.info_label.config(text=f"Archivo seleccionado: {file_path}")
            except Exception as e:
                self.info_label.config(text=f"Error al cargar el archivo: {str(e)}")

    def plot_node_neighbors(self):
        if self.current_graph is None:
            self.info_label.config(text="Primero cargue o muestre un grafo")
            return

        # Crear ventana para seleccionar nodo
        node_window = tk.Toplevel(self.root)
        node_window.title("Seleccionar nodo")

        tk.Label(node_window, text="Ingrese el nombre del nodo:").pack(padx=10, pady=5)

        self.node_entry = tk.Entry(node_window)
        self.node_entry.pack(padx=10, pady=5)

        tk.Button(node_window, text="Mostrar vecinos",
                command=lambda: self.do_plot_node(node_window)).pack(pady=10)

    def do_plot_node(self, window):
        node_name = self.node_entry.get()
        if not node_name:
            self.info_label.config(text="Debe ingresar un nombre de nodo")
            return

        result = PlotNode(self.current_graph, node_name)
        if not result:
            self.info_label.config(text=f"No se encontró el nodo {node_name}")
        else:
            self.info_label.config(text=f"Mostrando vecinos de {node_name}")

        window.destroy()

    def find_shortest_path(self):
        if self.current_graph is None:
            self.info_label.config(text="Primero cargue o muestre un grafo")
            return

        # Crear ventana para seleccionar nodos
        path_window = tk.Toplevel(self.root)
        path_window.title("Encontrar camino más corto")

        tk.Label(path_window, text="Nodo origen:").pack(padx=10, pady=5)
        self.origin_entry = tk.Entry(path_window)
        self.origin_entry.pack(padx=10, pady=5)

        tk.Label(path_window, text="Nodo destino:").pack(padx=10, pady=5)
        self.destination_entry = tk.Entry(path_window)
        self.destination_entry.pack(padx=10, pady=5)

        tk.Button(path_window, text="Encontrar camino",
                command=lambda: self.do_find_shortest_path(path_window)).pack(pady=10)

    def do_find_shortest_path(self, window):
        origin_name = self.origin_entry.get()
        destination_name = self.destination_entry.get()

        if not origin_name or not destination_name:
            self.info_label.config(text="Debe ingresar ambos nodos")
            return

        path = FindShortestPath(self.current_graph, origin_name, destination_name)

        if path is None:
            messagebox.showinfo("Resultado", f"No hay camino entre {origin_name} y {destination_name}")
        else:
            message = f"Camino encontrado:\n"
            for node in path.nodes:
                message += f"{node.name} -> "
            message = message[:-4]  # Remove last arrow
            message += f"\nCosto total: {path.cost:.2f}"
            messagebox.showinfo("Resultado", message)

        window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()