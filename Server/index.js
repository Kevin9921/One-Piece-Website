const express = require('express')
const app = express()
let mysql = require('mysql');

let charData

let connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'one Piece'
});

connection.connect(function(err) {
    if (err) {
      return console.error('error: ' + err.message);
    }
    connection.query("SELECT * FROM onepiece_characters LIMIT 3", 
        function (err, result) {
            if (err) throw err;
            charData = result
            console.log("yo",charData);
        });
    console.log('Connected to the MySQL server.');
  });

app.get("/api", (req, res) => {
    res.json(charData)
})

app.listen(5000, () => {console.log("Server started on port 5000")})