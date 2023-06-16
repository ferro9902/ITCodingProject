import DbConnector
import db_records.OsmRoadRecord
import db_records.OsmLineRecord


class OsmLoader:
    def start(self):
        self.dbc = DbConnector.DbConnector()

    def load_roads_from_latlong(self, lat: float, long: float):
        query = f"SELECT * FROM planet_osm_roads por WHERE ST_Intersects( por.way , ST_SetSRID(ST_MakePoint({lat}, {long}), 4326) );"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = db_records.OsmRoadRecord.OsmRoadRecord()
            road.record_to_osmroad(record)
            road_list.append(road)
        print("converted query result to road list of size: ",
              len(road_list))
        return road_list

    def load_roads_close_to_latlong(self, lat: float, long: float, max_road_num: int):
        query = f"SELECT * FROM planet_osm_roads por ORDER BY ST_Distance( por.way , ST_SetSRID(ST_MakePoint({lat}, {long}), 4326) ) ASC LIMIT {max_road_num};"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = db_records.OsmRoadRecord.OsmRoadRecord()
            road.record_to_osmroad(record)
            road_list.append(road)
        print("converted query result to road list of size: ",
              len(road_list))
        return road_list

    def load_lines_from_latlong(self, lat: float, long: float):
        query = f"SELECT * FROM planet_osm_line por WHERE ST_Intersects( por.way , ST_SetSRID(ST_MakePoint({lat}, {long}), 4326) );"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = db_records.OsmLineRecord.OsmLineRecord()
            line.record_to_osmline(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def load_lines_close_to_latlong(self, lat: float, long: float, max_line_num: int):
        query = f"SELECT * FROM planet_osm_line por ORDER BY ST_Distance( por.way , ST_SetSRID(ST_MakePoint({lat}, {long}), 4326) ) ASC LIMIT {max_line_num};"
        res = self.dbc.query_db(query)
        line_list = []
        for record in res:
            line = db_records.OsmLineRecord.OsmLineRecord()
            line.record_to_osmline(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def load_roads_by_id(self, id: int):
        query = f"SELECT * FROM planet_osm_roads por WHERE por.osm_id = {id};"
        res = self.dbc.query_db(query)
        road_list = []
        for record in res:
            road = db_records.OsmRoadRecord.OsmRoadRecord()
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
            line = db_records.OsmLineRecord.OsmLineRecord()
            line.record_to_osmline(record)
            line_list.append(line)
        print("converted query result to line list of size: ",
              len(line_list))
        return line_list

    def kill(self):
        self.dbc.disconnect


if __name__ == "__main__":
    ol = OsmLoader()
    ol.start()
    rl = ol.load_roads_from_latlong(10.1587858, 45.1632988)
    for r in rl:
        print(r.__str__(), "\n")
    ol.kill()
