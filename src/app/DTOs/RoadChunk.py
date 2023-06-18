import CoordinatesDTO
import OsmRoadDTO


class RoadChunk:

    def __init__(self) -> None:
        self.prev_chunk = None
        self.speed_limit = None
        self.start_coord = None
        self.dest_Coord = None
        self.weigh = None
        self.road = None

    def __init__(self, prev_chunk: 'RoadChunk', speed_limit: int, start_coord: CoordinatesDTO, dest_Coord: CoordinatesDTO, weigh: int, road: OsmRoadDTO.OsmRoadDTO) -> None:
        self.prev_chunk = prev_chunk
        self.speed_limit = speed_limit
        self.start_coord = start_coord
        self.dest_Coord = dest_Coord
        self.weigh = weigh
        self.road = road
