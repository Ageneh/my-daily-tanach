import re
import json
import xml.etree.ElementTree as ET
from os import path, listdir

YEAR = 2025

# \u202c > richtung formatieren
# \u202b > richtung: RTL

books_jsons = {}  # lang: book: ...

_DE = "de"
_EN = "en"
_HE = "he"
LANGS = [_DE, _EN, _HE]


def getVerseFromBookJson(book, lang):
	book_json = None
	if lang not in books_jsons.keys():
		books_jsons[lang] = {}

	lang_book = books_jsons[lang]

	if book in lang_book.keys():
		book_json = lang_book.get(book)
	else:
		book_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/books/{}/{}.json".format(lang, book)
		book_lines = "".join(open(book_dir, "r").readlines())
		book_json = json.loads(book_lines)
		books_jsons[lang][book] = book_json
	return book_json


BASE_DIR = "/Users/harega/WebstormProjects/tanach_backend/data/v2"


def run():
	days_list_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/{}/losungstage.txt".format(YEAR)
	texts_german_list_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/{}/losungstexte_de.txt".format(YEAR)
	translation_map_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/german-to-english-books.json"
	hebrew_translation_map_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/english-to-hebrew-books.json"
	english_translation_map_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/english-to-english-books.json"
	verses_dir = "/Users/harega/WebstormProjects/tanach_backend/data/v2/{}/losungsverse_de.txt".format(YEAR)

	translation_map = open(translation_map_dir, "r")
	translations_map_str = "".join(translation_map.readlines())
	translation_map_dict = json.loads(translations_map_str)

	hebrew_translation_map = open(hebrew_translation_map_dir, "r")
	hebrew_translation_map_str = "".join(hebrew_translation_map.readlines())
	hebrew_translation_map_dict = json.loads(hebrew_translation_map_str)

	english_translation_map = open(english_translation_map_dir, "r")
	english_translation_map_str = "".join(english_translation_map.readlines())
	english_translation_map_dict = json.loads(english_translation_map_str)

	book_name_pattern = "^(.*) (\\d+,.*)"

	verses_list = open(verses_dir, "r").readlines()

	texts_german = open(texts_german_list_dir, "r").readlines()
	days_list = open(days_list_dir, "r").readlines()

	losung_merge_output = {}

	verses_per_date = {}

	for index, verse in enumerate(verses_list[:]):
		book, verse_num = re.findall(book_name_pattern, verse)[0]
		book_en = translation_map_dict[book]

		day_date = days_list[index].strip()

		verses_per_lang = {
			_EN: [],
			_DE: [],
			_HE: [],
		}
		verses_per_lang_ARRAY = []

		chapter, verse_numbers = verse_num.split(",")

		for lang in LANGS:
			book_json = getVerseFromBookJson(book_en, lang)[book_en]

			verse_parts = verse_numbers.split(".")  # 2.4
			isMultiPart = len(verse_parts) > 1
			isMultiverse = False
			for p in verse_parts:
				# print(">>>>>>>", p)
				verse_start_end = p.split("-") if "-" in p else [int(p), int(p)]
				verse_start, verse_end = verse_start_end
				isMultiverse = isMultiPart or (len(verse_start_end) > 1 and (verse_start is not verse_end))
				if isMultiverse:  # has start and end; x-y
					verse_start, verse_end = map(lambda x: int(x), verse_start_end)
				try:
					verses_per_lang[lang] += book_json[chapter][verse_start - 1:verse_end]
					verses_per_lang_ARRAY.append(book_json[chapter][verse_start - 1:verse_end])
				except Exception as e:
					print(day_date, "/", book, ":: ", chapter, "--", verse_start, "--", verse_end)

					if book == "Joel":
						chapter_joel, verse_joel, verse_end_joel = joelException(chapter, verse_start, verse_end)
						verses_per_lang[lang] += book_json[chapter_joel][verse_joel - 1:verse_end_joel]
						verses_per_lang_ARRAY.append(book_json[chapter_joel][verse_joel - 1:verse_end_joel])

# 				if days_list[index].strip() == "2022-12-28":
# 					print(">>>>>>>", verses_per_lang[lang])

# 		if days_list[index].strip() == "2022-12-28":
# 			print("/////////", chapter, verses_per_lang_ARRAY)

		VERSES_DE = verses_per_lang[_DE]
		VERSES_EN = verses_per_lang[_EN]
		VERSES_HE = verses_per_lang[_HE]

		# print(book_en, ",",chapter, "//", verse_start, "--", verse_end, ">>", book_json[chapter][verse_start - 1:verse_end])

		DATA = {
			"book": {
				"book_de": book,
				"book": book_en,
				"book_en": english_translation_map_dict[book_en],
				"book_he": hebrew_translation_map_dict[book_en],
				"chapter": chapter,
				# "verses": "{}-{}".format(verse_start, verse_end) if isMultiverse else str(verse_start),
				"verses": verse_numbers,
			},
			"multiple": isMultiverse,
			"multiple_parts": isMultiPart,
			"text": {
				"hebrew": VERSES_HE,
				"german": texts_german[index].strip(),
				"german_sch2000": VERSES_DE,
				"english": VERSES_EN,
			}
		}
		losung_merge_output[day_date] = DATA
# 		print(day_date, ": -> ", DATA)

	return losung_merge_output


def getAllHebrewNames():
	names_list = {}
	for xmlFile in listdir("/Users/harega/WebstormProjects/tanach_backend/data/tanach/xml"):
		book_name = xmlFile.split(".")[0]
		tree = ET.parse("/Users/harega/WebstormProjects/tanach_backend/data/tanach/xml/{}".format(xmlFile))
		root = tree.getroot()

		tanach = root.find("tanach")
		book = tanach.find("book")
		if not book: continue
		names = book.find("names")
		hebrewname = names.find("hebrewname")

		print(
			hebrewname.text
		)
		names_list[book_name] = hebrewname.text

	return names_list


def joelException(chapter, verse_start, verse_end = None):
	ch3start = 5
	if verse_end is None:
		verse_end = verse_start
	if int(chapter) == 4:
		return ["3", ch3start + verse_start, ch3start + verse_end]
	return [chapter, verse_start, verse_end]

def writeToFile(output, fileName=None):
	json_object = json.dumps(output, indent=2, ensure_ascii=False).encode('utf8')
	if not fileName:
		file_name = "/losung-tanach-{}_v2.json".format(YEAR)
		with open("{}{}".format(BASE_DIR, file_name), "wb") as outfile:
			outfile.write(json_object)
	else:
		with open(fileName, "wb") as outfile:
			outfile.write(json_object)


def writeToFile1(output, fileName=None):
	json_object = json.dumps(output, indent=2, ensure_ascii=False).encode('utf8')
	if not fileName:
		file_name = "/AAA__VERSES__losung-tanach-{}_v2.json".format(YEAR)
		with open("{}{}".format(BASE_DIR, file_name), "wb") as outfile:
			outfile.write(json_object)
	else:
		with open(fileName, "wb") as outfile:
			outfile.write(json_object)


if __name__ == '__main__':
	years = range(2025, 2026)
	output = run()
	writeToFile(output)

# # YEAR = 2023
# # writeToFile(run())
#
# writeToFile(getAllHebrewNames(), fileName="{}/english-to-hebrew-books.json".format(BASE_DIR))
