var path = require('path');
var http = require('http');
var fs = require('fs');
var bodyParser = require('body-parser');
var express = require('express');
const { Client } = require('pg');
const app = express();

var port=8081; 

const db = new Client({
    host: 'localhost',
	port: 5432,
    user: 'postgres',
    password: 'password',
    database: 'data_quality_demo'
});

db.connect((err) => {
    if (err) {
        throw err;
    }
    console.log('Connected to database');
});
global.db = db;


app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 

app.use(express.static('static'));

app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded()); // to support URL-encoded bodies

app.set('port', process.env.port || port); // set express to use this port
