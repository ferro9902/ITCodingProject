-- select point by id
SELECT * FROM planet_osm_point
WHERE 'addr:housenumber' = '1'
    AND 'addr:street' = 'via mantova'
    AND 'addr:city' = 'cremona';

   
-- select poligon by italian name
SELECT * FROM planet_osm_polygon
WHERE tags ? 'name:it'
    AND tags -> 'name:it' ILIKE 'cremona';
    
-- select all polygons intersecting chosen polygon
SELECT *
FROM planet_osm_polygon
WHERE ST_Intersects(way, (SELECT way FROM planet_osm_polygon WHERE osm_id = -44189))
  AND osm_id != -44189
ORDER BY ST_Area(planet_osm_polygon.way) DESC;