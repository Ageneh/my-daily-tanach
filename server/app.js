const createError = require("http-errors");
const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const lessMiddleware = require("less-middleware");
const logger = require("morgan");

var allowedOrigins = ['http://localhost:3000',
	'http://yourapp.com'];

const indexRouter = require("./routes/index");

const app = express();
// const app = http.createServer((req, res) => {
// 	res.setHeader('Content-Type', 'application/json');
// 	res.end(JSON.stringify({ a: 1 }));
// });


const bodyParser = require('body-parser');
const cors = require('cors');

app.use(cors());
// app.use(cors({
// 	origin: function (origin, callback) {
// 		// allow requests with no origin
// 		// (like mobile apps or curl requests)
// 		if (!origin) return callback(null, true);
// 		if (allowedOrigins.indexOf(origin) === -1) {
// 			var msg = 'The CORS policy for this site does not ' +
// 				'allow access from the specified Origin.';
// 			return callback(new Error(msg), false);
// 		}
// 		return callback(null, true);
// 	}
// }));
// Configuring body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(lessMiddleware(path.join(__dirname, "public")));
app.use(express.static(path.join(__dirname, "public")));

app.use("/", indexRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
	next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
	// set locals, only providing error in development
	res.locals.message = err.message;
	res.locals.error = req.app.get("env") === "development" ? err : {};

	// render the error page
	res.status(err.status || 500);
	res.render("error");
});

module.exports = app;
