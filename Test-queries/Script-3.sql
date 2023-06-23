-- select roads by id
SELECT *
FROM planet_osm_roads por
WHERE por.osm_id = 203270772;

-- select line by id
SELECT *
FROM planet_osm_line pol
WHERE pol.osm_id = 84814913;
 
SELECT distinct por."highway" from planet_osm_roads por