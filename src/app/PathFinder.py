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
        completed = False

        self.start_coord = self.ol.correct_coordinate(self.start_coord)
        self.dest_coord = self.ol.correct_coordinate(self.dest_coord)

        completed = self.start_iter()

        while (not completed):
            completed = self.iter()

    def get_shortest_path(self) -> list[RoadChunk.RoadChunk]:
        final_chunk = [
            obj for obj in self.queue if self.dest_coord == obj.dest_coord][0]
        step = final_chunk
        step_list = [RoadChunk.RoadChunk]
        while (step != None):
            step_list.append(step)
            step = step.prev_chunk
        return reversed(step_list)

    def start_iter(self) -> bool:
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

                            if ((prev_coord[1] != self.dest_coord.latitude and prev_coord[0] != self.dest_coord.longitude) or (next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True

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

                            if (prev_coord[1] != self.dest_coord.latitude and prev_coord[0] != self.dest_coord.longitude):
                                return True

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

                            if ((next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True

                        else:
                            print(
                                "impossible to calculate path")
                            raise ValueError("Invalid start coordinate input")
                    else:
                        print("road is one way")
                        if (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight))

                            if ((next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True

                        else:
                            print(
                                "impossible to calculate path")
                            raise ValueError("Invalid start coordinate input")

    def iter(self) -> bool:
        min_weight_chunk = min(
            self.queue, key=lambda obj: obj.get_full_weight())
        self.queue.pop(min_weight_chunk)
        print("found min weight chunk for next iteration: ", min_weight_chunk)
        roads_after_min_weight_chunk = self.ol.load_merged_from_latlong(
            min_weight_chunk.dest_coord.latitude, min_weight_chunk.dest_coord.longitude)
        for road in roads_after_min_weight_chunk:
            road = OsmRoadDTO.OsmRoadDTO(road)
            maxspeed = self.compute_maxspeed(road, min_weight_chunk)
            coord_list = road.way.coords
            coord_list_len = len(coord_list)
            for i in range(coord_list_len):
                if (coord_list[i][0] == float(min_weight_chunk.dest_coord.longitude)) and (coord_list[i][1] == float(min_weight_chunk.dest_coord.latitude)):
                    if (road.oneway == None):
                        if (i > 0 and i < coord_list_len):
                            print(
                                "consider previous and next node too (check if they are destination)")
                            prev_coord = coord_list[i-1]
                            if (prev_coord[1] != min_weight_chunk.start_coord.latitude and prev_coord[0] != min_weight_chunk.start_coord.longitude):
                                prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    prev_coord[1], prev_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    maxspeed, min_weight_chunk.dest_coord, prev_coord_dto)
                                prev_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto, weight)
                                if (not any(prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(prev_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > prev_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = prev_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = prev_chunk.weigh

                            next_coord = coord_list[i+1]
                            if (next_coord[1] != min_weight_chunk.start_coord.latitude and next_coord[0] != min_weight_chunk.start_coord.longitude):
                                next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    next_coord[1], next_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            if ((prev_coord[1] != self.dest_coord.latitude and prev_coord[0] != self.dest_coord.longitude) or (next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True

                        elif (i > 0):
                            print(
                                "consider only previous node (check if it is destination)")
                            prev_coord = coord_list[i-1]
                            if (prev_coord[1] != min_weight_chunk.start_coord.latitude and prev_coord[0] != min_weight_chunk.start_coord.longitude):
                                prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    prev_coord[1], prev_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    maxspeed, min_weight_chunk.dest_coord, prev_coord_dto)
                                prev_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto, weight)
                                if (not any(prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(prev_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > prev_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = prev_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = prev_chunk.weigh

                            if (prev_coord[1] != self.dest_coord.latitude and prev_coord[0] != self.dest_coord.longitude):
                                return True

                        elif (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            if (next_coord[1] != min_weight_chunk.start_coord.latitude and next_coord[0] != min_weight_chunk.start_coord.longitude):
                                next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    next_coord[1], next_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            if ((next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True
                    else:
                        print("road is one way")
                        if (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            if (next_coord[1] != min_weight_chunk.start_coord.latitude and next_coord[0] != min_weight_chunk.start_coord.longitude):
                                next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    next_coord[1], next_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            if ((next_coord[1] != self.dest_coord.latitude and next_coord[0] != self.dest_coord.longitude)):
                                return True
        return False

    def compute_roadchunk_weight(self, prev_chunk: RoadChunk.RoadChunk, speed: str, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO):
        speed = float(speed)
        dist = self.coord_distance(start_coord, dest_coord)
        if (prev_chunk == None):
            return dist/speed
        else:
            angle = self.coord_angle_diff(prev_chunk, start_coord, dest_coord)
            # car acceleration in m/s^2
            acceleration = self.cl.get_param["0-60_acceleration"]
            if (angle <= self.cl.get_param("no_speed_threshold")):
                print("positive initial speed")
                start_speed = 0
                return self.time_to_cover(dist, start_speed, speed, acceleration)
            else:
                print("no initial speed")
                start_speed = 0
                return self.time_to_cover(dist, start_speed, speed, acceleration)

    def time_to_cover(self, distance, initial_speed, max_speed, acceleration):
        time_to_max_speed = (max_speed-initial_speed)/acceleration
        acceleration_distance = initial_speed * time_to_max_speed + \
            1/2*acceleration*(time_to_max_speed**2)

        if distance <= acceleration_distance:
            return (2 * distance / acceleration) ** 0.5
        else:
            return time_to_max_speed + (distance - acceleration_distance)/max_speed

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
