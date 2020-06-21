var path = require("path");
var express = require("express");
var https = require("https");
var fs = require('fs')

var DIST_DIR = path.join(__dirname, "/dist");
var app = express();

app.use(express.static(DIST_DIR));

app.get("*", function (req, res) {
  res.sendFile(path.join(DIST_DIR, "index.html"));
});

var port = process.env.DEVPORT || process.env.PORT || 443;
var host = '0.0.0.0';
https.createServer({
  key: fs.readFileSync('./client/server.key'),
  cert: fs.readFileSync('./client/server.cert')
}, app).listen(port, host, function() {
    console.log('Listening on port %d', port);
});