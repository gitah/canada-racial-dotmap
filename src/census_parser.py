""" Parse census data to get population information from it """

DBLOCK_UID_INDEX = 0
POP_INDEX = 1
CT_UID_INDEX = 38

def parse_census_file(file_path):
    """
    refer to data_references/census_dblock_92-151.pdf for schema

    returns map of dblock => (population, census track)
    """

    dblock_pop_map = {}

    with open(file_path) as fp:
        for line in fp:
            data = line.split()
            dblock_id = data[DBLOCK_UID_INDEX]
            dblock_pop = data[POP_INDEX]
            ct_id = data[CT_UID_INDEX]
            dblock_pop_map[dblock_id] = (dblock_pop, ct_id)

    return dblock_pop_map

## Main ##
if __name__ == "__main__":
    m = parse_census_file("data/2011_92-151_XBB_TXT.txt")
