//..............Include Express..................................//
const express = require('express');
router = express.Router();
const fs = require('fs');
const ejs = require('ejs');
const fetch = require('node-fetch');
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;
const KEYS = require('./config/keys.json');

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

app.use(session({
  resave: false,
  saveUninitialized: true,
  cookie: {
    maxAge: 600000 //600 seconds of login time before being logged out
  },
  secret: KEYS["session-secret"]
}));
app.use(passport.initialize());
app.use(passport.session());

passport.use(new GoogleStrategy({
    clientID: KEYS["google-client-id"],
    clientSecret: KEYS["google-client-secret"],
    callbackURL: "http://localhost:3000/auth/google/callback"
    //todo: port==process.env.PORT? :
  },
  function(accessToken, refreshToken, profile, done) {
    userProfile = profile; //so we can see & use details form the profile
    return done(null, userProfile);
  }
));

passport.serializeUser(function(user, cb) {
  cb(null, user);
});
passport.deserializeUser(function(obj, cb) {
  cb(null, obj);
});

/*
  This triggers the communication with Google
*/
app.get('/auth/google',
  passport.authenticate('google', {
    scope: ['email', 'openid']
  }));

/*
  This callback is invoked after Google decides on the login results
*/
app.get('/auth/google/callback',
  passport.authenticate('google', {
    failureRedirect: '/error?code=401'
  }),
  async function(request, response) {
    let playerEmail = request.user._json.email;
    console.log(playerEmail);
    let url = 'http://127.0.0.1:5000/users/exists/' + playerEmail;
    let res = await fetch(url);
    let details = JSON.parse(await res.text())["message"];

    console.log(details)

    if(details){
      response.redirect('/login');
    } else {
          url = 'http://127.0.0.1:5000/users'
          const headers = {
              "Content-Type": "application/json",
          }
          res = await fetch(url, {
              method: "POST",
              headers: headers,
              body: JSON.stringify({email: playerEmail}),
          });
        
          let posted_user = await res.text();
          details = JSON.parse(posted_user);
          console.log("Returned user:", details)
          url = 'http://127.0.0.1:5000/users/doctors/'+email;
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
  });

app.get("/auth/logout", (request, response) => {
  request.logout();
  response.redirect('/');
});

module.exports = router;

//Ok, User doesn't need a username. you can go just off email and id. 


app.get('/', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //-------------------Testing purposes: Verifying users actually exist in DB------------//
  //-----------------------------------//
  let url = 'http://127.0.0.1:5000/states';
  let res = await fetch(url);
  let details = JSON.parse(await res.text());  

  
  console.log(details)
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/home",{
    states: details
  });
});

app.get('/admin', async function(request, response) {
  console.log(request.method, request.url)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/adminInput",{
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

app.get('/users/:email', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let email = request.params.email;

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/user_details",{
    feedback:"",
    email: email,
  });
});

app.get('/macro', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let location = request.query.state

  let url = 'http://127.0.0.1:5000/states/'+location;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  console.log("Requested state per click:")
  console.log(details.overview)
  let overview = details.overview
  let map = ["Banned", "Restricted", "Allowed", "Protected"]
  for(key in overview){
    overview[key] = map[overview[key]]
  }

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("info/macro",{
    feedback:"",
    location:location,
    rank: "supportive",
    overview: overview
    
  });
});

app.get('/login', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let email = request.user._json.email;

  //Get user login info from query string portion of url
  if(email){
    //get alleged user 
    let url = 'http://127.0.0.1:5000/users/'+email;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested user per email:")
    console.log(details)

    //Verify user password matches
      url = 'http://127.0.0.1:5000/users/doctors/'+email;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/specificLoc", {
        feedback:"",
        email: email,
        doctorlist: details
    })}else{
      response.status(404); //404 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("info/login", {
        feedback:"Requested user does not exist"
      });
    }
  });//GET /login

  app.get('/users/delete/:email', async function(request, response) {
    console.log(request.method, request.url) //event logging
  
    let email = request.params.email;
    console.log("Info recieved for Deletion:", email)
  
    let url = 'http://127.0.0.1:5000/users/'+email;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested user per username:")
    console.log(details)
      res = await fetch(url, {
          method: "DELETE"
      });
    
      let deleted_user = await res.text();
      details = JSON.parse(deleted_user);
      console.log("Returned user:", details)
      
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/login",{
        feedback:"",
        email:""
      });
    })

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
    

app.post('/states', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //Get user information from body of POST request
  let name = request.body.statename;
  let overview = {
    minorsHRT: request.body.minorsHRT,
    minorsDYS: request.body.minorsDYS,
    minorsST: request.body.minorsST,
    adultsHRT: request.body.adultsHRT,
    adultsDYS: request.body.adultsDYS,
    adultsSUR: request.body.adultsSUR
  } 

  // HEADs UP: You really need to validate this information!
  console.log("Info recieved:", name, overview)
  console.log(name.length, Object.keys(overview).length)

  if (name.length > 0 & Object.keys(overview).length > 0){
    let url = 'http://127.0.0.1:5000/states/'+name;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested State per name:")
    console.log(details)

    if (JSON.stringify(details) === '{}'){
      url = 'http://127.0.0.1:5000/states'
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            name:name,
            overview:overview
            }),
      });
    
      url = 'http://127.0.0.1:5000/states/'+name;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      console.log("Returned State:", details)
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/adminInput", {
        feedback:"State Added",
        username: ""
    });
    } else {
      let name = request.body.statename;
      let overview = {
        minorsHRT: request.body.minorsHRT,
        minorsDYS: request.body.minorsDYS,
        minorsST: request.body.minorsST,
        adultsHRT: request.body.adultsHRT,
        adultsDYS: request.body.adultsDYS,
        adultsSUR: request.body.adultsSUR
      } 
      let url = 'http://127.0.0.1:5000/states/' +name;
      const headers = {
          "Content-Type": "application/json",
      }
      let res = await fetch(url, {
          method: "PUT",
          headers: headers,
          body: JSON.stringify({
            name:name,
            overview:overview
            }),
      });
      
      let posted_state = await res.text();
      let details = JSON.parse(posted_state);
      console.log("Returned state:", details)
      url = 'http://127.0.0.1:5000/states/' +name
      res = await fetch(url);
      details = JSON.parse(await res.text());
      console.log("Requested state per click:")
      console.log(details.overview)
      overview = details.overview
      let map = ["Banned", "Restricted", "Allowed", "Protected"]
      for(key in overview){
        overview[key] = map[overview[key]]
      }

      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/macro",{
        feedback:"",
        location:name,
        rank: "supportive",
        overview: overview
        
      }); 
    } 
  } else {
    response.status(401); //401 Unauthorized
    response.setHeader('Content-Type', 'text/html')
    response.render("info/adminInput", {
    feedback:"Missing Info. Please make sure each field is filled.",
    username:""
    });
  }
}); //THE PUT REQUEST DOES NOT WORK RIGHT NOW. WORK ON LATER. 

app.post('/doctors', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //Get user information from body of POST request
  let name = request.body.name;
  let doctorLocation = request.body.doctorLocation;
  let summary = request.body.summary;
  let number = request.body.number
  let email = request.body.email
  let link = request.body.link

  // HEADs UP: You really need to validate this information!
  console.log("Info recieved:", name, doctorLocation, summary, number, email, link)

  if (name.length > 0 & doctorLocation.length > 0 & number.length > 0 & email.length > 0){
    let url = 'http://127.0.0.1:5000/doctors/'+name;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());
    console.log("Requested Doctor per username:")
    console.log(details)

    if (JSON.stringify(details) === '{}'){
      url = 'http://127.0.0.1:5000/doctors'
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            name:name,
            doctorLocation: doctorLocation,
            summary: summary,
            contactInfo : {
              number: number,
              email: email
            },
            link: link

          }),
      });
    
      url = 'http://127.0.0.1:5000/doctors/'+name;
      res = await fetch(url);
      details = JSON.parse(await res.text());
      console.log("Returned user:", details)
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/adminInput", {
        feedback:"Doctor Added",
        username: ""
    });
    } else {
      url = 'http://127.0.0.1:5000/doctors/' +name;
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "PUT",
          headers: headers,
          body: JSON.stringify({
            name:name,
            location: doctorLocation,
            summary: summary,
            contactInfo : {
              number: number,
              email: email
            },
            link: link
          }),
      });
      
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      console.log("Returned user:", details)
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("info/admin", {
        feedback:"Doctor Updated",
        username: "",
    });
    } 
  } else {
    response.status(401); //401 Unauthorized
    response.setHeader('Content-Type', 'text/html')
    response.render("info/admin", {
    feedback:"Missing Info. Please make sure each field is filled.",
    username:""
    });
  }
}); //THE PUT REQUEST DOES NOT WORK RIGHT NOW. WORK ON LATER. 

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
