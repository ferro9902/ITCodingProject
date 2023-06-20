class CoordinatesDTO:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other_obj) -> bool:
        if (isinstance(other_obj, CoordinatesDTO)):
            if (other_obj.latitude == self.latitude and other_obj.longitude == self.longitude):
                return True
        return False
