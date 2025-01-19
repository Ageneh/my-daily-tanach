import re
import json
import xml.etree.ElementTree as ET
from os import path, listdir, makedirs
from operator import itemgetter

septuaginta_xml_path = "septuaginta_lxx.xml"

aprocrypha = [
    "Jdt",
    "Wis",
    "Tob",
    "Sir",
    "Bar",
    "1Macc",
    "2Macc",
    "AddDan",
    "AddEsth",
    "PrMan",
    "3Macc",
    "4Macc",
    "EpJer",
    "1Esd",
    "2Esd"
]


def get_book_abbr_mapping():
    mappings = {}
    with open("../../mappings/abbr-json-mappings.csv") as mappings_file:
        for line in mappings_file.readlines():
            abbr, fname = line.replace("\n", "").split(";")
            mappings[abbr] = fname
    return mappings


def get_gr_to_json_mappings():
    abbr_book_mapping = get_book_abbr_mapping()
    mappings = {}
    with open("../../mappings/abbr-gr-to-standard.csv") as mappings_file:
        for line in mappings_file.readlines()[1:]:
            gr_abbr, std_abbr = line.replace("\n", "").split(";")
            mappings[gr_abbr] = abbr_book_mapping[std_abbr]
    return mappings


def run():
    tree = ET.parse(septuaginta_xml_path)
    root = tree.getroot()
    nodes_biblebook = root.findall("BIBLEBOOK")

    abbr_json_map = get_gr_to_json_mappings()
    print(abbr_json_map)
    for node_biblebook in nodes_biblebook[:]:
        book_num, book_name, book_abbr = itemgetter("bnumber", "bname", "bsname")(node_biblebook.attrib)
        if book_abbr in aprocrypha:
            continue

        out_filename = abbr_json_map[book_abbr]

        book_json_out = {}
        for node_book_chapter in node_biblebook.findall("CHAPTER"):
            chapter_num = itemgetter("cnumber")(node_book_chapter.attrib)
            chapter_verses = [node_chapter_verse.text for node_chapter_verse in node_book_chapter.findall("VERS")]
            book_json_out[chapter_num] = chapter_verses

        _final_json = {out_filename: book_json_out}
        export_json(out_filename, _final_json)


def export_json(filename, output):
    file_name = "../{}.json".format(filename)
    makedirs(path.dirname(file_name), exist_ok=True)
    print("Output json data to {}".format(filename))
    with open(file_name, "wb+") as outfile:
        json_object = json.dumps(output, indent=2, ensure_ascii=False).encode('utf8')
        outfile.write(json_object)


if __name__ == '__main__':
    run()
