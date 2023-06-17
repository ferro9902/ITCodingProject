class CoordinatesDTO:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude
