-- select roads intersecting given coordinates
SELECT *
FROM planet_osm_roads por
WHERE ST_Intersects(
  por.way ,
  ST_SetSRID(ST_MakePoint(8.4527658, 39.0746487), 4326)
);

-- select 10 roads closest to given coordinates
SELECT *
FROM planet_osm_roads por
ORDER BY ST_Distance(
  por.way ,
  ST_SetSRID(ST_MakePoint(8.4527658, 39.0746487), 4326)
) ASC
LIMIT 10;

-- select 10 roads closest to given coordinates filtered with highway
SELECT *
FROM planet_osm_roads por
WHERE por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'trunk', 'trunk_link')
ORDER BY ST_Distance(
  por.way ,
  ST_SetSRID(ST_MakePoint(8.4527658, 39.0746487), 4326)
) ASC
LIMIT 10 

SELECT pol2.*
FROM planet_osm_line AS pol1
JOIN planet_osm_line AS pol2 ON ST_Intersects(pol1.way, pol2.way)
WHERE pol1.osm_id = 815680410
  AND pol1.highway = pol2.highway ;
 
select *
FROM planet_osm_polygon AS pop
JOIN planet_osm_line AS pol ON ST_DWithin(ST_SetSRID(pol.way, 4326), ST_SetSRID(pop.way, 4326), 0.0002)
WHERE pol.osm_id = 107818039 and pop.building is not null and lower(pop.building) != 'no' 

EXPLAIN analyze SELECT *
FROM planet_osm_polygon AS pop
JOIN planet_osm_line AS pol ON ST_DWithin(ST_Simplify(ST_SetSRID(pol.way, 4326), 0.001), ST_Simplify(ST_SetSRID(pop.way, 4326), 0.001), 0.0002)
WHERE pol.osm_id = 107818039 AND pop.building IS NOT NULL AND LOWER(pop.building) != LOWER('no')

EXPLAIN analyze SELECT count(*)
FROM planet_osm_polygon AS pop
WHERE ST_DWithin(ST_SetSRID(pop.way, 4326), ST_SetSRID((
    SELECT pol.way
    FROM planet_osm_line AS pol
    WHERE pol.osm_id = 107818039
), 4326), 0.0003)
  AND pop.building IS NOT NULL
  AND LOWER(pop.building) != 'no'

CREATE INDEX idx_osm_polygon_way ON planet_osm_polygon USING GIST(way);
CREATE INDEX idx_osm_line_way ON planet_osm_line USING GIST(way);
CREATE INDEX idx_osm_line_osm_id ON planet_osm_line (osm_id);
CREATE INDEX idx_osm_polygon_building ON planet_osm_polygon (building);
  
DROP INDEX idx_osm_polygon_way;
DROP INDEX idx_osm_line_way;
DROP INDEX idx_osm_line_osm_id;
DROP INDEX idx_osm_polygon_building;


set max_parallel_workers = 16;
SET max_parallel_workers_per_gather = 8;
SET work_mem = '2000MB';
  

-- select highway lines intersecting given coordinates
SELECT *
FROM planet_osm_line pol 
WHERE pol.highway notnull AND ST_Intersects(
  pol.way ,
  ST_SetSRID(ST_MakePoint(8.4527658, 39.0746487), 4326)
);

-- select 10 highway lines closest to given coordinates
SELECT *
FROM planet_osm_line pol 
WHERE pol.highway NOTNULL 
ORDER BY ST_Distance(
  pol.way ,
  ST_SetSRID(ST_MakePoint(8.4527658, 39.0746487), 4326)
) ASC
LIMIT 10;



SELECT * FROM planet_osm_roads por WHERE ST_Intersects( por.way , ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326)) AND por.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'trunk', 'trunk_link');


SELECT * FROM planet_osm_line pol WHERE pol.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'trunk', 'trunk_link') ORDER BY ST_Distance( pol.way , ST_SetSRID(ST_MakePoint(10.1587859, 45.1632988), 4326) ) ASC LIMIT 1;


SELECT COUNT(*) AS line_count FROM planet_osm_line as pol WHERE ST_Intersects(pol.way, ST_Point(10.1587858, 45.1632988, 4326)) AND pol.highway IN ('living_street', 'motorway', 'motorway_link', 'primary', 'primary_link', 'residential', 'secondary', 'secondary_link', 'tertiary', 'trunk', 'trunk_link');