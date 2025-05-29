import simplekml
import os
from datetime import datetime


class KMLGenerator:
    def __init__(self, airspace):
        self.airspace = airspace

    def generate_kml(self, elements=None, filename=None):
        """
        Genera un archivo KML con los elementos especificados del espacio aéreo.

        Args:
            elements (list): Lista de elementos a incluir ("airports", "navpoints", "airways")
            filename (str): Nombre del archivo de salida (opcional)

        Returns:
            tuple: (success: bool, filename: str)
        """
        if elements is None:
            elements = ["airports", "navpoints", "airways"]

        try:
            kml = simplekml.Kml()
            kml.document.name = f"Airspace Data - {datetime.now().strftime('%Y-%m-%d')}"

            # Agregar aeropuertos
            if "airports" in elements:
                airports_folder = kml.newfolder(name="Airports")
                for airport in self.airspace.nav_airports:
                    if airport.sids:
                        first_sid = airport.sids[0]
                        pnt = airports_folder.newpoint(
                            name=airport.name,
                            coords=[(first_sid.longitude, first_sid.latitude)],
                            description=f"Airport: {airport.name}\nICAO: {airport.icao}"
                        )
                        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/pal2/icon57.png"

            # Agregar puntos de navegación
            if "navpoints" in elements:
                navpoints_folder = kml.newfolder(name="Navigation Points")
                for point in self.airspace.nav_points:
                    pnt = navpoints_folder.newpoint(
                        name=point.name,
                        coords=[(point.longitude, point.latitude)],
                        description=f"Nav Point: {point.name}\nFrequency: {point.frequency if hasattr(point, 'frequency') else 'N/A'}"
                    )
                    pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/pal2/icon18.png"

            # Agregar rutas aéreas
            if "airways" in elements:
                airways_folder = kml.newfolder(name="Airways")
                for segment in self.airspace.nav_segments:
                    origin = self.airspace.find_nav_point_by_number(segment.origin_number)
                    destination = self.airspace.find_nav_point_by_number(segment.destination_number)
                    if origin and destination:
                        lin = airways_folder.newlinestring(
                            name=f"{origin.name} to {destination.name}",
                            description=f"Distance: {segment.distance:.1f} km",
                            coords=[(origin.longitude, origin.latitude),
                                    (destination.longitude, destination.latitude)]
                        )
                        lin.style.linestyle.color = simplekml.Color.red
                        lin.style.linestyle.width = 2

            # Determinar el nombre del archivo
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"airspace_{timestamp}.kml"

            # Guardar el archivo
            kml.save(filename)
            return True, os.path.abspath(filename)

        except Exception as e:
            return False, str(e)

    def generate_path_kml(self, path, filename=None):
        """
        Genera un archivo KML con una ruta específica.

        Args:
            path: Objeto Path que contiene los nodos de la ruta
            filename (str): Nombre del archivo de salida (opcional)

        Returns:
            tuple: (success: bool, filename: str)
        """
        try:
            kml = simplekml.Kml()
            kml.document.name = f"Flight Path - {datetime.now().strftime('%Y-%m-%d')}"

            # Crear carpeta para la ruta
            path_folder = kml.newfolder(name="Flight Path")

            # Agregar puntos de la ruta
            for i, node in enumerate(path.nodes):
                point = self.airspace.find_nav_point_by_name(node.name)
                if point:
                    pnt = path_folder.newpoint(
                        name=f"{i + 1}. {point.name}",
                        coords=[(point.longitude, point.latitude)]
                    )
                    pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/pal2/icon48.png"

            # Agregar línea de la ruta
            coords = []
            for node in path.nodes:
                point = self.airspace.find_nav_point_by_name(node.name)
                if point:
                    coords.append((point.longitude, point.latitude))

            if len(coords) > 1:
                lin = path_folder.newlinestring(
                    name="Flight Path",
                    description=f"Total distance: {path.cost:.2f} km",
                    coords=coords
                )
                lin.style.linestyle.color = simplekml.Color.blue
                lin.style.linestyle.width = 4

            # Determinar el nombre del archivo
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"flight_path_{timestamp}.kml"

            # Guardar el archivo
            kml.save(filename)
            return True, os.path.abspath(filename)

        except Exception as e:
            return False, str(e)