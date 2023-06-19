import DTOs.CoordinatesDTO as CoordinatesDTO
import DTOs.OsmRoadDTO as OsmRoadDTO


class RoadChunk:

    def __init__(self) -> None:
        self.prev_chunk = None
        self.speed_limit = None
        self.start_coord = None
        self.dest_coord = None
        self.weigh = None
        self.road = None

    def __init__(self, prev_chunk: 'RoadChunk', speed_limit: int, start_coord: CoordinatesDTO.CoordinatesDTO, dest_coord: CoordinatesDTO.CoordinatesDTO, weigh: int, road: OsmRoadDTO.OsmRoadDTO) -> None:
        self.prev_chunk = prev_chunk
        self.speed_limit = speed_limit
        self.start_coord = start_coord
        self.dest_coord = dest_coord
        self.weigh = weigh
        self.road = road
