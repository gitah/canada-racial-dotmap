"""
Reads a shapefile containing all the dissemination blocks (dblock)

For each dblock create a dot for each person in it at a random location
The dot will have the following info:
    a) Latitude, Longitude
    b) Color (representing the race)
    c) Quadkey (indicates which google maps tile we need)
"""
import shapefile

import nhi_parser
import census_parser

SHAPEFILE = "data/dblocks.shp"

DBUID_FIELD = 0
CTUID_FIELD = 24

def draw_dots(shape_file, nhi_file, census_file)
    ctrack_demo = parse_nhi_file(nhi_file)
    dblock_pop = parse_census_file(census_file)
    sf = shapefile.Reader(shape_file)
    shape_recs = sf.shapeRecords()

    for sr in shape_recs:
        rec = sr.record
        shape = sr.shape

        dblock_id = rec[DBUID_FIELD]
        ctrack_id = rec[CTUID_FIELD]

        demo = ctrack_demo[ctrack_id]
        dlbock_pop = dblock_pops[dblock_id]
        
        ratios = {
                "east_asian" : demo.ratio_east_asian,
                "black" : demo.ratio_black,
                "hispanic" : demo.ratio_hispanic,
                "south_asian" : demo.ratio_south_asian,
                "other" : demo.ratio_other,
                "aboriginal" : demo.ratio_aboriginal,
                "white" : demo.ratio_white,
        }
        draw_dblock_dots(shape, pop, ratios) 


def draw_dblock_dots(shape, pop, ratios):
    """
        1. 
    """
    DOT_COLORS = {
            "east_asian" : "red",
            "black" : "green",
            "hispanic" : "orange",
            "south_asian" : "brown",
            "other" : "purple",
            "aboriginal" : "gold",
            "white" : "blue"
    }
    dot_counts = {k:int(v*pop) for k,v in ratios}

    for demographic,count in dot_counts.item():
        for i in range(count):
            # 1) generate random (lat,lng) within bound of shape
                # 1.5) compute gmaps quadkey from (lat,lng)
            # 2) create dot (lat, lng, color, quadkey)
            # 3) write dot as row in sqllite
            pass
