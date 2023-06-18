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
    TRUNK = "trunk"
    TRUNK_LINK = "trunk_link"
