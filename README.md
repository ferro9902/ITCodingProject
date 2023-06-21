# __WORK IN PROGRESS__ (to complete tests)

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
3. number and entity of the turns

## INITIAL STEPS
### STEP 1
I starded by downloading the OpenStreetMap data for italy from geofabrik though the following link: https://download.geofabrik.de/europe/italy-latest.osm.pbf

### STEP 2
I then imported the data to a Postgres database i had already configured on my computer (called "OSMDB") through __osm2pgsql__.
It was only necessary to activate a few extension on the DB (__plpgsql__, __postgis__ and __hstore__) before running the command:

    > osm2pgsql -d OSMDB -U postgres --password --hstore --latlong italy-latest.osm.pbf

where each of the tags identifies a specific parameter for the __osm2pgsql__ function: TODO

- "-d" : to select a DB different from the default __postgres__ (in this case __OSMDB__)
- "-U" : to specify the username through which we are going to access the DB
- "--password" : to allow us to specify the password of the given username
- "--hstore" : to add additional tags without a column to an additional hstore column
- "--latlong" : to store data in a latitude and longitude fomat, rather than using the EPSG:3857 format (which corresponds to the Web Mercator projection or WGS84 datum that is what GPSs use)

### STEP 3
It was then necessary to install a few python modules:

1)  __psycopg2__ : to allow the connection to a DB
2)  __tkinter__ :  to create simple user interactive interfaces
3)  __shapely__ :  to manage complex geometries

## APPLICATION STRUCTURE
At this point I was able to start to write the python code of the application.

### Application Structure:
The application can be executed from a main class that handles all of the high level logic behind the application. It then interacts, directly or indirectly, to a few classes that take care of implementing all of the logic behind the application:

- "CoordinatesImputForm.py" : which is responsible for the creation of the user interface inwhich the application parameters are to be inserted
- "DbConnector.py" : which is responsible for the connection and querying of the database
- "OsmLoader.py" : in which all of the different types of query are implemented and in which data is parsed after each query is completed
- "PathFinter.py" : most important class of the whole application, in this class are implemented all of the methods responsible for the path fining algorithm


## Sources:
- https://wiki.openstreetmap.org/wiki/IT:Pagina%20Principale?uselang=it
- https://download.geofabrik.de/europe/italy.html
- https://osm2pgsql.org/