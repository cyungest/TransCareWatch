//..............Include Express..................................//
const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const fetch = require('node-fetch');

//..............Create an Express server object..................//
const app = express();

//Socket connection
let server = require('http').Server(app);
let io = require('socket.io')(server);

//..............Apply Express middleware to the server object....//
app.use(express.json()); //Used to parse JSON bodies (needed for POST requests)
app.use(express.urlencoded());
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

//.............Define server routes..............................//
//Express checks routes in the order in which they are defined

app.get('/', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //-------------------Testing purposes: Verifying users actually exist in DB------------//
  //-----------------------------------//

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/home",{
  });
});


// Because routes/middleware are applied in order,
// this will act as a default error route in case of
// a request fot an invalid route

app.get('/login', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //-------------------Testing purposes: Verifying users actually exist in DB------------//
  //-----------------------------------//

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/login",{
  });
});

app.get('/users', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/user_details",{
    feedback:"",
    username:""
  });
});

app.get('/macro', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let location = request.query.state

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/macro",{
    feedback:"",
    location:location,
    rank: "supportive"
    
  });
});

app.use("", function(request, response){
  response.status(404);
  response.setHeader('Content-Type', 'text/html')
  response.render("error", {
    "errorCode":"404",
    feedback:"",
    username:""
  });
});

//..............Start the server...............................//
const port = process.env.PORT || 3000;
app.set('port', port);
server.listen(port, function() {
  console.log('Server started at http://127.0.0.1:'+port+'.')
});
