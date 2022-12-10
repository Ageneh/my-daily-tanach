const express = require("express");
const router = express.Router();

const fs = require("fs");
const parser = require("xml2json");

const LOSUNGSTAGE = "losungstage.txt";
const LOSUNGSTEXTE_DE = "losungstexte_de.txt";
const LOSUNGSVERSE_DE = "losungsverse_de.txt";

const parseLosungenTanachJson = (year) => {
	// e.g.: losung-tanach-2022.json
	const content = fs.readFileSync(`./data/v2/losung-tanach-${year}.json`);
	const json = JSON.parse(content);
	console.log("to json ->", json);
	return json;
}

const parseLosungen2022 = () => {
	const content = fs.readFileSync("./data/tanach/txt/Losungen Free 2022.xml");

	const json = parser.toJson(content, {});
	console.log("to json ->", json);

	return json;
}

const readLosungen2022 = () => {
	const content = fs.readFileSync("./data/Losungen2022.json");
	return JSON.parse(content);
}

const readBookNamesGermanToEnglish = () => {
	const content = fs.readFileSync("./data/BookNameMap.json");
	return JSON.parse(content);
}
const BOOKS_GER_ENG = readBookNamesGermanToEnglish();

const normalizeISODateString = (dateString = undefined) => {
	if (!dateString || dateString.length < 1) {
		dateString = new Date().toISOString();
	}
	return `${dateString.split("T")[0]}T00:00:00`;
}

const today = new Date();
const todayDateString = {
	"ISO_NORMALIZED": normalizeISODateString(),
	"SHORT": normalizeISODateString().split("T")[0],
};
const getDateData = (dateObject) => {
	const date = new Date().toISOString();
	return ({
		"ISO_NORMALIZED": normalizeISODateString(date),
		"SHORT": normalizeISODateString(date).split("T")[0],
	});
}

const _losungenJson = readLosungen2022().FreeXml.Losungen;
const toLosungenByDate = (losungenList) => {
	const losungen = {};
	losungenList.forEach(losung => {
		losungen[losung.Datum.split("T")[0]] = losung;
	});
	return losungen;
}
const LOSUNGEN_BY_DATE_2022 = toLosungenByDate(_losungenJson);

const getLosungByDate = (addedDays = 0) => {
	const date = new Date();
	date.setDate(date.getDate() + addedDays);
	return LOSUNGEN_BY_DATE_2022[date.toISOString().split("T")[0]];
}
const LOSUNG_TODAY = LOSUNGEN_BY_DATE_2022[todayDateString.SHORT];

const getverseData = (losung) => {
	const verse = losung.Losungsvers;
	// ["Psalm 116,9", "Psalm", "116,9", "116", "9", null]
	const re = /(.*) ((\d{1,3}),(\d{1,3})-?(\d{1,3})?)/g;
	const [
		full,
		book,
		versesInChapter,
		chapter,
		verseStart,
		verseEnd,
	] = re.exec(verse);

	const isMultiVerses = !!verseEnd && parseInt(verseEnd) > parseInt(verseStart);
	return {
		data: {
			full,
			book,
			chapterVerse: versesInChapter,
			chapter: parseInt(chapter),
			verse: parseInt(verseStart),
			verseEnd,
		},
		isMultiVerses,
	}
}

const germanToJson = (german) => {
	return {
		losungText: german.Losungstext,
	}
}

const hebrewToJson = (hebrew) => {
	return {
		losungText: hebrew.w.join(" "),
	}
}

const getLosungsDaten = () => {
	const bookNames = readBookNamesGermanToEnglish()
	const losung = getLosungByDate();
	const verseData = getverseData(losung);

	const xmlContent = fs.readFileSync(`./data/tanach/xml/${bookNames[verseData.data.book]}.xml`);
	const {Tanach} = JSON.parse(parser.toJson(xmlContent, {}));

	const titleData = Tanach.teiHeader.fileDesc.titleStmt.title
	const tanachTitle = {
		english: titleData[0].$t,
		hebrew: titleData[1].$t,
	}
	const bookTitle = {
		english: titleData[3].$t,
		hebrew: titleData[4].$t,
	}

	const chapters = Tanach.tanach.book.c
	const chapter = chapters[verseData.data.chapter - 1]
	const verse = chapter.v[verseData.data.verse - 1]
	console.log(chapter, verse, verseData.data.verse - 1)

	return {
		book: {
			tanachTitle,
			bookTitle,
		},
		verseData,
		verses: {
			hebrew: hebrewToJson(verse),
			german: germanToJson(losung),
		},
	}
}

const getLosungsDatenV2= () => {
	const losungen = parseLosungenTanachJson(new Date().getFullYear());
	return {
		date: todayDateString.SHORT,
		...losungen[todayDateString.SHORT],
	};
};


/* GET home page. */
router.get("/", (req, res, next) => {
	// res.set("json-spaces", "4");
	// res.setHeader('Content-Type', 'application/json');
	// res.status(200)
	res.json(getLosungsDatenV2());
});
router.get("/tanach", (req, res, next) => {
	res.send(LOSUNG_TODAY);
});
router.get("/nt", (req, res, next) => {
	res.send(LOSUNG_TODAY);
});
router.get("/at", (req, res, next) => {
	res.send(LOSUNG_TODAY);
});
router.get("/books", (req, res, next) => {
	res.send(LOSUNG_TODAY);
});

const getLosungAfterNDays = (req, res, next) => {
	const days = Math.abs(req.params["days"] || req.query["days"] || 1);
	res.send(getLosungByDate(days));
};
router.get("/after", getLosungAfterNDays);
router.get("/after/:days", getLosungAfterNDays);

const getLosungBeforeNDays = (req, res, next) => {
	const days = Math.abs(req.params["days"] || req.query["days"] || 1) * -1;
	res.send(getLosungByDate(days));
};
router.get("/before", getLosungBeforeNDays);
router.get("/before/:days", getLosungBeforeNDays);

router.get("/:year/:month/:day", (req, res, next) => {
	const dateData = [req.params["year"], req.params["month"], req.params["day"]];
	const date = `${dateData[0]}-${dateData[1]}-${dateData[2]}`
	res.send(LOSUNGEN_BY_DATE_2022[date]);
});

module.exports = router;
