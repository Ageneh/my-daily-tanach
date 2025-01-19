import re
import json
import xml.etree.ElementTree as ET
from os import path, listdir, makedirs

from talosung_gen.preconditions import get_res_path, get_out_path, LANGS, _EN, _DE, _HE, BOOK_NAME_PATTERN, \
    YEAR, _GR

# \u202c > richtung formatieren
# \u202b > richtung: RTL

books_jsons = {}  # lang: book: ...
LOSUNG_TXT_FILES = [
    "losungen_ot_datum.csv",
    "losungen_ot_losungstext.csv",
    "losungen_ot_losungsvers.csv",
]

####### paths and vars
ge_to_en_json = get_res_path("german-to-english-books.json")
en_to_he_json = get_res_path("english-to-hebrew-books.json")
en_map_json = get_res_path("english-to-english-books.json")

days_list_dir = ""
texts_german_list_dir = ""
verses_dir = ""

RAW_RES_DIR = path.abspath(get_out_path())

def get_en_lang_title_mappings():
    mappings = {}
    with open(get_res_path("books/mappings/english-fname-translations.csv")) as mappings_file:
        for row in mappings_file.readlines()[1:]:
            fname, abbr, ge, he, en, gr = row.replace("\n", "").split(";")
            mappings[fname] = {
                "filename": fname,
                "file": "{}.json".format(fname),
                "abbreviation": abbr,
                _HE: he,
                _GR: gr,
                _EN: en,
                _DE: ge,
            }
            print(fname, abbr, [ge, he, en, gr])
    return mappings

def get_verse_from_book_json(book, lang):
    book_json = None
    if lang not in books_jsons.keys():
        books_jsons[lang] = {}

    lang_book = books_jsons[lang]

    if book in lang_book.keys():
        book_json = lang_book.get(book)
    else:
        book_dir = get_res_path("books/{}/{}.json".format(lang, book))
        book_lines = "".join(open(book_dir, "r").readlines())
        book_json = json.loads(book_lines)
        books_jsons[lang][book] = book_json
    return book_json


def define_input_file_paths():
    global days_list_dir, texts_german_list_dir, verses_dir
    [days_list_dir, texts_german_list_dir, verses_dir] = map(
        lambda fname: "{}/{}".format(RAW_RES_DIR, fname),
        LOSUNG_TXT_FILES
    )


def get_translation_dict(translation_dir):
    translation_map = open(translation_dir, "r")
    translation_map_stringified = "".join(translation_map.readlines())
    return json.loads(translation_map_stringified)


def get_all_hebrew_names():
    names_list = {}
    tanach_xml_path = get_res_path("tanach/xml")
    for xmlFile in listdir(tanach_xml_path):
        book_name = xmlFile.split(".")[0]
        tree = ET.parse("{}/{}".format(tanach_xml_path, xmlFile))
        root = tree.getroot()

        tanach = root.find("tanach")
        book = tanach.find("book")
        if not book: continue
        names = book.find("names")
        hebrewname = names.find("hebrewname")

        # print(hebrewname.text)
        names_list[book_name] = hebrewname.text

    return names_list


def joel_exception(chapter, verse_start, verse_end=None):
    ch3start = 5
    if verse_end is None:
        verse_end = verse_start
    if int(chapter) == 4:
        return ["3", ch3start + verse_start, ch3start + verse_end]
    return [chapter, verse_start, verse_end]


def write_to_file(output):
    json_object = json.dumps(output, indent=2, ensure_ascii=False).encode('utf8')
    file_name = "losung-tanach-{}.json".format(YEAR)
    out_file_path = get_out_path("{}".format(file_name))
    makedirs(path.dirname(out_file_path), exist_ok=True)
    print("Output tanach.json file to {}".format(out_file_path))
    with open(out_file_path, "wb+") as outfile:
        outfile.write(json_object)


def merge():
    define_input_file_paths()

    losung_merge_output = {}

    # translation dictionaries
    en_to_lang_mappings = get_en_lang_title_mappings()
    translation_map_dict = get_translation_dict(ge_to_en_json)
    hebrew_translation_map_dict = get_translation_dict(en_to_he_json)
    english_translation_map_dict = get_translation_dict(en_map_json)

    with open(verses_dir, "r") as verses_list:
        print("Opened file: {}".format(verses_dir))
        with open(texts_german_list_dir, "r") as _texts_german, open(days_list_dir, "r") as _days:
            print("Opened file: {}".format(texts_german_list_dir))
            print("Opened file: {}".format(days_list_dir))

            days_list = _days.readlines()
            texts_german = _texts_german.readlines()

            for index, verse in enumerate(verses_list.readlines()[:]):
                book_name_german, verse_num = re.findall(BOOK_NAME_PATTERN, verse)[0]
                # print(">>>>>>>", book_name_german)
                book_en = translation_map_dict[book_name_german]
                day_date = days_list[index].strip()
                verses_per_lang = {_EN: [], _DE: [], _HE: [], _GR: []}
                verses_per_lang_array = []
                chapter, verse_numbers = verse_num.split(",")

                for lang in LANGS:
                    book_json = get_verse_from_book_json(book_en, lang)[book_en]

                    verse_parts = verse_numbers.split(".")  # 2.4
                    is_multi_part = len(verse_parts) > 1
                    is_multiverse = False
                    for p in verse_parts:
                        verse_start_end = p.split("-") if "-" in p else [int(p), int(p)]
                        verse_start, verse_end = verse_start_end
                        is_multiverse = is_multi_part or (len(verse_start_end) > 1 and (verse_start is not verse_end))
                        if is_multiverse:  # has start and end; x-y
                            verse_start, verse_end = map(lambda x: int(x), verse_start_end)
                        try:
                            verses_per_lang[lang] += book_json[chapter][verse_start - 1:verse_end]
                            verses_per_lang_array.append(book_json[chapter][verse_start - 1:verse_end])
                        except Exception as e:
                            # print(day_date, "/", book, ":: ", chapter, "--", verse_start, "--", verse_end)

                            if book_name_german.lower() == "joel":
                                chapter_joel, verse_joel, verse_end_joel = joel_exception(chapter, verse_start,
                                                                                          verse_end)
                                verses_per_lang[lang] += book_json[chapter_joel][verse_joel - 1:verse_end_joel]
                                verses_per_lang_array.append(book_json[chapter_joel][verse_joel - 1:verse_end_joel])

                # print(book_en, ",", chapter, "//", verse_start, "--", verse_end, ">>", book_json[chapter][verse_start - 1:verse_end])

                losung_merge_output[day_date] = {
                    "book": {
                        "book_de": book_name_german,
                        "book": book_en,
                        "book_en": english_translation_map_dict[book_en],
                        "book_he": hebrew_translation_map_dict[book_en],
                        "book_gr": en_to_lang_mappings[book_en][_GR],
                        "chapter": chapter,
                        # "verses": "{}-{}".format(verse_start, verse_end) if is_multiverse else str(verse_start),
                        "verses": verse_numbers,
                    },
                    "multiple": is_multiverse,
                    "multiple_parts": is_multi_part,
                    "text": {
                        "hebrew": verses_per_lang[_HE],
                        "german": texts_german[index].strip(),
                        "german_sch2000": verses_per_lang[_DE],
                        "english": verses_per_lang[_EN],
                        "greek": verses_per_lang[_GR],
                    }
                }
                # print(day_date, ": -> ", losung_merge_output[day_date])

    return losung_merge_output


def run():
    output = merge()
    write_to_file(output)


if __name__ == '__main__':
    run()
