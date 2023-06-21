import app.DTOs.RoadChunk as RoadChunk
import app.DTOs.CoordinatesDTO as CoordinatesDTO
import app.DTOs.OsmRoadDTO as OsmRoadDTO
import app.ConfigLoaders.AppConfigLoader as APPConfigLoader
import app.enums.HighwayType as HighwayType
import app.OsmLoader as OsmLoader
from math import radians, sin, cos, sqrt, atan2, degrees, asin


class PathFinder:

    def __init__(self, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO) -> None:
        self.visited = [RoadChunk.RoadChunk]
        self.queue = [RoadChunk.RoadChunk]
        self.start_coord = start_coord
        self.dest_coord = dest_coord
        self.cl = APPConfigLoader.AppConfigLoader()

# Main method for PathFinder that manages all of the procedure
    def resolve(self) -> bool:
        self.ol = OsmLoader.OsmLoader()
        self.ol.start()
        completed = False

        self.start_coord = self.ol.correct_coordinate(self.start_coord)
        self.dest_coord = self.ol.correct_coordinate(self.dest_coord)

        completed = self.start_iter()

        while (not completed):
            completed = self.iter()

        # killing the OsmLoader
        self.ol.kill()

# Method to return the shortest path (used after the algorithm completed all iterations)
    def get_shortest_path(self) -> list[RoadChunk.RoadChunk]:
        # Find the list with the shortest path to the destination and transform the nested RoadChunks into a linear list going from the start coordinate to the destination coordinate
        final_chunk = [
            obj for obj in self.queue if self.dest_coord == obj.dest_coord][0]
        step = final_chunk
        step_list = [RoadChunk.RoadChunk]
        while (step != None):
            step_list.append(step)
            step = step.prev_chunk
        return reversed(step_list)

# First iteration of the algorithm
    def start_iter(self) -> bool:
        print("starting first iteration of algorithm")
        # find all of the roads that intersect the start node
        roads_on_startnode = self.ol.load_merged_from_latlong(
            self.start_coord.latitude, self.start_coord.longitude)
        for road in roads_on_startnode:
            maxspeed = self.compute_maxspeed(road, None)
            coord_list = road.way.coords
            coord_list_len = len(coord_list)
            for i in range(coord_list_len):
                # iterate over the coordinate of each road until you get to those that concide with the start coordinate
                long = coord_list[i][0]
                lat = coord_list[i][1]
                if (long == float(self.start_coord.longitude)) and (lat == float(self.start_coord.latitude)):
                    # if the road is not unidirectional add to the queue the roadchunks that go in either direction (if possible)
                    if (road.oneway == None or road.oneway == 'no'):
                        if (i > 0 and i < coord_list_len):
                            print(
                                "consider previous and next node too (check if they are destination)")
                            prev_coord = coord_list[i-1]
                            prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                prev_coord[1], prev_coord[0])
                            weight = self.compute_roadchunk_weight(
                                None, maxspeed, self.start_coord, prev_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, prev_coord_dto, weight, road))

                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                None, maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight, road))

                            # check if the destination has been reached
                            if ((prev_coord[1] == self.dest_coord.latitude and prev_coord[0] == self.dest_coord.longitude) or (next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True

                        elif (i > 0):
                            print(
                                "consider only previous node (check if it is destination)")
                            prev_coord = coord_list[i-1]
                            prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                prev_coord[1], prev_coord[0])
                            weight = self.compute_roadchunk_weight(
                                None, maxspeed, self.start_coord, prev_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, prev_coord_dto, weight, road))

                            # check if the destination has been reached
                            if (prev_coord[1] == self.dest_coord.latitude and prev_coord[0] == self.dest_coord.longitude):
                                return True

                        elif (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                None, maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight, road))

                            # check if the destination has been reached
                            if ((next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True

                        else:
                            print(
                                "impossible to calculate path")
                            raise ValueError("Invalid start coordinate input")
                    else:
                        # if the road is unidirectional add to the queue only the chunk of road that follows the direction of flow of the road
                        print("road is one way")
                        if (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                next_coord[1], next_coord[0])
                            weight = self.compute_roadchunk_weight(
                                None, maxspeed, self.start_coord, next_coord_dto)
                            self.queue.append(RoadChunk.RoadChunk(
                                None, maxspeed, self.start_coord, next_coord_dto, weight, road))

                            # check if the destination has been reached
                            if ((next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True

                        else:
                            print(
                                "impossible to calculate path")
                            raise ValueError("Invalid start coordinate input")
                    continue
        return False

# method that represents a single iteration of the algorithm (similar to the first iteration but with some key differences)
    def iter(self) -> bool:
        # extract the chunk with the minimum weight from the queue of nodes to be visited and remove it from the queue
        min_weight_chunk = min(
            self.queue, key=lambda obj: obj.get_full_weight)
        self.queue.pop(self.queue.index(min_weight_chunk))
        print("found min weight chunk for next iteration: ", min_weight_chunk)
        # extract all of the roads (different from the starting road chunk) that connect to the end of the minimum weight road chunk
        roads_after_min_weight_chunk = self.ol.load_merged_from_latlong(
            min_weight_chunk.dest_coord.latitude, min_weight_chunk.dest_coord.longitude)
        for road in roads_after_min_weight_chunk:
            # for each road extract max speed and list of coordinates
            road = OsmRoadDTO.OsmRoadDTO(road)
            maxspeed = self.compute_maxspeed(road, min_weight_chunk)
            coord_list = road.way.coords
            coord_list_len = len(coord_list)
            for i in range(coord_list_len):
                # iterate over the coordinate of each road until you get to those that concide with the start coordinate
                long = coord_list[i][0]
                lat = coord_list[i][1]
                if (long == float(min_weight_chunk.dest_coord.longitude)) and (lat == float(min_weight_chunk.dest_coord.latitude)):
                    if (road.oneway == None or road.oneway == 'no'):
                        # if the road is not unidirectional add to the queue the roadchunks that go in either direction (if possible)
                        if (i > 0 and i < coord_list_len):
                            print(
                                "consider previous and next node too (check if they are destination)")
                            prev_coord = coord_list[i-1]
                            if (prev_coord[1] != min_weight_chunk.start_coord.latitude and prev_coord[0] != min_weight_chunk.start_coord.longitude):
                                prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    prev_coord[1], prev_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto)
                                prev_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto, weight, road)
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
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight, road)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            # check if the destination has been reached
                            if ((prev_coord[1] == self.dest_coord.latitude and prev_coord[0] == self.dest_coord.longitude) or (next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True

                        elif (i > 0):
                            print(
                                "consider only previous node (check if it is destination)")
                            prev_coord = coord_list[i-1]
                            if (prev_coord[1] != min_weight_chunk.start_coord.latitude and prev_coord[0] != min_weight_chunk.start_coord.longitude):
                                prev_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    prev_coord[1], prev_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto)
                                prev_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, prev_coord_dto, weight, road)
                                if (not any(prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(prev_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if prev_chunk.start_coord == obj.start_coord and prev_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > prev_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = prev_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = prev_chunk.weigh

                            # check if the destination has been reached
                            if (prev_coord[1] == self.dest_coord.latitude and prev_coord[0] == self.dest_coord.longitude):
                                return True

                        elif (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            if (next_coord[1] != min_weight_chunk.start_coord.latitude and next_coord[0] != min_weight_chunk.start_coord.longitude):
                                next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    next_coord[1], next_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight, road)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            # check if the destination has been reached
                            if ((next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True
                    else:
                        # if the road is unidirectional add to the queue only the chunk of road that follows the direction of flow of the road
                        print("road is one way")
                        if (i < coord_list_len):
                            print(
                                "consider only next node (check if it is destination)")
                            next_coord = coord_list[i+1]
                            if (next_coord[1] != min_weight_chunk.start_coord.latitude and next_coord[0] != min_weight_chunk.start_coord.longitude):
                                next_coord_dto = CoordinatesDTO.CoordinatesDTO(
                                    next_coord[1], next_coord[0])
                                weight = self.compute_roadchunk_weight(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto)
                                next_chunk = RoadChunk.RoadChunk(
                                    min_weight_chunk, maxspeed, min_weight_chunk.dest_coord, next_coord_dto, weight, road)
                                if (not any(next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord for obj in self.visited)):
                                    self.queue.append(next_chunk)
                                else:
                                    already_visited_same_chunk = [
                                        obj for obj in self.visited if next_chunk.start_coord == obj.start_coord and next_chunk.dest_coord == obj.dest_coord][0]
                                    if (already_visited_same_chunk.get_full_weight() > next_chunk.get_full_weight()):
                                        already_visited_same_chunk.prev_chunk = next_chunk.prev_chunk
                                        already_visited_same_chunk.weigh = next_chunk.weigh

                            # check if the destination has been reached
                            if ((next_coord[1] == self.dest_coord.latitude and next_coord[0] == self.dest_coord.longitude)):
                                return True
                    continue
        return False

# compute the roadchunk weight (time to cross it) based on the maximum possible speed on it, and on the angle that it forms with the previous road chunk
    def compute_roadchunk_weight(self, prev_chunk: RoadChunk.RoadChunk, speed: str, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO):
        # speed is in km/h
        speed = float(speed)
        # convert the speed to m/s
        speed = speed/3.6
        # calculating the covered distance in meters
        dist = self.coord_distance(start_coord, dest_coord)
        # if we have no previous road chunk we compute the time to run the distance as a simple division between distance and maximum speed
        if (prev_chunk == None):
            return dist/speed
        else:
            # if we have a previous road chunk we take into account the angle between it and the current chunk
            angle = self.coord_angle_diff(prev_chunk, start_coord, dest_coord)
            # car acceleration in m/s^2 (taken from the application configuration parameters)
            acceleration = self.cl.get_param["0-60_acceleration"]

            # we are going to reduce the initial speed in the current road chunk more, the higher is the angle between the two
            # if the angle is lower than the 'no_speed_threshold' we consider the initial speed as a function of the angle
            no_speed_threshold = self.cl.get_param("no_speed_threshold")
            if (angle <= no_speed_threshold):
                print("positive initial speed")
                start_speed = speed / no_speed_threshold * \
                    (no_speed_threshold - angle)
                return self.time_to_cover(dist, start_speed, speed, acceleration)
            else:
                # otherwise the initial speed is zero
                print("no initial speed")
                start_speed = 0
                return self.time_to_cover(dist, start_speed, speed, acceleration)

# calculate the time to cover a distance based on initial speed, max speed and acceleration
    def time_to_cover(self, distance, initial_speed, max_speed, acceleration):
        time_to_max_speed = (max_speed-initial_speed)/acceleration
        acceleration_distance = initial_speed * time_to_max_speed + \
            1/2*acceleration*(time_to_max_speed**2)

        if distance <= acceleration_distance:
            return (2 * distance / acceleration) ** 0.5
        else:
            return time_to_max_speed + (distance - acceleration_distance)/max_speed

# get or compute the maximum possible speed for a given road
    def compute_maxspeed(self, road: OsmRoadDTO.OsmRoadDTO, prev_chunk: RoadChunk.RoadChunk) -> int:
        # check if the maxspeed is in the current road or in the previous chunk (if the previous chunk is on the same road)
        if ("maxspeed" in road.tags):
            return int(road.tags["maxspeed"])
        elif (prev_chunk != None):
            if (prev_chunk.road.name == road.name):
                return prev_chunk.speed_limit

        # check if any of the connected roads (of the same type) has the speed declared amongst the tags
        connected_roads = self.ol.load_connected_lines_of_same_type(
            road.osm_id)
        for r in connected_roads:
            if ("maxspeed" in r.tags):
                return r.tags["maxspeed"]

        # resolve the max speed depending on the road type, based on the 'highway' type and on the presence of houses close to it
        high_type = HighwayType.HighwayType.resolve(road.highway)
        if (high_type == HighwayType.HighwayType.MOTORWAY or high_type == HighwayType.HighwayType.MOTORWAY_LINK):
            return self.cl.get_param("motorway_maxspeed")
        elif (high_type == HighwayType.HighwayType.PRIMARY or high_type == HighwayType.HighwayType.PRIMARY_LINK or high_type == HighwayType.HighwayType.TRUNK or high_type == HighwayType.HighwayType.TRUNK_LINK):
            # check if the number of houses close to the given road is higher than the threshold to consider the road as urban
            is_urban = self.ol.count_houses_near_road(
                road.osm_id, self.cl.get_param("house_ditance_threshold")) >= self.cl.get_param("house_number_threshold_for_urban_road")
            if (is_urban):
                return self.cl.get_param("primary_urban_maxspeed")
            else:
                return self.cl.get_param("primary_extraurban_maxspeed")
        elif (high_type == HighwayType.HighwayType.SECONDARY or high_type == HighwayType.HighwayType.SECONDARY_LINK or high_type == HighwayType.HighwayType.TERTIARY or high_type == HighwayType.HighwayType.TERTIARY_LINK):
            # check if the number of houses close to the given road is higher than the threshold to consider the road as urban
            is_urban = self.ol.count_houses_near_road(
                road.osm_id, self.cl.get_param("house_ditance_threshold")) >= self.cl.get_param("house_number_threshold_for_urban_road")
            if (is_urban):
                return self.cl.get_param("secondary_urban_maxspeed")
            else:
                return self.cl.get_param("secondary_extraurban_maxspeed")
        elif (high_type == HighwayType.HighwayType.RESIDENTIAL or high_type == HighwayType.HighwayType.LIVING_STREET):
            return self.cl.get_param("pedestrian_priority_zone_maxspeed")

# calculate the distance in meters between two coordinates through the haversine formula
    def coord_distance(self, coord1: CoordinatesDTO.CoordinatesDTO, coord2: CoordinatesDTO.CoordinatesDTO):
        lat1, lon1, lat2, lon2 = map(
            radians, [coord1.latitude, coord1.longitude, coord2.latitude, coord2.longitude])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance = c * 6371 * 1000  # Earth radius in kilometers * 1000

        return distance

# calculate the angle between two lines formed by three coordinates: line1 = (coord1, coord2) and line2 = (coord2, coord3)
    def coord_angle_diff(self, coord1: CoordinatesDTO.CoordinatesDTO, coord2: CoordinatesDTO.CoordinatesDTO, coord3: CoordinatesDTO.CoordinatesDTO):
        # compute the angle of each couple of coordinates (South = 0, West = 90, North = 180, East = 270)
        chunk1_angle = degrees(atan2(float(coord2.latitude) - float(coord1.latitude),
                               float(coord2.longitude) - float(coord1.longitude))) + 180
        chunk2_angle = degrees(atan2(
            float(coord3.latitude) - float(coord2.latitude), float(coord3.longitude) - float(coord2.longitude))) + 180
        # return the absolute difference between the two coordinates
        return abs(chunk1_angle - chunk2_angle)


# TEST
if __name__ == "__main__":
    """ start_coord = CoordinatesDTO.CoordinatesDTO("45.136233", "10.028642")
    dest_coord = CoordinatesDTO.CoordinatesDTO("45.093592", "10.030017")
    prev_chunk = RoadChunk.RoadChunk(
        None, None, start_coord, dest_coord, None, None)
    start_coord1 = CoordinatesDTO.CoordinatesDTO("45.093592", "10.030017")
    dest_coord1 = CoordinatesDTO.CoordinatesDTO("45.092138", "10.114450")

    pf = PathFinder(start_coord, dest_coord1)
    print(pf.coord_angle_diff(prev_chunk, start_coord1, dest_coord1))"""
