from shapely.wkb import loads
import ast


class OsmRoadDTO:

    def __init__(self):
        self.osm_id = None
        self.access = None
        self.addr_housename = None
        self.addr_housenumber = None
        self.addr_interpolation = None
        self.admin_level = None
        self.aerialway = None
        self.aeroway = None
        self.amenity = None
        self.area = None
        self.barrier = None
        self.bicycle = None
        self.brand = None
        self.bridge = None
        self.boundary = None
        self.building = None
        self.construction = None
        self.covered = None
        self.culvert = None
        self.cutting = None
        self.denomination = None
        self.disused = None
        self.embankment = None
        self.foot = None
        self.generator_source = None
        self.harbour = None
        self.highway = None
        self.historic = None
        self.horse = None
        self.intermittent = None
        self.junction = None
        self.landuse = None
        self.layer = None
        self.leisure = None
        self.lock = None
        self.man_made = None
        self.military = None
        self.motorcar = None
        self.name = None
        self.natural = None
        self.office = None
        self.oneway = None
        self.operator = None
        self.place = None
        self.population = None
        self.power = None
        self.power_source = None
        self.public_transport = None
        self.railway = None
        self.ref = None
        self.religion = None
        self.route = None
        self.service = None
        self.shop = None
        self.sport = None
        self.surface = None
        self.toll = None
        self.tourism = None
        self.tower_type = None
        self.tracktype = None
        self.tunnel = None
        self.water = None
        self.waterway = None
        self.wetland = None
        self.width = None
        self.wood = None
        self.z_order = None
        self.way_area = None
        self.tags = None
        self.way = None

    def init_from_ref(self, ref_obj: 'OsmRoadDTO'):
        self.osm_id = ref_obj.osm_id
        self.access = ref_obj.access
        self.addr_housename = ref_obj.addr_housename
        self.addr_housenumber = ref_obj.addr_housenumber
        self.addr_interpolation = ref_obj.addr_interpolation
        self.admin_level = ref_obj.admin_level
        self.aerialway = ref_obj.aerialway
        self.aeroway = ref_obj.aeroway
        self.amenity = ref_obj.amenity
        self.area = ref_obj.area
        self.barrier = ref_obj.barrier
        self.bicycle = ref_obj.bicycle
        self.brand = ref_obj.brand
        self.bridge = ref_obj.bridge
        self.boundary = ref_obj.boundary
        self.building = ref_obj.building
        self.construction = ref_obj.construction
        self.covered = ref_obj.covered
        self.culvert = ref_obj.culvert
        self.cutting = ref_obj.cutting
        self.denomination = ref_obj.denomination
        self.disused = ref_obj.disused
        self.embankment = ref_obj.embankment
        self.foot = ref_obj.foot
        self.generator_source = ref_obj.generator_source
        self.harbour = ref_obj.harbour
        self.highway = ref_obj.highway
        self.historic = ref_obj.historic
        self.horse = ref_obj.horse
        self.intermittent = ref_obj.intermittent
        self.junction = ref_obj.junction
        self.landuse = ref_obj.landuse
        self.layer = ref_obj.layer
        self.leisure = ref_obj.leisure
        self.lock = ref_obj.lock
        self.man_made = ref_obj.man_made
        self.military = ref_obj.military
        self.motorcar = ref_obj.motorcar
        self.name = ref_obj.name
        self.natural = ref_obj.natural
        self.office = ref_obj.office
        self.oneway = ref_obj.oneway
        self.operator = ref_obj.operator
        self.place = ref_obj.place
        self.population = ref_obj.population
        self.power = ref_obj.power
        self.power_source = ref_obj.power_source
        self.public_transport = ref_obj.public_transport
        self.railway = ref_obj.railway
        self.ref = ref_obj.ref
        self.religion = ref_obj.religion
        self.route = ref_obj.route
        self.service = ref_obj.service
        self.shop = ref_obj.shop
        self.sport = ref_obj.sport
        self.surface = ref_obj.surface
        self.toll = ref_obj.toll
        self.tourism = ref_obj.tourism
        self.tower_type = ref_obj.tower_type
        self.tracktype = ref_obj.tracktype
        self.tunnel = ref_obj.tunnel
        self.water = ref_obj.water
        self.waterway = ref_obj.waterway
        self.wetland = ref_obj.wetland
        self.width = ref_obj.width
        self.wood = ref_obj.wood
        self.z_order = ref_obj.z_order
        self.way_area = ref_obj.way_area
        self.tags = ref_obj.tags
        self.way = ref_obj.way

    def record_to_osmroad(self, record: list[str]):
        self.osm_id = record[0]
        self.access = record[1]
        self.addr_housename = record[2]
        self.addr_housenumber = record[3]
        self.addr_interpolation = record[4]
        self.admin_level = record[5]
        self.aerialway = record[6]
        self.aeroway = record[7]
        self.amenity = record[8]
        self.area = record[9]
        self.barrier = record[10]
        self.bicycle = record[11]
        self.brand = record[12]
        self.bridge = record[13]
        self.boundary = record[14]
        self.building = record[15]
        self.construction = record[16]
        self.covered = record[17]
        self.culvert = record[18]
        self.cutting = record[19]
        self.denomination = record[20]
        self.disused = record[21]
        self.embankment = record[22]
        self.foot = record[23]
        self.generator_source = record[24]
        self.harbour = record[25]
        self.highway = record[26]
        self.historic = record[27]
        self.horse = record[28]
        self.intermittent = record[29]
        self.junction = record[30]
        self.landuse = record[31]
        self.layer = record[32]
        self.leisure = record[33]
        self.lock = record[34]
        self.man_made = record[35]
        self.military = record[36]
        self.motorcar = record[37]
        self.name = record[38]
        self.natural = record[39]
        self.office = record[40]
        self.oneway = record[41]
        self.operator = record[42]
        self.place = record[43]
        self.population = record[44]
        self.power = record[45]
        self.power_source = record[46]
        self.public_transport = record[47]
        self.railway = record[48]
        self.ref = record[49]
        self.religion = record[50]
        self.route = record[51]
        self.service = record[52]
        self.shop = record[53]
        self.sport = record[54]
        self.surface = record[55]
        self.toll = record[56]
        self.tourism = record[57]
        self.tower_type = record[58]
        self.tracktype = record[59]
        self.tunnel = record[60]
        self.water = record[61]
        self.waterway = record[62]
        self.wetland = record[63]
        self.width = record[64]
        self.wood = record[65]
        self.z_order = record[66]
        self.way_area = record[67]
        self.tags = ast.literal_eval("{" + record[68].replace("=>", ":") + "}")
        self.way = loads(bytes.fromhex(record[69]))

    def __str__(self):
        return f"QueryRow(osm_id={self.osm_id}, access={self.access}, addr_housename={self.addr_housename}, " \
               f"addr_housenumber={self.addr_housenumber}, addr_interpolation={self.addr_interpolation}, " \
               f"admin_level={self.admin_level}, aerialway={self.aerialway}, aeroway={self.aeroway}, " \
               f"amenity={self.amenity}, area={self.area}, barrier={self.barrier}, bicycle={self.bicycle}, " \
               f"brand={self.brand}, bridge={self.bridge}, boundary={self.boundary}, building={self.building}, " \
               f"construction={self.construction}, covered={self.covered}, culvert={self.culvert}, " \
               f"cutting={self.cutting}, denomination={self.denomination}, disused={self.disused}, " \
               f"embankment={self.embankment}, foot={self.foot}, generator_source={self.generator_source}, " \
               f"harbour={self.harbour}, highway={self.highway}, historic={self.historic}, horse={self.horse}, " \
               f"intermittent={self.intermittent}, junction={self.junction}, landuse={self.landuse}, " \
               f"layer={self.layer}, leisure={self.leisure}, lock={self.lock}, man_made={self.man_made}, " \
               f"military={self.military}, motorcar={self.motorcar}, name={self.name}, natural={self.natural}, " \
               f"office={self.office}, oneway={self.oneway}, operator={self.operator}, place={self.place}, " \
               f"population={self.population}, power={self.power}, power_source={self.power_source}, " \
               f"public_transport={self.public_transport}, railway={self.railway}, ref={self.ref}, " \
               f"religion={self.religion}, route={self.route}, service={self.service}, shop={self.shop}, " \
               f"sport={self.sport}, surface={self.surface}, toll={self.toll}, tourism={self.tourism}, " \
               f"tower_type={self.tower_type}, tracktype={self.tracktype}, tunnel={self.tunnel}, " \
               f"water={self.water}, waterway={self.waterway}, wetland={self.wetland}, width={self.width}, " \
               f"wood={self.wood}, z_order={self.z_order}, way_area={self.way_area}, tags={self.tags}, " \
               f"way={self.way})"

    def __eq__(self, other):
        if isinstance(other, OsmRoadDTO):
            return self.osm_id == other.osm_id
        return False
