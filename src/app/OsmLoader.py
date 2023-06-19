import DbConnector
import DTOs.OsmRoadDTO as OsmRoadDTO
import DTOs.CoordinatesDTO as CoordinatesDTO
from shapely.geometry import Point, MultiPoint
import math


class OsmLoader:
    def start(self):
        self.dbc = DbConnector.DbConnector()

    def load_merged_from_latlong(self, lat: float, long: float):
        roads_on_startnode = self.load_roads_from_latlong(
            lat, long)
        for r in self.load_lines_from_latlong(
                lat, long):
            obj = OsmRoadDTO.OsmRoadDTO.init_from_ref(r)
            if obj not in roads_on_startnode:
                roads_on_startnode.append(obj)

    def load_roads_from_latlong(self, lat: float, long: float):
        query = f"SELECT * FROM planet_osm_roads por WHERE ST_Intersects( por.way , ST_SetSRID(ST_MakePoint({long}, {lat}), 4326)) AND por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link');"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = OsmRoadDTO.OsmRoadDTO()
            road.record_to_osmroad(record)
            road_list.append(road)
        print("converted query result to road list of size: ",
              len(road_list))
        return road_list

    def load_roads_close_to_latlong(self, lat: float, long: float, max_road_num: int):
        query = f"SELECT * FROM planet_osm_roads por WHERE por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link') ORDER BY ST_Distance( por.way , ST_SetSRID(ST_MakePoint({long}, {lat}), 4326) ) ASC LIMIT {max_road_num};"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = OsmRoadDTO.OsmRoadDTO()
            road.record_to_osmroad(record)
            road_list.append(road)
        print("converted query result to road list of size: ",
              len(road_list))
        return road_list

    def load_roads_on_latlong(self, lat: float, long: float):
        query = f"SELECT COUNT(*) AS line_count FROM planet_osm_roads as por WHERE ST_Intersects(por.way, ST_Point({long}, {lat}, 4326)) AND por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link');"
        res = self.dbc.query_db(query)[0][0]
        print(
            f"found {res} roads crossing on given coordinates long [{long}] and lat [{lat}]")
        return res

    def load_lines_from_latlong(self, lat: float, long: float):
        query = f"SELECT * FROM planet_osm_line por WHERE ST_Intersects( por.way , ST_SetSRID(ST_MakePoint({long}, {lat}), 4326) ) AND por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link');"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = OsmRoadDTO.OsmRoadDTO()
            line.record_to_osmroad(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def load_lines_close_to_latlong(self, lat: float, long: float, max_line_num: int):
        query = f"SELECT * FROM planet_osm_line pol WHERE pol.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link') ORDER BY ST_Distance( pol.way , ST_SetSRID(ST_MakePoint({long}, {lat}), 4326) ) ASC LIMIT {max_line_num};"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = OsmRoadDTO.OsmRoadDTO()
            line.record_to_osmroad(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def count_lines_on_latlong(self, lat: float, long: float):
        query = f"SELECT COUNT(*) AS line_count FROM planet_osm_line as pol WHERE ST_Intersects(pol.way, ST_Point({long}, {lat}, 4326)) AND pol.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'trunk', 'trunk_link');"
        res = self.dbc.query_db(query)[0][0]
        print(
            f"found {res} lines crossing on given coordinates long [{long}] and lat [{lat}]")
        return res

    def load_roads_by_id(self, id: int):
        query = f"SELECT * FROM planet_osm_roads por WHERE por.osm_id = {id};"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = OsmRoadDTO.OsmRoadDTO()
            road.record_to_osmroad(record)
            road_list.append(road)
        print("converted query result to road list of size: ",
              len(road_list))
        return road_list

    def load_lines_by_id(self, id: int):
        query = f"SELECT * FROM planet_osm_line pol WHERE pol.osm_id = {id};"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = OsmRoadDTO.OsmRoadDTO()
            line.record_to_osmroad(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def load_connected_lines_by_id(self, id: int):
        query = f"SELECT pol2.* FROM planet_osm_line AS pol1 JOIN planet_osm_line AS pol2 ON ST_Intersects(pol1.way, pol2.way) WHERE pol1.osm_id = 815680410 AND pol1.highway = pol2.highway;"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = OsmRoadDTO.OsmRoadDTO()
            line.record_to_osmroad(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def correct_coordinate(self, coord: CoordinatesDTO.CoordinatesDTO) -> CoordinatesDTO.CoordinatesDTO:
        closest_road = self.load_lines_close_to_latlong(
            coord.latitude, coord.longitude, 1)
        coordinates = closest_road[0].way.coords
        min_distance = float('inf')
        for coordinate in coordinates:
            distance = math.sqrt(
                (coordinate[0] - float(coord.longitude)) ** 2 + (coordinate[1] - float(coord.latitude)) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_coord = coordinate
        return CoordinatesDTO.CoordinatesDTO(closest_coord[1], closest_coord[0])

    def count_houses_near_road(self, id: int, house_distance_threshold):
        query = f"select count(*) FROM planet_osm_polygon AS pop JOIN planet_osm_roads AS por ON ST_DWithin(ST_SetSRID(por.way, 4326), ST_SetSRID(pop.way, 4326), {house_distance_threshold}) WHERE por.osm_id = {id} and pop.building = 'yes'"
        res = self.dbc.query_db(query)[0][0]
        print(
            f"found [{res}] houses close to the given road with id [{id}]")
        return res

    def kill(self):
        self.dbc.disconnect()


if __name__ == "__main__":
    ol = OsmLoader()
    ol.start()
    rl = ol.load_roads_from_latlong(39.0746487, 8.4527658)
    for r in rl:
        print(r.__str__(), "\n")
    ol.count_lines_on_latlong(39.0746487, 8.4527658)
    # coord = CoordinatesDTO.CoordinatesDTO("45.1632988", "10.1587859")
    # ol.correct_coordinate(coord)
    # ol.kill()