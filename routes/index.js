const express = require("express");
const router = express.Router();

const fs = require("fs");

const parseLosungenTanachJson = (year) => {
	// e.g.: losung-tanach-2022.json
	const content = fs.readFileSync(`./data/v2/losung-tanach-${year}.json`);
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

const getLosungsDatenV2= () => {
	const losungen = parseLosungenTanachJson(new Date().getFullYear());
	return {
		date: todayDateString.SHORT,
		...losungen[todayDateString.SHORT],
	};
};

/* GET home page. */
router.get("/", (req, res, next) => {
	res.set("json-spaces", "4");
	res.json(getLosungsDatenV2());
});

module.exports = router;
