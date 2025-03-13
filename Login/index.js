//const cookieSession = require("cookie-session");
const express = require("express");
const session = require("express-session");
const passport = require("passport");
const cors = require("cors");
const passportSetup = require("./passport");
const authRoute = require("./routes/auth");
const app = express();
require("dotenv").config();
console.log("NODE_ENV:", process.env.NODE_ENV);

// for localhost
/*app.use(
  cookieSession({ name: "session", keys: ["brahma"], maxAge: 24 * 60 * 60 * 100 })
);*/

app.set("trust proxy", 1); // Required for sessions to work behind a proxy

app.use(session({
  secret: "dattatreya",  // Change this to a strong secret
  resave: false,
  saveUninitialized: true,
  // for localhost 
  cookie: {  maxAge: 24 * 60 * 60 * 1000, secure: true, sameSite: "none"  }  // Set `true` if using HTTPS
  /*
  cookie:{
    maxAge: 24 * 60 * 60 * 1000,
    secure: true, //Enable in production (set to false for localhost testing)
    httpOnly: true,  // Prevents client-side access to the cookie
    sameSite: process.env.NODE_ENV === "production" ? "lax" : "none", //Important for cross-origin requests,"lax" for production
  }*/
}));


////////////////////////////////////
/*
app.use((req, res, next) => {
  console.log("Session Data 1:", req.session);
  next();
});
*/
/*app.get("/test-cookie", (req, res) => {
  res.cookie("test_cookie", "test_value", {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: process.env.NODE_ENV === "production" ? "none" : "lax",
  });
  res.send("Test cookie sent!");
});
*/

///////////////////////////////////

app.use(passport.initialize());
app.use(passport.session());


app.use(
  cors({
    //origin: "http://localhost:5173",
    origin: "https://margentai.netlify.app",
    methods: "GET,POST,PUT,DELETE",
    credentials: true,
  })
);

app.use(express.static('public'));

app.use("/auth", authRoute);

app.listen("5000", () => {
  console.log("Server is running!");
});
