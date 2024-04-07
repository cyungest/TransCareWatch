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

app.get('/admin', async function(request, response) {
  console.log(request.method, request.url)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/admin",{
    feedback:"",
    username:""
  });

})
// Because routes/middleware are applied in order,
// this will act as a default error route in case of
// a request fot an invalid route

app.get('/loginpage', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //-------------------Testing purposes: Verifying users actually exist in DB------------//
  //-----------------------------------//

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/login",{
    feedback:""
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

app.get('/login', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //Get user login info from query string portion of url
  let username = request.query.username;
  let password = request.query.password;
  if(username && password){
    //get alleged user 
    let url = 'http://127.0.0.1:5000/users/'+username;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested user per username:")
    console.log(details)

    //Verify user password matches
    if (details["password"] && details["password"]==password){
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      console.log("Returned user:", details)
      url = 'http://127.0.0.1:5000/users/doctors/'+username;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/specificLoc", {
        feedback:"",
        username: username,
        doctorlist: details
    });
    }else if (details["password"] && details["password"]!=password){
      response.status(401); //401 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("info/login", {
        feedback:"Incorrect password. Please try again"
      });
    }else{
      response.status(404); //404 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("info/login", {
        feedback:"Requested user does not exist"
      });
    }
  }else{
    response.status(401); //401 Unauthorized
    response.setHeader('Content-Type', 'text/html')
    response.render("info/login", {
      feedback:"Please provide both a username and password"
    });
  }
  
});//GET /login

app.post('/users', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //Get user information from body of POST request
  let username = request.body.username;
  let email = request.body.email;
  let password = request.body.password;
  // HEADs UP: You really need to validate this information!
  console.log("Info recieved:", username, email, password)

  if (username.length > 0 & email.length > 0 & password.length > 0){
    let url = 'http://127.0.0.1:5000/users/'+username;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested user per username:")
    console.log(details)

    url = "http://127.0.0.1:5000/users"
    res = await fetch(url);
    user_list = JSON.parse(await res.text());
    if(user_list.some(user => user.username == username)) {
      response.status(401); //401 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("info/user_details", {
      feedback:"Duplicate Username. Please try a different name.",
      username:""

    });
    } else if (user_list.some(user => user.email == email)){
      response.status(401); //401 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("info/user_details", {
      feedback:"Duplicate Email. Please try a different email.",
      username:""

    })
    } else if (JSON.stringify(details) === '{}'){
      url = 'http://127.0.0.1:5000/users'
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify(request.body),
      });
    
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      console.log("Returned user:", details)
      url = 'http://127.0.0.1:5000/users/doctors/'+username;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/specificLoc", {
        feedback:"",
        username: username,
        doctorlist: details
    });
    } else {
      url = 'http://127.0.0.1:5000/users/' +username;
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "PUT",
          headers: headers,
          body: JSON.stringify(request.body),
      });
      
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      console.log("Returned user:", details)
      url = 'http://127.0.0.1:5000/users/doctors/'+username;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/specificLoc", {
        feedback:"",
        username: username,
        doctorlist: details
    });
    } 
  } else {
    response.status(401); //401 Unauthorized
    response.setHeader('Content-Type', 'text/html')
    response.render("info/user_details", {
    feedback:"Missing Info. Please make sure each field is filled.",
    username:""
    });
  }

  

 
}); //POST /user

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
