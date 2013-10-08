""" Parse dessimination block shapefile to get shape of each dblock  """

import shapefile

DBUID_FIELD = 0
CTUID_FIELD = 24
SHAPEFILE_SHAPE_shape = 5

def parse_shape_file(file_path):
    """
    parse the shapefile of all the dblocks
    returns map of dblock => shape
    """

    dblock_to_shape = {}

    import ipdb; ipdb.set_trace()
    sf = shapefile.Reader(file_path)

    shape_recs = sf.shapeRecords()

    for sr in shape_recs:
        rec = sr.record
        shape = sr.shape

        dblock_id = rec[DBUID_FIELD]
        ctrack_id = rec[CTUID_FIELD]

        if shape.parts == SHAPEFILE_SHAPE_shape:
            dblock_to_shape[dblock_id] = shape

    return dblock_to_shape

## Main ##
if __name__ == "__main__":
    m = parse_shape_file("data/dblocks.shp")
