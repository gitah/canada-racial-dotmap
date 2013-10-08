"""
Reads a shapefile containing all the dissemination blocks (dblock)

For each dblock create a dot for each person in it at a random location
The dot will have the following info:
    a) Latitude, Longitude
    b) Color (representing the race)
    c) Quadkey (indicates which google maps tile we need)
"""
import sqllite3

import shapefile

from nhs_parser import parse_nhs_file
from census_parser import parse_census_file
from shapefile_parser import parse_shapefile_file

SHAPEFILE = "data/dblocks.shp"

def generate_dots(shape_file, nhs_file, census_file, outfile)

    outfile_fp = open(outfile, 'w')

    ct_to_demo = parse_nhs_file(nhs_file)
    dblock_to_pop = parse_census_file(census_file)
    dblock_to_shape = parse_shapefile_file(shape_file)

    for dblock_id, shape in dblock_to_shape:
        pop, ctrack_id = dblock_to_pop[dblock_id]
        demo = ct_to_demo[ctrack_id]
        
        ratios = {
                "east_asian" : demo.ratio_east_asian,
                "black" : demo.ratio_black,
                "hispanic" : demo.ratio_hispanic,
                "south_asian" : demo.ratio_south_asian,
                "other" : demo.ratio_other,
                "aboriginal" : demo.ratio_aboriginal,
                "white" : demo.ratio_white,
        }

        dblock_dots = generate_dblock_dots(dblock_shape, dblock_pop, dblock_demo_ratios) 
        write_dots_to_db(dblock_dots, outfile_fp)

    outfile_fp.close()

def generate_dblock_dots(shape, pop, ratios):
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

    dots = []
    for demographic,count in dot_counts.item():
        for i in range(count):
            lat,lng = generate_random_point(shape)
            dot_color = DOT_COLORS[demographic]
            dots.append( (lat,lng,dot_color)
    return dots

def init_out_file(outfile):
    return 

def write_dots(dots, outfile_fp):
    dotstr = "%s %s %s" % (lat lng quadkey)
    outfile_fp.write(dotstr)
