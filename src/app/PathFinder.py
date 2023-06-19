import DTOs.RoadChunk as RoadChunk
import DTOs.CoordinatesDTO as CoordinatesDTO
import DTOs.OsmRoadDTO as OsmRoadDTO
import ConfigLoaders.AppConfigLoader as APPConfigLoader
import enums.HighwayType as HighwayType
import OsmLoader
from math import radians, sin, cos, sqrt, atan2, degrees


class PathFinder:

    def __init__(self, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO) -> None:
        self.visited = [RoadChunk.RoadChunk]
        self.queue = [RoadChunk.RoadChunk]
        self.start_coord = start_coord
        self.dest_coord = dest_coord
        self.cl = APPConfigLoader.AppConfigLoader()

    def resolve(self) -> bool:
        self.ol = OsmLoader.OsmLoader()
        self.ol.start()

        self.start_coord = self.ol.correct_coordinate(self.start_coord)
        self.dest_coord = self.ol.correct_coordinate(self.dest_coord)

        self.start_iter()
        # TODO

    def start_iter(self):
        print("starting first iteration of algorithm")
        roads_on_startnode = self.ol.load_merged_from_latlong(
            self.start_coord.latitude, self.start_coord.longitude)
        for road in roads_on_startnode:
            road = OsmRoadDTO.OsmRoadDTO(road)
            maxspeed = self.compute_maxspeed(road, None)
            coord_list = road.way.coords
            coord_list_len = len(coord_list)
            for i in range(coord_list_len):
                if (coord_list[i][0] == float(self.start_coord.longitude)) and (coord_list[i][1] - float(self.start_coord.latitude)):
                    if (road.oneway == None):
                        if (i > 0 and i < coord_list_len):
                            print(
                                "consider previous and next node too (check if they are destination)")
                            prev_coord = coord_list[i-1]
                            prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                prev_coord[1], prev_coord[0])
                            weight = self.compute_roadchunk_weight(
                                maxspeed, self.start_coord, prev_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, prev_coord_dto, weight))

                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight))
                        elif (i > 0):
                            print(
                                "consider only previous node (check if it is destination)")
                            prev_coord = coord_list[i-1]
                            prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                prev_coord[1], prev_coord[0])
                            weight = self.compute_roadchunk_weight(
                                maxspeed, self.start_coord, prev_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, prev_coord_dto, weight))
                        elif (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight))
                        else:
                            print(
                                "impossible to calculate path")
                            raise ValueError("Invalid start coordinate input")

    def compute_roadchunk_weight(self, prev_chunk: RoadChunk.RoadChunk, speed: str, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO):
        # TODO
        speed = float(speed)
        if (prev_chunk == None):
            dist = self.coord_distance(start_coord, dest_coord)
            return dist/speed
        else:
            angle = self.coord_angle_diff(prev_chunk, start_coord, dest_coord)
            if (angle <= self.cl.get_param("no_speed_threshold")):
                print("positive initial speed")
                # TODO calculate initial speed based on angle from maxspeed
            else:
                print("no initial speed")
                # TODO

    def compute_maxspeed(self, road: OsmRoadDTO.OsmRoadDTO, prev_chunk: RoadChunk.RoadChunk) -> int:
        if (road.tags["maxspeed"] != None):
            return int(road.tags["maxspeed"])
        elif (prev_chunk != None):
            if (prev_chunk.road.name == road.name):
                return prev_chunk.speed_limit

        connected_roads = self.ol.load_connected_lines_by_id(road.osm_id)
        maxspeed = [road.tags["maxspeed"] for road in connected_roads]
        if (len(maxspeed) > 0):
            return maxspeed[0]
        else:
            high_type = HighwayType.HighwayType.resolve(road.highway)
            if (high_type.__eq__(HighwayType.HighwayType.MOTORWAY) or high_type.__eq__(HighwayType.HighwayType.MOTORWAY_LINK)):
                return self.cl.get_param["motorway_maxspeed"]
            elif (high_type.__eq__(HighwayType.HighwayType.PRIMARY) or high_type.__eq__(HighwayType.HighwayType.PRIMARY_LINK) or high_type.__eq__(HighwayType.HighwayType.TRUNK) or high_type.__eq__(HighwayType.HighwayType.TRUNK_LINK)):
                is_urban = self.ol.count_houses_near_road(
                    road.osm_id, self.cl.get_param["house_ditance_threshold"]) >= self.cl.get_param["house_number_threshold_for_urban_road"]
                if (is_urban):
                    return self.cl.get_param["primary_urban_maxspeed"]
                else:
                    return self.cl.get_param["primary_extraurban_maxspeed"]
            elif (high_type.__eq__(HighwayType.HighwayType.SECONDARY) or high_type.__eq__(HighwayType.HighwayType.SECONDARY_LINK) or high_type.__eq__(HighwayType.HighwayType.TERTIARY) or high_type.__eq__(HighwayType.HighwayType.TERTIARY_LINK)):
                is_urban = self.ol.count_houses_near_road(
                    road.osm_id, self.cl.get_param["house_ditance_threshold"]) >= self.cl.get_param["house_number_threshold_for_urban_road"]
                if (is_urban):
                    return self.cl.get_param["secondary_urban_maxspeed"]
                else:
                    return self.cl.get_param["secondary_extraurban_maxspeed"]
            elif (high_type.__eq__(HighwayType.HighwayType.RESIDENTIAL) or high_type.__eq__(HighwayType.HighwayType.LIVING_STREET)):
                return self.cl.get_param["pedestrian_priority_zone_maxspeed"]

    def coord_distance(coord1: CoordinatesDTO.CoordinatesDTO, coord2: CoordinatesDTO.CoordinatesDTO):
        lat1, lon1, lat2, lon2 = map(
            radians, [coord1.latitude, coord1.longitude, coord2.latitude, coord2.longitude])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * sqrt(a)
        distance = 6371 * c  # Earth radius in kilometers

        return distance

    def coord_angle_diff(self, coord1: CoordinatesDTO.CoordinatesDTO, coord2: CoordinatesDTO.CoordinatesDTO, coord3: CoordinatesDTO.CoordinatesDTO):
        chunk1_angle = degrees(atan2(float(coord2.latitude) - float(coord1.latitude),
                               float(coord2.longitude) - float(coord1.longitude))) + 180
        chunk2_angle = degrees(atan2(
            float(coord3.latitude) - float(coord2.latitude), float(coord3.longitude) - float(coord2.longitude))) + 180
        return abs(chunk1_angle - chunk2_angle)


if __name__ == "__main__":
    """ start_coord = CoordinatesDTO.CoordinatesDTO("45.136233", "10.028642")
    dest_coord = CoordinatesDTO.CoordinatesDTO("45.093592", "10.030017")
    prev_chunk = RoadChunk.RoadChunk(
        None, None, start_coord, dest_coord, None, None)
    start_coord1 = CoordinatesDTO.CoordinatesDTO("45.093592", "10.030017")
    dest_coord1 = CoordinatesDTO.CoordinatesDTO("45.092138", "10.114450")

    pf = PathFinder(start_coord, dest_coord1)
    print(pf.coord_angle_diff(prev_chunk, start_coord1, dest_coord1))"""
