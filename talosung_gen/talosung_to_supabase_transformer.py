import csv
import json
from os import path
import pandas as pd
import dateutil.parser as dateparser

from talosung_gen.preconditions import get_out_path, YEAR

TALOSUNG_JSON = path.abspath(get_out_path("losung-tanach-{}.json".format(YEAR)))
OUT_FILE_NAME = path.abspath(get_out_path("supa_losung-tanach-{}.csv".format(YEAR)))
SUPABASE_COLS = [
    "date",
    "book",
    "multiple",
    "multiple_parts",
    "text",
]
SUPABASE_COLS_PREFIX = [
    "",
    "",
    "",
    "",
    "",
]


def build_csv_row(obj):
    (date, value_dict) = obj
    row = {"date": "{}".format(dateparser.parse(date).date())}
    for i, c in enumerate(SUPABASE_COLS):
        if i == 0: continue
        col_val = json.dumps(value_dict[c], ensure_ascii=False)
        # if len(SUPABASE_COLS_PREFIX[i]) > 0:
        row[c] = "{}{}".format(SUPABASE_COLS_PREFIX[i], col_val)
        # print("))))", col_val)
    return row


def write_csv():
    print("Running for columns: {}".format(SUPABASE_COLS))

    data = None
    # Parsing the XML file
    with open(TALOSUNG_JSON, "r") as file:
        data = json.load(file)

    rows = [build_csv_row(entry) for entry in data.items()]

    df = pd.DataFrame(rows[:], columns=SUPABASE_COLS)
    print("Output csv file to {}".format(OUT_FILE_NAME))
    df.to_csv(OUT_FILE_NAME, header=True, index=False,
              # encoding="utf_8",
              quotechar='\"', sep=',',
              escapechar='\\',
              columns=SUPABASE_COLS, doublequote=True, quoting=csv.QUOTE_MINIMAL,
              )
    return rows


def run():
    write_csv()
    return


if __name__ == '__main__':
    run()
