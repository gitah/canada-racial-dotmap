""" Parse NHI csv data and get demographic information from it """
import csv

class DemographicsInfo(object):
    def __init__(self):
        self.east_asian = 0
        self.black = 0
        self.hispanic = 0
        self.south_asian = 0
        self.other = 0
        self.aboriginal = 0
        self.white = 0

        self.total_population = 0

    @property
    def count_non_white(self):
        return self.east_asian \
               + self.black \
               + self.hispanic \
               + self.south_asian \
               + self.other \
               + self.aboriginal

    @property
    def count_all(self):
        return self.count_non_white + self.white

    @property
    def ratio_east_asian(self):
        return float(self.east_asian) / float(self.count_all)

    @property
    def ratio_black(self):
        return float(self.black) / float(self.count_all)

    @property
    def ratio_hispanic(self):
        return float(self.hispanic) / float(self.count_all)

    @property
    def ratio_south_asian(self):
        return float(self.south_asian) / float(self.count_all)

    @property
    def ratio_other(self):
        return float(self.other) / float(self.count_all)

    @property
    def ratio_aboriginal(self):
        return float(self.aboriginal) / float(self.count_all)

    @property
    def ratio_white(self):
        return float(self.white) / float(self.count_all)

    def __str__(self):
        retstr = [
            "East Asian: %s" % self.east_asian,
            "Black: %s" % self.black,
            "Hispanic: %s" % self.hispanic,
            "South Asian: %s" % self.south_asian,
            "Other: %s" % self.other,
            "Aboriginal: %s" % self.aboriginal,
            "White: %s" % self.white
        ]
        return "\n".join(retstr)

def parse_cencus_tract_info(rows):
    """ Pass in multiple rows for a census tract to create CensusTractInfo
    object
    
    Demographics the folowing are derived from 'Visible Minority' section
        East Asian (Chinese + South East Asian + Korea + Japanese + Fillipino)
        Hispanic (Latin American)
        Black
        South Asian
        Other (Arab + West Asian +  Visible minority, n.i.e. + Multiple visible minorities)

    Demographics for the following are from 'Ethnic origin population' section:
        Aboriginal

    Demographics for 'White' is derived from
        <Total Population> - <Visible Minority Pop.> - <Aboriginal Pop.>

    Row schema:
        0:  Geo_Code
        1:  Prov_Name
        2:  CMA_CA_Name
        3:  CT_Name
        4:  GNR
        5:  Topic                (ex. Visible Minority)
        6:  Characteristic       (ex. Total visible minority population)
        7:  Note
        8:  Total                (ex, 200)
        9:  Flag_Total
        10: Male
        11: Flag_Male
        12: Female
        13: Flag_Female
    """
    info = DemographicsInfo()
    for row in rows:
        topic = row[5].strip()
        charac = row[6].strip('"').strip()
        try:
            total = int(row[8].strip())
        except ValueError:
            # sometimes we can have floats in for the total
            # but we don't care about those rows
            continue

        if topic == "Visible minority population":
            if charac in {"Chinese", "Fillipino", "Korean", "Japanese", "Southeast Asian"}:
                info.east_asian += total
            elif charac == "South Asian":
                info.south_asian += total
            elif charac == "Black":
                info.black += total
            elif charac == "Latin American":
                info.hispanic += total
            elif charac in {"Arab", "West Asian", "Visible minority, n.i.e.","Multiple visible minorities" }:
                info.other += total
        elif topic == "Ethnic origin population":
            if charac == "Total population in private households by ethnic origins":
                info.total_population = total
            elif charac == "North American Aboriginal origins":
                info.aboriginal += total

    info.white = info.total_population - info.count_non_white
    return info

def parse_nhi_file(file_path):
    ct_map = {}

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file) 
        eof = False

        # skip first line which is column names
        csv_reader.next()

        r = csv_reader.next()
        curr_ct_id = r[0]
        curr_ct_rows = [r]
        while True:
            while True:
                try:
                    r = csv_reader.next()
                    if r[0] != curr_ct_id:
                        # reached end of data for current CT
                        break;
                    curr_ct_rows.append(r)
                except StopIteration:
                    # we have reached end of csv file
                    eof = True
                    break
            ct_info = parse_cencus_tract_info(curr_ct_rows)
            ct_map[curr_ct_id] = ct_info

            # update current census track for next iteration
            if not eof:
                curr_ct_id = r[0]
                curr_ct_rows = [r]
            else:
                break
    return ct_map

## Main ##
if __name__ == "__main__":
    CSV_FILE = "data/nhi-bc.csv"
    m = parse_nhi_file(CSV_FILE)
    import ipdb; ipdb.set_trace()
