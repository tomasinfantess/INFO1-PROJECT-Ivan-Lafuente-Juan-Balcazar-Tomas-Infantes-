import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from graph import Graph, AddNode, AddSegment, Plot, PlotNode, FindShortestPath
from node import Node
from airSpace import AirSpace
from kml_generator import KMLGenerator
import matplotlib.pyplot as plt
import subprocess
import os
from pathlib import Path
from PIL import Image, ImageTk
from segment import Segment






class GraphApp:
   def __init__(self, root):
       self.root = root
       self.root.title("Airspace Route Explorer - 10")
       self.current_graph = None
       self.current_airspace = None
       self.current_path = None
       self.selected_nodes = []
       self.r_key_pressed = False
       self.selected_for_path = []



       # Configuración de estilos
       self.setup_styles()


       # Datos de airspaces disponibles
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


       # Interfaz principal
       self.setup_ui()


       # Grafo de ejemplo
       self.example_graph = self.create_example_graph()
       self.current_graph = self.example_graph


   def setup_styles(self):
       """Configura los estilos visuales"""
       style = ttk.Style()
       style.configure("TFrame", background="#f0f0f0")
       style.configure("TLabelFrame", background="#f0f0f0", font=('Helvetica', 10, 'bold'))
       style.configure("TButton", font=('Helvetica', 9), padding=5)
       style.configure("Export.TButton", foreground="blue", font=('Helvetica', 10, 'bold'))
       style.configure("Title.TLabel", font=('Helvetica', 12, 'bold'), background="#f0f0f0")


   def setup_ui(self):
       """Construye la interfaz de usuario"""
       # Frame principal
       self.main_frame = ttk.Frame(self.root)
       self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


       # Título
       ttk.Label(
           self.main_frame,
           text="Airspace Route Explorer - 10",
           style="Title.TLabel"
       ).pack(pady=(0, 10))


       # Panel de selección de airspace
       self.setup_airspace_selector()


       # Panel de visualización
       self.setup_visualization_controls()


       # Panel de exportación KML
       self.setup_kml_export_controls()


       # Panel de información
       self.setup_info_panel()
       ttk.Button(
           self.main_frame,
           text="Manual",
           command=self.show_manual
       ).pack(pady=(5, 0))


       ttk.Button(
           self.main_frame,
           text="Para sacarte una sonrisa",
           command=self.show_image_window
       ).pack(pady=(5, 0))

       ttk.Button(
           self.main_frame,
           text="Mostrar vecinos de vecinos (ESTO TAMPOCO)",
           command=self.activate_neighbors_of_neighbors_mode
       ).pack(pady=(5, 0))

   def activate_neighbors_of_neighbors_mode(self):
       self.current_mode = 'vv'
       self.info_label.config(text="Modo activo: mostrar vecinos de vecinos - haz clic en un nodo")

   def plot_neighbors_of_neighbors(self, airspace, origin_point):
       import matplotlib.pyplot as plt

       plt.figure(figsize=(12, 8))

       # Todos los nodos en gris
       for point in airspace.nav_points:
           plt.plot(point.longitude, point.latitude, 'o', color='gray', markersize=3)
           plt.text(point.longitude, point.latitude, point.name, fontsize=8)

       # Nodo origen en azul
       plt.plot(origin_point.longitude, origin_point.latitude, 'bo', markersize=6, label='Origen')
       plt.text(origin_point.longitude, origin_point.latitude, origin_point.name, fontsize=10, color='blue')

       visited = {origin_point}
       second_level_nodes = set()

       # Vecinos directos en verde y líneas rojas desde el origen
       for neighbor in origin_point.neighbors:
           visited.add(neighbor)
           plt.plot(neighbor.longitude, neighbor.latitude, 'go', markersize=4)
           plt.text(neighbor.longitude, neighbor.latitude, neighbor.name, fontsize=9)

           # Línea desde origen
           plt.plot(
               [origin_point.longitude, neighbor.longitude],
               [origin_point.latitude, neighbor.latitude],
               'r-', linewidth=1.5
           )

           # Buscar vecinos de vecinos
           for second_neighbor in neighbor.neighbors:
               if second_neighbor not in visited:
                   second_level_nodes.add(second_neighbor)

                   # Nodo morado
                   plt.plot(second_neighbor.longitude, second_neighbor.latitude, 'mo', markersize=4)
                   plt.text(second_neighbor.longitude, second_neighbor.latitude, second_neighbor.name, fontsize=9)

                   # Línea desde vecino (si existe conexión directa)
                   if airspace.has_segment_between(neighbor, second_neighbor):
                       plt.plot(
                           [neighbor.longitude, second_neighbor.longitude],
                           [neighbor.latitude, second_neighbor.latitude],
                           'purple', linestyle='--', linewidth=1.2
                       )

       plt.xlabel('Longitud')
       plt.ylabel('Latitud')
       plt.grid(True)
       plt.title(f"Vecinos y vecinos de vecinos de {origin_point.name}")
       plt.tight_layout()
       plt.show()


   def show_image_window(self):
       image_window = tk.Toplevel(self.root)
       image_window.title("Imagen")

       # Ruta absoluta a la imagen
       image_path = "imagen.jpg"
       if not os.path.exists(image_path):
           messagebox.showerror("Error", "No se encuentra la imagen.")
           return

       img = Image.open(image_path)
       img = img.resize((500, 300))  # Ajustar tamaño si es necesario
       img_tk = ImageTk.PhotoImage(img)

       label = tk.Label(image_window, image=img_tk)
       label.image = img_tk  # ¡Importante! Para que no se elimine de memoria
       label.pack(padx=10, pady=10)

   def show_manual(self):
       manual_window = tk.Toplevel(self.root)
       manual_window.title("Manual de uso")
       manual_window.geometry("400x250")
       manual_window.resizable(False, False)

       instructions = (
           "✅ Clic encima de nodo:\n  Muestra vecinos\n\n"
           "✅ Control + Clic en 2 nodos:\n  Muestra shortest path\n\n"
           "✅ A + Clic en hueco vacío:\n"
           "  - Crea nodo\n"
           "  - Escribir nombre\n"
           "  - Clicar OK\n"
           "  - Clicar los nodos con los que se quiera crear un path\n"
           "  - Presionar Enter para que se acabe la edición"
       )

       label = tk.Label(manual_window, text=instructions, justify="left", anchor="w", font=("Helvetica", 10))
       label.pack(padx=10, pady=10, fill="both", expand=True)


   def setup_airspace_selector(self):
       """Configura el selector de airspace"""
       frame = ttk.LabelFrame(self.main_frame, text="Selección de Airspace")
       frame.pack(fill=tk.X, pady=5)


       # Combobox para seleccionar airspace
       self.airspace_var = tk.StringVar()
       self.airspace_combobox = ttk.Combobox(
           frame,
           textvariable=self.airspace_var,
           values=list(self.airspace_data.keys()),
           state="readonly",
           font=('Helvetica', 10)
       )
       self.airspace_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


       # Botón de carga
       ttk.Button(
           frame,
           text="Cargar Airspace",
           command=self.load_airspace
       ).pack(side=tk.LEFT, padx=5)


   def setup_visualization_controls(self):
       """Configura los controles de visualización"""
       frame = ttk.LabelFrame(self.main_frame, text="Visualización")
       frame.pack(fill=tk.X, pady=5)


       # Botones principales
       buttons = [
           ("Crear Grafo desde 0", self.create_empty_graph),
           ("Mostrar Grafo Ejemplo", self.show_example),
           ("Mostrar Vecinos", self.plot_node_neighbors),
           ("Calcular Ruta Corta", self.find_shortest_path),
       ]


       for text, command in buttons:
           ttk.Button(
               frame,
               text=text,
               command=command
           ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


   def setup_kml_export_controls(self):
       """Configura los controles de exportación KML"""
       frame = ttk.LabelFrame(self.main_frame, text="Exportación KML")
       frame.pack(fill=tk.X, pady=5)


       # Botón para exportar grafo completo
       ttk.Button(
           frame,
           text="Exportar Grafo Completo",
           command=self.export_full_graph_kml,
           style="Export.TButton"
       ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


       # Botón para exportar ruta (inicialmente deshabilitado)
       self.btn_export_path = ttk.Button(
           frame,
           text="Exportar Ruta Actual (NO TE LO PUEDES PERDER)",
           command=self.export_path_kml,
           style="Export.TButton",
           state=tk.DISABLED
       )
       self.btn_export_path.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)


       # Botón para abrir carpeta de exports
       ttk.Button(
           frame,
           text="Abrir Carpeta",
           command=self.open_export_folder
       ).pack(side=tk.LEFT, padx=5)


   def setup_info_panel(self):
       """Configura el panel de información"""
       frame = ttk.Frame(self.main_frame)
       frame.pack(fill=tk.X, pady=10)


       self.info_label = ttk.Label(
           frame,
           text="Seleccione un airspace y realice una operación",
           wraplength=500,
           background="#f0f0f0"
       )
       self.info_label.pack(fill=tk.X)


   # ====================== Funcionalidades principales ======================


   def create_example_graph(self):
       """Crea un grafo de ejemplo"""
       G = Graph()
       nodes = [
           Node("A", 1, 20), Node("B", 8, 17), Node("C", 15, 20),
           Node("D", 18, 15), Node("E", 2, 4), Node("F", 6, 5),
           Node("G", 12, 12), Node("H", 10, 3), Node("I", 19, 1),
           Node("J", 13, 5), Node("K", 3, 15), Node("L", 4, 10)
       ]


       for node in nodes:
           AddNode(G, node)


       segments = [
           ("AB", "A", "B"), ("AE", "A", "E"), ("AK", "A", "K"),
           ("BA", "B", "A"), ("BC", "B", "C"), ("BF", "B", "F"),
           ("BK", "B", "K"), ("BG", "B", "G"), ("CD", "C", "D"),
           ("CG", "C", "G"), ("DG", "D", "G"), ("DH", "D", "H"),
           ("DI", "D", "I"), ("EF", "E", "F"), ("FL", "F", "L"),
           ("GB", "G", "B"), ("GF", "G", "F"), ("GH", "G", "H"),
           ("ID", "I", "D"), ("IJ", "I", "J"), ("JI", "J", "I"),
           ("KA", "K", "A"), ("KL", "K", "L"), ("LK", "L", "K"),
           ("LF", "L", "F")
       ]


       for name, orig, dest in segments:
           AddSegment(G, name, orig, dest)


       return G

   def create_empty_graph(self):
       """Inicializa un grafo vacío y airspace vacío"""
       self.current_airspace = AirSpace()
       self.current_airspace.nav_points = []
       self.current_airspace.nav_segments = []
       self.current_airspace.nav_airports = []

       self.info_label.config(text="Nuevo grafo vacío creado")
       self.interactive_plot_airspace(self.current_airspace)


   def load_airspace(self):
       """Carga el airspace seleccionado"""
       selected = self.airspace_var.get()
       if not selected:
           messagebox.showwarning("Advertencia", "Seleccione un airspace primero")
           return


       try:
           airspace = AirSpace()
           data = self.airspace_data[selected]


           # Cargar datos (maneja posibles errores de archivo)
           if not all(Path(f).exists() for f in data.values()):
               raise FileNotFoundError("No se encontraron los archivos de datos")


           airspace.load_nav_points(data["nav"])
           airspace.load_nav_segments(data["seg"])
           airspace.load_nav_airports(data["airports"])
           airspace.build_neighbors()


           self.current_airspace = airspace
           self.info_label.config(text=f"Airspace '{selected}' cargado correctamente")
           self.interactive_plot_airspace(airspace)


       except Exception as e:
           messagebox.showerror(
               "Error",
               f"No se pudo cargar el airspace {selected}:\n{str(e)}"
           )
           self.info_label.config(text=f"Error al cargar {selected}")


   def plot_airspace(self, airspace):
       """Visualiza el airspace completo"""
       plt.figure(figsize=(12, 8))


       # Plot segments
       for segment in airspace.nav_segments:
           origin = airspace.find_nav_point_by_number(segment.origin_number)
           destination = airspace.find_nav_point_by_number(segment.destination_number)
           if origin and destination:
               plt.plot(
                   [origin.longitude, destination.longitude],
                   [origin.latitude, destination.latitude],
                   'gray', linestyle='-', linewidth=0.5
               )


               # Mostrar distancia en el segmento
               mid_x = (origin.longitude + destination.longitude) / 2
               mid_y = (origin.latitude + destination.latitude) / 2
               plt.text(mid_x, mid_y, f"{segment.distance:.1f} km", fontsize=6)


       # Plot navigation points
       for point in airspace.nav_points:
           plt.plot(point.longitude, point.latitude, 'ro', markersize=3)
           plt.text(point.longitude, point.latitude, point.name, fontsize=8)


       # Plot airports
       for airport in airspace.nav_airports:
           if airport.sids:
               first_sid = airport.sids[0]
               plt.plot(first_sid.longitude, first_sid.latitude, 'bo', markersize=5)
               plt.text(
                   first_sid.longitude, first_sid.latitude,
                   airport.name, fontsize=10, color='blue'
               )


       plt.xlabel('Longitud')
       plt.ylabel('Latitud')
       plt.grid(True)
       plt.title(f"Airspace: {self.airspace_var.get()}")
       plt.tight_layout()
       plt.show()


   def show_example(self):
       """Muestra el grafo de ejemplo"""
       self.current_graph = self.example_graph
       Plot(self.current_graph)
       self.info_label.config(text="Grafo de ejemplo mostrado")


   def plot_node_neighbors(self):
       """Muestra los vecinos de un nodo"""
       if not self.current_airspace:
           messagebox.showwarning("Advertencia", "Primero cargue un airspace")
           return


       # Ventana para seleccionar nodo
       node_window = tk.Toplevel(self.root)
       node_window.title("Seleccionar Nodo")
       node_window.resizable(False, False)


       ttk.Label(node_window, text="Nombre del nodo:").pack(padx=10, pady=5)


       self.node_entry = ttk.Entry(node_window)
       self.node_entry.pack(padx=10, pady=5)


       ttk.Button(
           node_window,
           text="Mostrar Vecinos",
           command=lambda: self.do_plot_node(node_window)
       ).pack(pady=10)


   def do_plot_node(self, window):
       """Procesa la selección de nodo para mostrar vecinos"""
       node_name = self.node_entry.get().strip()
       if not node_name:
           messagebox.showwarning("Advertencia", "Ingrese un nombre de nodo")
           return


       point = self.current_airspace.find_nav_point_by_name(node_name)
       if not point:
           messagebox.showerror("Error", f"Nodo '{node_name}' no encontrado")
           return


       self.plot_airspace_node(self.current_airspace, point)
       window.destroy()


   def plot_airspace_node(self, airspace, origin_point):
       """Visualiza un nodo y sus vecinos"""
       plt.figure(figsize=(12, 8))


       # Todos los nodos en gris
       for point in airspace.nav_points:
           plt.plot(point.longitude, point.latitude, 'o', color='gray', markersize=3)
           plt.text(point.longitude, point.latitude, point.name, fontsize=8)


       # Nodo origen en azul
       plt.plot(
           origin_point.longitude, origin_point.latitude,
           'bo', markersize=5, label='Origen'
       )
       plt.text(
           origin_point.longitude, origin_point.latitude,
           origin_point.name, fontsize=10, color='blue'
       )


       # Vecinos en verde y conexiones en rojo
       for neighbor in origin_point.neighbors:
           plt.plot(
               neighbor.longitude, neighbor.latitude,
               'go', markersize=4, label='Vecino'
           )
           plt.text(neighbor.longitude, neighbor.latitude, neighbor.name, fontsize=9)


           plt.plot(
               [origin_point.longitude, neighbor.longitude],
               [origin_point.latitude, neighbor.latitude],
               'r-', linewidth=1
           )


           # Mostrar distancia
           mid_x = (origin_point.longitude + neighbor.longitude) / 2
           mid_y = (origin_point.latitude + neighbor.latitude) / 2


           for segment in airspace.nav_segments:
               if (segment.origin_number == origin_point.number and
                       segment.destination_number == neighbor.number):
                   plt.text(mid_x, mid_y, f"{segment.distance:.1f} km", fontsize=7)
                   break


       plt.xlabel('Longitud')
       plt.ylabel('Latitud')
       plt.grid(True)
       plt.title(f"Vecinos de {origin_point.name}")
       plt.legend()
       plt.tight_layout()
       plt.show()


   def find_shortest_path(self):
       """Calcula la ruta más corta entre dos nodos"""
       if not self.current_airspace:
           messagebox.showwarning("Advertencia", "Primero cargue un airspace")
           return


       # Ventana para seleccionar origen y destino
       path_window = tk.Toplevel(self.root)
       path_window.title("Calcular Ruta Más Corta")
       path_window.resizable(False, False)


       ttk.Label(path_window, text="Nodo origen:").pack(padx=10, pady=5)
       self.origin_entry = ttk.Entry(path_window)
       self.origin_entry.pack(padx=10, pady=5)


       ttk.Label(path_window, text="Nodo destino:").pack(padx=10, pady=5)
       self.destination_entry = ttk.Entry(path_window)
       self.destination_entry.pack(padx=10, pady=5)


       ttk.Button(
           path_window,
           text="Calcular Ruta",
           command=lambda: self.do_find_shortest_path(path_window)
       ).pack(pady=10)


   def do_find_shortest_path(self, window):
       """Procesa el cálculo de la ruta más corta"""
       origin_name = self.origin_entry.get().strip()
       destination_name = self.destination_entry.get().strip()


       if not origin_name or not destination_name:
           messagebox.showwarning("Advertencia", "Ingrese ambos nodos")
           return


       origin = self.current_airspace.find_nav_point_by_name(origin_name)
       destination = self.current_airspace.find_nav_point_by_name(destination_name)


       if not origin:
           messagebox.showerror("Error", f"Nodo origen '{origin_name}' no encontrado")
           return
       if not destination:
           messagebox.showerror("Error", f"Nodo destino '{destination_name}' no encontrado")
           return


       # Convertir airspace a grafo para el algoritmo de ruta
       graph = self.airspace_to_graph(self.current_airspace)
       path = FindShortestPath(graph, origin_name, destination_name)


       if not path:
           messagebox.showinfo("Resultado", f"No hay ruta entre {origin_name} y {destination_name}")
           window.destroy()
           return


       self.current_path = path  # Guardar para exportación
       self.btn_export_path.config(state=tk.NORMAL)  # Habilitar exportación


       # Mostrar resultados
       self.plot_airspace_path(self.current_airspace, path)


       # Ventana de resultados con opción de exportar
       result_window = tk.Toplevel(self.root)
       result_window.title("Resultado de Ruta")


       ttk.Label(
           result_window,
           text=f"Ruta encontrada: {' → '.join([n.name for n in path.nodes])}"
       ).pack(padx=10, pady=5)


       ttk.Label(
           result_window,
           text=f"Distancia total: {path.cost:.2f} km"
       ).pack(padx=10, pady=5)


       ttk.Button(
           result_window,
           text="Exportar a KML",
           command=lambda: self.export_path_kml(window=result_window),
           style="Export.TButton"
       ).pack(pady=10)


       window.destroy()


   def airspace_to_graph(self, airspace):
       """Convierte un airspace a un grafo para el algoritmo de ruta"""
       graph = Graph()


       # Añadir nodos (convertir lat/lon a coordenadas simples)
       for point in airspace.nav_points:
           AddNode(graph, Node(point.name, point.longitude, point.latitude))


       # Añadir segmentos
       for segment in airspace.nav_segments:
           origin = airspace.find_nav_point_by_number(segment.origin_number)
           destination = airspace.find_nav_point_by_number(segment.destination_number)
           if origin and destination:
               segment_name = f"{origin.name}_{destination.name}"
               AddSegment(graph, segment_name, origin.name, destination.name)


       return graph


   def plot_airspace_path(self, airspace, path):
       """Visualiza una ruta en el airspace"""
       plt.figure(figsize=(12, 8))


       # Todos los segmentos en gris
       for segment in airspace.nav_segments:
           origin = airspace.find_nav_point_by_number(segment.origin_number)
           destination = airspace.find_nav_point_by_number(segment.destination_number)
           if origin and destination:
               plt.plot(
                   [origin.longitude, destination.longitude],
                   [origin.latitude, destination.latitude],
                   'gray', linestyle='-', linewidth=0.5
               )


       # Todos los nodos en rojo
       for point in airspace.nav_points:
           plt.plot(point.longitude, point.latitude, 'ro', markersize=3)
           plt.text(point.longitude, point.latitude, point.name, fontsize=8)


       # Dibujar la ruta en azul
       for i in range(len(path.nodes) - 1):
           current = airspace.find_nav_point_by_name(path.nodes[i].name)
           next_node = airspace.find_nav_point_by_name(path.nodes[i + 1].name)


           if current and next_node:
               plt.plot(
                   [current.longitude, next_node.longitude],
                   [current.latitude, next_node.latitude],
                   'b-', linewidth=2, label='Ruta' if i == 0 else ""
               )


       # Marcar origen y destino
       origin = airspace.find_nav_point_by_name(path.nodes[0].name)
       destination = airspace.find_nav_point_by_name(path.nodes[-1].name)


       if origin:
           plt.plot(
               origin.longitude, origin.latitude,
               'go', markersize=6, label='Origen'
           )
       if destination:
           plt.plot(
               destination.longitude, destination.latitude,
               'ro', markersize=6, label='Destino'
           )


       plt.xlabel('Longitud')
       plt.ylabel('Latitud')
       plt.grid(True)
       plt.title(f"Ruta más corta: {path.nodes[0].name} → {path.nodes[-1].name}")
       plt.legend()
       plt.tight_layout()
       plt.show()


   # ====================== Funcionalidades KML ======================


   def export_full_graph_kml(self):
       """Exporta el grafo completo a KML"""
       if not self.current_airspace:
           messagebox.showwarning("Advertencia", "Primero cargue un airspace")
           return


       filename = filedialog.asksaveasfilename(
           defaultextension=".kml",
           filetypes=[("KML files", "*.kml")],
           title="Guardar grafo completo como KML",
           initialfile=f"airspace_{self.airspace_var.get()}.kml"
       )
       if not filename:
           return


       generator = KMLGenerator(self.current_airspace)
       success, result = generator.generate_kml(
           elements=["airports", "navpoints", "airways"],
           filename=filename
       )


       if success:
           self.info_label.config(text=f"Grafo exportado a: {filename}")
           if messagebox.askyesno("Éxito", "¿Abrir en Google Earth?"):
               self.open_in_google_earth(filename)
       else:
           messagebox.showerror("Error", f"Error al exportar:\n{result}")


   def export_path_kml(self, window=None):
       """Exporta la ruta actual a KML"""
       if not self.current_path:
           messagebox.showwarning("Advertencia", "No hay ruta calculada")
           return


       origin = self.current_path.nodes[0].name
       destination = self.current_path.nodes[-1].name


       filename = filedialog.asksaveasfilename(
           defaultextension=".kml",
           filetypes=[("KML files", "*.kml")],
           title="Guardar ruta como KML",
           initialfile=f"ruta_{origin}_to_{destination}.kml"
       )
       if not filename:
           return


       generator = KMLGenerator(self.current_airspace)
       success, result = generator.generate_path_kml(
           path=self.current_path,
           filename=filename
       )


       if success:
           self.info_label.config(text=f"Ruta exportada a: {filename}")
           if window:
               window.destroy()
           if messagebox.askyesno("Éxito", "¿Abrir en Google Earth?"):
               self.open_in_google_earth(filename)
       else:
           messagebox.showerror("Error", f"Error al exportar ruta:\n{result}")


   def open_in_google_earth(self, kml_file):
       """Abre un archivo KML en Google Earth"""
       if not os.path.exists(kml_file):
           messagebox.showerror("Error", f"Archivo no encontrado:\n{kml_file}")
           return


       try:
           if os.name == 'nt':  # Windows
               os.startfile(kml_file)
           else:  # Linux/Mac
               subprocess.run(["google-earth-pro", kml_file])
       except Exception as e:
           messagebox.showerror(
               "Error",
               f"No se pudo abrir Google Earth:\n{str(e)}\n\n"
               "Asegúrese de tener Google Earth instalado."
           )


   def open_export_folder(self):
       """Abre la carpeta de exportaciones"""
       try:
           current_dir = os.getcwd()
           if os.name == 'nt':  # Windows
               os.startfile(current_dir)
           else:  # Linux/Mac
               subprocess.run(["xdg-open", current_dir])
       except Exception as e:
           messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{str(e)}")

   def interactive_plot_airspace(self, airspace):
       import matplotlib.pyplot as plt
       from tkinter import simpledialog, messagebox
       from segment import Segment

       fig, ax = plt.subplots(figsize=(12, 8))
       self.selected_nodes = []
       self.current_mode = None  # 'a', 'd', o None
       coords_to_point = {}

       # Dibujar el grafo existente
       for segment in airspace.nav_segments:
           origin = airspace.find_nav_point_by_number(segment.origin_number)
           destination = airspace.find_nav_point_by_number(segment.destination_number)
           if origin and destination:
               ax.plot(
                   [origin.longitude, destination.longitude],
                   [origin.latitude, destination.latitude],
                   'gray', linestyle='-', linewidth=0.5
               )

       for point in airspace.nav_points:
           coords = (point.longitude, point.latitude)
           coords_to_point[coords] = point
           ax.plot(point.longitude, point.latitude, 'ro', markersize=4)
           ax.text(point.longitude, point.latitude, point.name, fontsize=7)

       ax.set_title(f"Airspace interactivo: {self.airspace_var.get()}")
       ax.set_xlabel("Longitud")
       ax.set_ylabel("Latitud")
       ax.grid(True)
       fig.tight_layout()

       def on_key_press(event):
           # Actualizar el modo según la tecla presionada
           if event.key == 'a':
               self.current_mode = 'a'
               self.info_label.config(text="Modo creación de nodos (a) - Haz clic donde quieras añadir un nodo")
           elif event.key == 'd':
               self.current_mode = 'd'
               self.info_label.config(text="Modo creación de conexiones (d) - Selecciona 2 nodos para conectarlos")
           elif event.key == 'control':
               self.current_mode = 'path'
               self.info_label.config(text="Modo ruta más corta (Control) - Selecciona 2 nodos")

       def on_key_release(event):
           # Limpiar el modo cuando se suelta la tecla
           if event.key in ['a', 'd', 'control']:
               self.current_mode = None
               self.info_label.config(text="Modo normal - Haz clic en un nodo para ver sus vecinos")

       def on_click(event):
           if not event.inaxes:
               return

           click_x, click_y = event.xdata, event.ydata

           # Encontrar el punto más cercano al clic
           min_dist = float("inf")
           closest_point = None
           for (x, y), point in coords_to_point.items():
               dist = (x - click_x) ** 2 + (y - click_y) ** 2
               if dist < min_dist and dist < 0.05:
                   min_dist = dist
                   closest_point = point

           # Modo normal - mostrar vecinos
           if self.current_mode is None and closest_point:
               self.plot_airspace_node(airspace, closest_point)
               return

           # Modo creación de nodos (tecla 'a')
           if self.current_mode == 'a':
               # Preguntar por el nombre del nodo
               name = simpledialog.askstring("Nuevo nodo", "Nombre del nuevo nodo:")
               if name:
                   # Crear el nuevo nodo
                   new_node = Node(name, click_x, click_y)
                   airspace.nav_points.append(new_node)
                   coords_to_point[(click_x, click_y)] = new_node

                   # Dibujar el nuevo nodo
                   ax.plot(click_x, click_y, 'co', markersize=6)
                   ax.text(click_x, click_y, name, fontsize=8)
                   fig.canvas.draw()

                   self.info_label.config(text=f"Nodo '{name}' creado en ({click_x:.2f}, {click_y:.2f})")

           # Modo creación de conexiones (tecla 'd')
           elif self.current_mode == 'd' and closest_point:
               if len(self.selected_nodes) == 0:
                   # Primer nodo seleccionado para la conexión
                   self.selected_nodes.append(closest_point)
                   self.info_label.config(text=f"Seleccionado nodo {closest_point.name}. Seleccione el nodo destino")
               else:
                   # Segundo nodo seleccionado, crear conexión
                   origin = self.selected_nodes[0]
                   destination = closest_point

                   # Verificar si la conexión ya existe
                   exists = False
                   for seg in airspace.nav_segments:
                       if (seg.origin_number == origin.number and
                               seg.destination_number == destination.number):
                           exists = True
                           break

                   if not exists:
                       # Crear segmento en ambas direcciones
                       distance = ((origin.longitude - destination.longitude) ** 2 +
                                   (origin.latitude - destination.latitude) ** 2) ** 0.5

                       seg1 = Segment(
                           origin_number=origin.number,
                           destination_number=destination.number,
                           name=f"{origin.name}_{destination.name}",
                           distance=distance
                       )

                       seg2 = Segment(
                           origin_number=destination.number,
                           destination_number=origin.number,
                           name=f"{destination.name}_{origin.name}",
                           distance=distance
                       )

                       airspace.nav_segments.extend([seg1, seg2])

                       # Dibujar la nueva conexión
                       ax.plot(
                           [origin.longitude, destination.longitude],
                           [origin.latitude, destination.latitude],
                           'b-', linewidth=1.5
                       )
                       fig.canvas.draw()

                       self.info_label.config(
                           text=f"Conexión creada: {origin.name} ↔ {destination.name} "
                                f"(Distancia: {distance:.2f} km)"
                       )
                   else:
                       self.info_label.config(text=f"La conexión {origin.name} ↔ {destination.name} ya existe")

                   self.selected_nodes.clear()

           # Modo ruta más corta (tecla control)
           elif self.current_mode == 'path' and closest_point:
               self.selected_nodes.append(closest_point)
               if len(self.selected_nodes) == 2:
                   self.handle_shortest_path_selection()
                   self.selected_nodes.clear()


           elif self.current_mode == 'vv' and closest_point:
               self.plot_neighbors_of_neighbors(airspace, closest_point)

       # Conectar los eventos
       fig.canvas.mpl_connect('button_press_event', on_click)
       fig.canvas.mpl_connect('key_press_event', on_key_press)
       fig.canvas.mpl_connect('key_release_event', on_key_release)

       # Mostrar instrucciones
       messagebox.showinfo(
           "Instrucciones",
           "Modo interactivo:\n\n"
           "✅ Clic en nodo: Muestra vecinos\n"
           "✅ Control + Clic en 2 nodos: Calcula ruta más corta\n"
           "✅ Tecla 'a' + Clic: Crear nuevo nodo\n"
           "✅ Tecla 'd' + Clic en 2 nodos: Crear conexión directa\n"
           "\nPresiona la tecla antes de hacer clic para activar los modos"
       )

       plt.show()

   def handle_shortest_path_selection(self):
       """Maneja la selección de dos nodos para calcular la ruta"""
       if len(self.selected_nodes) != 2:
           return

       origin, destination = self.selected_nodes
       graph = self.airspace_to_graph(self.current_airspace)
       path = FindShortestPath(graph, origin.name, destination.name)

       if path:
           self.current_path = path
           self.btn_export_path.config(state=tk.NORMAL)
           self.plot_airspace_path(self.current_airspace, path)
       else:
           messagebox.showinfo("Sin ruta", f"No hay camino entre {origin.name} y {destination.name}")




if __name__ == "__main__":
   root = tk.Tk()


   # Configuración de la ventana principal
   root.geometry("800x600")
   root.minsize(700, 500)
   root.eval('tk::PlaceWindow . center')  # Centrar ventana


   app = GraphApp(root)
   root.mainloop()

