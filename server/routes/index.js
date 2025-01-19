const express = require("express");
const router = express.Router();

const fs = require("fs");
const t = require("../py_app/resources/books/en/en.json");

const parseLosungenTanachJson = (year) => {
	// e.g.: losung-tanach-2022.json
	const content = fs.readFileSync(`./data/v2/losung-tanach-${year}.json`);
	console.log("to json ->", content);
	const json = JSON.parse(content);
	console.log("to json ->", json);
	return json;
}

const normalizeISODateString = (dateString = undefined) => {
	if (!dateString || dateString.length < 1) {
		dateString = new Date().toISOString();
	}
	return `${dateString.split("T")[0]}T00:00:00`;
}

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

const getLosungsDatenV2 = () => {
	const losungen = parseLosungenTanachJson(new Date().getFullYear());
	return {
		date: todayDateString.SHORT,
		...losungen[todayDateString.SHORT],
	};
};

const getDataEnglishTransformed = () => {
	// const t = (require("../data/v2/en_OT.json")) // [{abbrev, chapters, name}]
	const [OT, NT] = writeTestaments()

	const transformed = t.map(({abbrev, chapters, name}) => {
		const perChapter = {}
		chapters.forEach((chapter, index) => {
			perChapter[index+1] = chapter
		})

		return {
			[name]: {
				...perChapter,
			}
		}
	});

	Object.values(transformed)
		.forEach(book => {
			const bookName = Object.keys(book)[0]
			const bookNameOutput = (bookName.includes("1") || bookName.includes("2")) ? [...bookName.split(" ").reverse()].join("_") : bookName

			fs.writeFileSync(`./data/v2/${bookNameOutput}.json`, JSON.stringify({
				[bookNameOutput]: book[bookName]
			}))
		})

	return transformed.slice(0, 2)
}

const getDataGermanTransformed = () => {
	const t = (require("../data/v2/books/de/de_OT.json")) // [{abbrev, chapters, name}]
	// const [OT, NT] = writeTestaments("de")

	const transformed = t.map(({abbrev, chapters, name}) => {
		const perChapter = {}
		chapters.forEach((chapter, index) => {
			perChapter[index+1] = chapter
		})

		return {
			[name]: {
				...perChapter,
			}
		}
	});

	Object.values(transformed)
		.forEach(book => {
			const bookName = Object.keys(book)[0]
			const bookNameOutput = (bookName.includes("1") || bookName.includes("2")) ? [...bookName.split(" ").reverse()].join("_") : bookName

			fs.writeFileSync(`./data/v2/de__${bookNameOutput}.json`, JSON.stringify({
				[bookNameOutput]: book[bookName]
			}))
		})

	return transformed.slice(0, 2)
}

const writeTestaments = (filename = "en") => {
	const t = (require(`../data/v2/${filename}.json`)) // [{abbrev, chapters, name}]
	const OT = t.slice(0, 39).map(({abbrev, chapters, name}) => {
		return {
			abbrev,
			chapters,
			name,
		}
	});
	// fs.writeFileSync(`./data/v2/${filename}_OT.json`, JSON.stringify(OT))

	const NT = t.slice(39, 66).map(({abbrev, chapters, name}) => {
		return {
			abbrev,
			chapters,
			name,
		}
	});
	// fs.writeFileSync(`./data/v2/${filename}_NT.json`, JSON.stringify(NT))

	return [OT, NT]
}

/* GET home page. */
router.get("/", (req, res, next) => {
	res.set("json-spaces", "4");
	res.json(getLosungsDatenV2());
});

// router.get("/", (req, res, next) => {
// 	res.set("json-spaces", "4");
// 	res.json(getDataGermanTransformed());
// });

module.exports = router;
