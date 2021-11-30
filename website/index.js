var express = require('express');
var app     = express();

var mysql = require('mysql2');
var connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '1234',
  database: 'proddis'
});

app.get('/random', function(req, res){
    console.log('firstName: ', req.query.firstName);
    res.send(`echoing: ${req.query.firstName}`);
    connection.query(`
        INSERT INTO contacts (
            firstName,
            lastName,
            phoneNumber,
            email,
            university,
            major
        ) VALUES (
            '${req.query.firstName}',
            '${req.query.lastName}',
            '${req.query.phoneNumber}',
            '${req.query.email}',
            '${req.query.university}',
            '${req.query.major}'
        )`,
        function(err, results, fields) {
            console.log(results);
            res.send(results);
        })
 });

app.get('/read', function(req, res){

    connection.query(
      'SELECT * FROM `contacts`',
      function(err, results, fields) {
        console.log(results);
        res.send(results);
      }
    );

 });

app.listen(3001, function(){
    console.log('Running on port 3001');
})

// used to serve static files from public directory
app.use(express.static('public'));



