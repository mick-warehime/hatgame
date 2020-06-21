var path = require("path");
var express = require("express");

var DIST_DIR = path.join(__dirname, "/dist");
var app = express();

app.use(express.static(DIST_DIR));

app.get("*", function (req, res) {
  res.sendFile(path.join(DIST_DIR, "index.html"));
});

var port = process.env.DEVPORT || process.env.PORT || 8080;
var host = '0.0.0.0';

//http
app.listen(port, host, function() {
    console.log('Listening on port %d', port);
});