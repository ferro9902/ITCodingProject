# IT CODING PROJECT
## ASSIGNEMENT
Travel time estimation: Students will use map APIs such as Google Maps or OpenStreetMap to gather
information about roads and traffic. They will then use regression algorithms to estimate travel time
between two points based on variables such as distance, road type, and traffic conditions. Pro: allows for
working with APIs, geospatial data, and regression algorithms. Cons: may require a basic understanding of
map APIs and regression algorithms

## OBJECTIVE
My application will use OpenStreetMap to predict travel time based on:
1. distance
2. road type
3. traffic conditions
4. altitude variations
5. number of turns

## HOW I DID IT
### STEP 1
I starded by downloading the OpenStreetMap data for italy from geofabrik though the following link: https://download.geofabrik.de/europe/italy-latest.osm.pbf

### STEP 2
I then imported the data to a Postgres database i had already configured on my computer (called "OSMDB") through __osm2pgsql__.
this was archieved through the command:

    > osm2pgsql -d OSMDB -U postgres --password --hstore --latlong italy-latest.osm.pbf

where each of the tags identifies a specific parameter for the __osm2pgsql__ function: TODO

- "-d" : 
- ecc.

### STEP 3
It was then necessary to install a few python modules:

1)  __psycopg2__ 
2)  __tkinter__
3)  __shapely__

### STEP 4
At this point I was able to start to write the python code of the application

## Sources:
- https://wiki.openstreetmap.org/wiki/IT:Pagina%20Principale?uselang=it
- https://download.geofabrik.de/europe/italy.html
- https://osm2pgsql.org/