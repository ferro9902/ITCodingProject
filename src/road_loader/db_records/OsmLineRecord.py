class OsmLineRecord:
    def __init__(self, osm_id, access, addr_housename, addr_housenumber, addr_interpolation,
                 admin_level, aerialway, aeroway, amenity, area, barrier, bicycle, brand,
                 bridge, boundary, building, construction, covered, culvert, cutting,
                 denomination, disused, embankment, foot, generator_source, harbour,
                 highway, historic, horse, intermittent, junction, landuse, layer,
                 leisure, lock, man_made, military, motorcar, name, natural, office,
                 oneway, operator, place, population, power, power_source, public_transport,
                 railway, ref, religion, route, service, shop, sport, surface, toll, tourism,
                 tower_type, tracktype, tunnel, water, waterway, wetland, width, wood,
                 z_order, way_area, tags, way):
        self.osm_id = osm_id
        self.access = access
        self.addr_housename = addr_housename
        self.addr_housenumber = addr_housenumber
        self.addr_interpolation = addr_interpolation
        self.admin_level = admin_level
        self.aerialway = aerialway
        self.aeroway = aeroway
        self.amenity = amenity
        self.area = area
        self.barrier = barrier
        self.bicycle = bicycle
        self.brand = brand
        self.bridge = bridge
        self.boundary = boundary
        self.building = building
        self.construction = construction
        self.covered = covered
        self.culvert = culvert
        self.cutting = cutting
        self.denomination = denomination
        self.disused = disused
        self.embankment = embankment
        self.foot = foot
        self.generator_source = generator_source
        self.harbour = harbour
        self.highway = highway
        self.historic = historic
        self.horse = horse
        self.intermittent = intermittent
        self.junction = junction
        self.landuse = landuse
        self.layer = layer
        self.leisure = leisure
        self.lock = lock
        self.man_made = man_made
        self.military = military
        self.motorcar = motorcar
        self.name = name
        self.natural = natural
        self.office = office
        self.oneway = oneway
        self.operator = operator
        self.place = place
        self.population = population
        self.power = power
        self.power_source = power_source
        self.public_transport = public_transport
        self.railway = railway
        self.ref = ref
        self.religion = religion
        self.route = route
        self.service = service
        self.shop = shop
        self.sport = sport
        self.surface = surface
        self.toll = toll
        self.tourism = tourism
        self.tower_type = tower_type
        self.tracktype = tracktype
        self.tunnel = tunnel
        self.water = water
        self.waterway = waterway
        self.wetland = wetland
        self.width = width
        self.wood = wood
        self.z_order = z_order
        self.way_area = way_area
        self.tags = tags
        self.way = way

    def record_to_osmline(self, record):
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
        self.tags = record[68]
        self.way = record[69]

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
