import app.DTOs.CoordinatesDTO as CoordinatesDTO
import app.DTOs.OsmRoadDTO as OsmRoadDTO


# Data Transfer Object for roadchunks

class RoadChunk:

    def __init__(self) -> None:
        self.prev_chunk = RoadChunk()
        self.speed_limit = None
        self.start_coord = CoordinatesDTO.CoordinatesDTO()
        self.dest_coord = CoordinatesDTO.CoordinatesDTO()
        self.weigh = None
        self.road = OsmRoadDTO.OsmRoadDTO()

    def __init__(self, prev_chunk: 'RoadChunk', speed_limit: int, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO, weigh: int, road: OsmRoadDTO.OsmRoadDTO) -> None:
        self.prev_chunk = prev_chunk
        self.speed_limit = speed_limit
        self.start_coord = start_coord
        self.dest_coord = dest_coord
        self.weigh = weigh
        self.road = road

    # iteratively compute the full weight for the given chunk with all of the previuos chunks
    def get_full_weight(self):
        if (self.prev_chunk != None):
            return self.weigh + self.prev_chunk.get_full_weight()
        else:
            return self.weigh

    def __str__(self):
        return f"RoadChunk going from [{self.start_coord}] to [{self.dest_coord}] at speed [{self.speed_limit}] in seconds [{round(self.weigh)}]"
