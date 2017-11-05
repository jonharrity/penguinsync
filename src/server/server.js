var fs = require('fs');
var path = require('path');
var secretPath = path.join(__dirname, 'secret');
/*var clientSecret = '';
fs.readFile(secretPath, 'utf8', (err, data) => {
	if( err ) {
		console.log(err.name+': ' + err.message);
		throw err;
	}
	clientSecret = data;
});
*/
var clientSecret = process.env.CLIENT_SECRET;

var clientId = '402842006506-q8qjida6ob94156d7dv33r5l00n69c85.apps.googleusercontent.com';
var redirectURI = 'https://fierce-bastion-75518.herokuapp.com/cb';

var express = require('express');
var app = express();
var port = (process.env.PORT || 3000);
var maxStateStorageTime = 1000 * 60 * 5;

var cbResPath = path.join(__dirname, 'cb.html');

app.set('states', {});

//default
app.get('/', (req,res) => {
	res.send('');
});

//takes query: state
app.get('/push', (req,res) => {
	var store = app.get('states');
	var state = req.query.state;
	if( typeof state === 'string' ) {
		store[state] = {time: Math.floor(new Date()/1000)};
		app.set('states', store);
		setTimeout((state) => {
			var store = app.get('states');
			delete store[state];
			app.set('states',store);
		}, maxStateStorageTime, state);
	}
	res.send('received');
});
app.get('/cb', (req,res) => {
	var store = app.get('states');
	var state = req.query.state;
	var code = req.query.code;
	if( typeof state === 'string' && typeof code === 'string' && (typeof store[state] != 'undefined') ) {
		var xhr = new XMLHttpRequest();
		var params = [	'code='+code,
						'client_id='+clientId,
						'client_secret='+clientSecret,
						'redirect_uri='+redirectURI,
						'grant_type=authorization_code'
					].join('&');
		xhr.open('POST','https://www.googleapis.com/oauth2/v4/token',true);
		xhr.setRequestHeader('Host', 'www.googleapis.com');
		xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
		xhr.send(params);
		xhr.onreadystatechange = function(v) { 
			return () => {
				var conn = v.conn;
				if( conn.readyState === XMLHttpRequest.DONE && conn.status === 200 ) {
					var store = app.get('states');
					var state = v.state;
					var parsed = JSON.parse(conn.responseText);
					//response should contain fields: access_token, expires_in, token_type, refresh_token
					store[state] = parsed;
					app.set('states',store);
				}
				else
					console.log(conn.response);
			};
		}({conn: xhr, state: state});
	}
	res.sendFile(cbResPath);
});

//takes query: state
app.get('/pop', (req,res) => {
	var store = app.get('states');
	var state = req.query.state;
	if( typeof state === 'string' && (typeof store[state] != 'undefined') && (typeof store[state]['access_token'] != 'undefined') ) {
		var obj = store[state];
		res.send(JSON.stringify(obj));
	}
	else
		res.send('');
});


app.listen(port,()=>console.log('penguinsync auth server started'));


