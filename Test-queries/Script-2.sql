-- select roads intersecting given coordinates
SELECT *
FROM planet_osm_roads por
WHERE ST_Intersects(
  por.way ,
  ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326)
);

-- select 10 roads closest to given coordinates
SELECT *
FROM planet_osm_roads por
ORDER BY ST_Distance(
  por.way ,
  ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326)
) ASC
LIMIT 10;

-- select highway lines intersecting given coordinates
SELECT *
FROM planet_osm_line pol 
WHERE pol.highway notnull AND ST_Intersects(
  pol.way ,
  ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326)
);

-- select 10 highway lines closest to given coordinates
SELECT *
FROM planet_osm_line pol 
WHERE pol.highway NOTNULL 
ORDER BY ST_Distance(
  pol.way ,
  ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326)
) ASC
LIMIT 10;


SELECT COUNT(*) AS line_count FROM planet_osm_line as pol WHERE ST_Intersects(pol.way, ST_SetSRID(ST_MakePoint(10.1587858, 45.1632988), 4326));