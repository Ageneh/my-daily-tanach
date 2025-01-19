import xml.etree.ElementTree as ET
from os import path
import pandas as pd
import dateutil.parser as dateparser

from talosung_gen.preconditions import get_res_path, get_out_path, YEAR

XML_SRC_XML = path.abspath(get_res_path("losungen/raw/Losungen Free {}.xml".format(YEAR, YEAR)))
OUT_NT_CSV = path.abspath(get_out_path("losungen_nt.csv"))
OUT_OT_CSV = path.abspath(get_out_path("losungen_ot.csv"))


# \u202c > richtung formatieren
# \u202b > richtung: RTL


def build_csv_row(i, cols):
    row = {}
    for c in cols:
        text = i.find(c).text
        if c == "Datum":
            text = "{}".format(dateparser.parse(text).date())
        row[c] = text
    return row


def write_csv(cols=None, out_file_name=OUT_OT_CSV):
    if cols is None: cols = []

    print("Running for columns: {}".format(cols))

    # Parsing the XML file
    xmlparse = ET.parse(XML_SRC_XML)
    root = xmlparse.getroot()
    rows = [build_csv_row(i, cols) for i in root]

    df = pd.DataFrame(rows, columns=cols)
    print("Output csv file to {}".format(out_file_name))
    df.to_csv(out_file_name, header=False, columns=cols, index=False)

    for col in cols:
        sub_out_file_name = out_file_name.replace(".csv", "_{}.csv".format(col.lower()))
        with open(sub_out_file_name, "w+") as output_csv:
            print("Output csv file to {}".format(sub_out_file_name))
            output_csv.writelines(list(map(lambda r: r[col] + "\n", rows)))
        # df.to_csv(out_file_name.replace(".csv", "_{}.csv".format(col.lower())), header=False, columns=[col], index=False, quoting=0)

    return rows


def run():
    cols = ["Datum", "Losungsvers", "Losungstext", "Lehrtextvers", "Lehrtext"]
    write_csv(cols[:3])
    write_csv([cols[0]] + cols[3:], OUT_NT_CSV)


if __name__ == '__main__':
    run()
