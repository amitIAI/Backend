const GoogleStrategy = require("passport-google-oauth20").Strategy;
const GithubStrategy = require("passport-github2").Strategy;
const FacebookStrategy = require("passport-facebook").Strategy;
const passport = require("passport");
require("dotenv").config();


const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;

GITHUB_CLIENT_ID = "your id";
GITHUB_CLIENT_SECRET = "your id";

FACEBOOK_APP_ID = "your id";
FACEBOOK_APP_SECRET = "your id";

console.log("entering passport google strategy")
passport.use(
  new GoogleStrategy(
    {
      clientID: GOOGLE_CLIENT_ID,
      clientSecret: GOOGLE_CLIENT_SECRET,
      callbackURL: "https://login-service-9qx5.onrender.com/auth/google/callback",
      //callbackURL: "https://margentai.netlify.app/auth/google/callback",
    },
    async (accessToken, refreshToken, profile, done) =>{
      
      const user = {
          id: profile.id,
          name: profile.displayName,
          email: profile.emails?.[0]?.value || null,  // Extracts email safely
          photo: profile.photos?.[0]?.value || null,
          provider: profile.provider
      };
      console.log("entering user data:", user);
      return done(null, user);  // Pass the user object to the session
    }));
      
passport.use(
  new GithubStrategy(
    {
      clientID: GITHUB_CLIENT_ID,
      clientSecret: GITHUB_CLIENT_SECRET,
      callbackURL: "/auth/github/callback",
    },
    function (accessToken, refreshToken, profile, done) {
      done(null, profile);
    }
  )
);

passport.use(
  new FacebookStrategy(
    {
      clientID: FACEBOOK_APP_ID,
      clientSecret: FACEBOOK_APP_SECRET,
      callbackURL: "/auth/facebook/callback",
    },
    function (accessToken, refreshToken, profile, done) {
      done(null, profile);
      // if using mongo db
      /*
      const user = {
        username: profile.displayName,
        avatar: profile.photos[0],
        id: profile.id,
      };

      user.modal
      */
    }
  )
);

// Required if using sessions

passport.serializeUser((user, done) => {
  console.log("🔄 No user serializing User:");
  if(user){
    console.log("Serializing User:",); }
  done(null, user);
});

passport.deserializeUser((user, done) => {
  console.log("🔄 Deserializing User:");

 if (!user) {
  console.log("❌ No user found during deserialization!");
  // return done(new Error("User not found"), null);
  }

  done(null, user);
});

/*
passport.serializeUser((user, done) => {
  console.log("Serializing User ID:", user.id);
  done(null, user.id); // ✅ Store only the user ID in the session
});

passport.deserializeUser((id, done) => {
  console.log("🔄 Deserializing User ID:", id);
  
  // Simulate a database lookup for now
  const user = { id, name: "Amit Pahwa", email: "amit@indivisionai.com"  }; 

  done(null, user);
});

*/
