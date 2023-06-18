import DTOs.RoadChunk
import DTOs.CoordinatesDTO
import DTOs.OsmRoadDTO
import OsmLoader
from math import radians, sin, cos, sqrt


class PathFinder:

    def __init__(self, start_coord: DTOs.CoordinatesDTO.CoordinatesDTO, dest_coord: DTOs.CoordinatesDTO.CoordinatesDTO) -> None:
        self.visited = [DTOs.RoadChunk.RoadChunk]
        self.queue = [DTOs.RoadChunk.RoadChunk]
        self.start_coord = start_coord
        self.dest_coord = dest_coord

    def resolve(self) -> bool:
        self.ol = OsmLoader.OsmLoader()
        self.ol.start()

        self.start_coord = self.ol.correct_coordinate(self.start_coord)
        self.dest_coord = self.ol.correct_coordinate(self.dest_coord)

        self.start_iter()

    def start_iter(self):
        print("starting first iteration of algorithm")
        roads_on_startnode = self.ol.load_merged_from_latlong(
            self.start_coord.latitude, self.start_coord.longitude)
        for road in roads_on_startnode:
            road = DTOs.OsmRoadDTO.OsmRoadDTO(road)
            coord_list = road.way.coords
            coord_list_len = len(coord_list)
            for i in range(coord_list_len):
                if (coord_list[i][0] == float(self.start_coord.longitude)) and (coord_list[i][1] - float(self.start_coord.latitude)):
                    if (road.oneway == None):
                        if (i > 0 and i < coord_list_len):
                            # TODO
                            print(
                                "consider previous and next node too (check if they aredestination)")
                            prev_coord = coord_list[i-1]
                            prev_coord_dto = DTOs.CoordinatesDTO.CoordinatesDTO(
                                prev_coord[1], prev_coord[0])
                            weight = self.compute_roadchunk_weight(
                                road.tag['maxspeed'], self.start_coord, prev_coord_dto)
                            self.queue.append(DTOs.RoadChunk.RoadChunk(
                                None, road.tag['maxspeed'], self.start_coord, prev_coord_dto, ))
                        elif (i > 0):
                            # TODO
                            print(
                                "consider only previous node (check if it is destination)")
                        elif (i < coord_list_len):
                            # TODO
                            print(
                                "consider only previous node (check if it is destination)")
                        else:
                            # TODO
                            print(
                                "throw exception as it is inpossible to calculate path")

    def compute_roadchunk_weight(self, prev_chunk: DTOs.RoadChunk.RoadChunk, speed: str, start_coord: DTOs.CoordinatesDTO.CoordinatesDTO, dest_coord: DTOs.CoordinatesDTO.CoordinatesDTO):
        # TODO
        speed = float(speed)
        if (speed != None):
            if (prev_chunk == None):
                dist = self.coord_distance(start_coord, dest_coord)
                return dist/speed

    def coord_distance(coord1: DTOs.CoordinatesDTO.CoordinatesDTO, coord2: DTOs.CoordinatesDTO.CoordinatesDTO):
        lat1, lon1, lat2, lon2 = map(
            radians, [coord1.latitude, coord1.longitude, coord2.latitude, coord2.longitude])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * sqrt(a)
        distance = 6371 * c  # Earth radius in kilometers

        return distance
