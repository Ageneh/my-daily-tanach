import re
import json
from os import path, listdir

from talosung_gen.preconditions import get_res_path

de_verses = "losungsverse_de.txt"
en_verses = "losungsverse_en.txt"
he_verses = "losungsverse_he.txt"
gr_verses = "losungsverse_gr.txt"


f = open(de_verses, "r")
verses = f.readlines()

book_name_pattern = "^(.*) (\d+,.*)"

book_abbr_dict = {
	"1. Chronik": "1CH",
	"1. Könige": "1KÖ",
	"1. Mose": "GEN",
	"1. Samuel": "1SA",
	"2. Chronik": "2CH",
	"2. Könige": "2KÖ",
	"2. Mose": "EXO",
	"2. Samuel": "2SA",
	"3. Mose": "LEV",
	"4. Mose": "NUM",
	"5. Mose": "DEU",
	"Daniel": "DAN",
	"Habakuk": "HAB",
	"Haggai": "HAG",
	"Hesekiel": "HES",
	"Hiob": "HIO",
	"Hosea": "HOS",
	"Jeremia": "JER",
	"Jesaja ": "JES ",
	"Joel": "JOE",
	"Jona": "JON",
	"Josua": "JOS",
	"Klagelieder": "KLA",
	"Maleachi": "MAL",
	"Micha": "MIC",
	"Nahum": "NAH",
	"Nehemia": "NEH",
	"Prediger": "PRE",
	"Psalm": "PSA",
	"Richter": "RIC",
	"Rut": "RUT",
	"Sacharja": "SAC",
	"Sprüche": "SPR",
	"Zefanja": "ZEF",
}

for verse in verses:
	verse_normalized = verse.strip()
	# print(verse_normalized, ">>", re.findall(book_name_pattern, verse))


books = listdir(get_res_path("books"))
for book in books:
	book_title = book.split(".")[0]
	book_data = book_title.split("_")

	book_abbr = ""
	if len(book_data) > 1:  # has number
		book_abbr = "{}{}".format(book_data[1], book_data[0])\
			.upper()[:3]

	print(book_abbr)

	#
