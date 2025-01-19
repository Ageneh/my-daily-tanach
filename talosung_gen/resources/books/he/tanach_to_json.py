import re
import json
import xml.etree.ElementTree as ET
from os import path, listdir, makedirs
from operator import itemgetter

tanach_xml_path = "./tanach_index.xml"


def run():
    tree = ET.parse(tanach_xml_path)
    root = tree.getroot()
    node_tanach=root.find("tanach")
    for node_books in node_tanach.findall("book"):
        node_book_names = node_books.find("names")
        node_book_fname = node_book_names.find("filename")
        node_book_abbrev = node_book_names.find("abbrev")
        # print(node_book_fname.text)

        print(node_book_abbrev.text)

        book_tree = ET.parse("./Books_xml/{}.xml".format(node_book_fname.text))
        node_header_title = book_tree.find("teiHeader").find("fileDesc").find("titleStmt")
        nodes_header_title = list(filter(lambda x: x.attrib.get("type") == "mainhebrew", node_header_title.findall("title")))[0]
        # print(node_book_fname.text, ",\t\t\t\t", nodes_header_title.text)
        # print(list(node_header_title.findall("title")))

if __name__ == '__main__':
    run()
