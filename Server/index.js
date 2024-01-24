const express = require('express')
//const cors = require('cors');
const app = express()
//app.use(cors());
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
    connection.query("SELECT * FROM onepiece_characters WHERE character_id=3", 
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

app.get("/api/newCharacter", (req, res) => {
    connection.query("SELECT * FROM onepiece_characters ORDER BY RAND() LIMIT 1", 
      function (err, result) {
        if (err) {
          console.error('Error fetching new character:', err);
          return res.status(500).json({ error: 'Internal Server Error' });
        }
  
        res.json(result);
      }
    );
  });

app.listen(5000, () => {console.log("Server started on port 5000")})