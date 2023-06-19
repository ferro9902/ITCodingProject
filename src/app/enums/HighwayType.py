from enum import Enum


class HighwayType(Enum):
    LIVING_STREET = "living_street"
    MOTORWAY = "motorway"
    MOTORWAY_LINK = "motorway_link"
    PRIMARY = "primary"
    PRIMARY_LINK = "primary_link"
    RESIDENTIAL = "residential"
    SECONDARY = "secondary"
    SECONDARY_LINK = "secondary_link"
    TERTIARY = "tertiary"
    TERTIARY_LINK = "tertiary_link"
    TRUNK = "trunk"
    TRUNK_LINK = "trunk_link"

    @classmethod
    def resolve(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"No member of {cls.__name__} has a value of {value}")
