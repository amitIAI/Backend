const router = require("express").Router();
const passport = require("passport");

//const CLIENT_URL = "http://localhost:5173/";
const CLIENT_URL = "https://margentai.netlify.app/";


router.get("/login/success", (req, res) => {
  console.log("🔍 Request received at /auth/login/success");
  console.log("Session Data:", req.session);
  console.log("req.session.passport:", req.session.passport)
  console.log("User Data Before:", req.user);
 // console.log("Deserialized User Data Before:", user);

  /////////////////////////////////////
  console.log("req.session.passport?.user", req.session.passport?.user)
  // ✅ Force debug session storage
  if (!req.user) {
    console.log("❌ req.user is undefined! Checking req.session.passport...");
    if (req.session?.passport?.user) {
      console.log("✅ Found user in session! Manually assigning to req.user...");
      req.user = req.session.passport.user;
    } else {
      console.log("❌ No user found in session!");
    }
  }

  console.log("User Data AFTER:", req.user);
  ///////////////////////////////////////

  if (req.user) {
    res.status(200).json({
      success: true,
      message: "Authentication successful",
      user: req.user,
      //   cookies: req.cookies
    });
  } else {
      res.status(401).json({ success: false, message: "Unauthorized" });
  }
});

router.get("/login/failed", (req, res) => {
  res.status(401).json({
    success: false,
    message: "failure",
  });
});

router.get("/logout", (req, res, next) => {
  req.logout(function (err){
    if (err) {
      return next(err);  // Pass error to Express error handler
    }
    req.session.destroy(() => {
      res.redirect(CLIENT_URL);
    });
  });
});

router.get("/google", passport.authenticate("google", { scope: ["profile", "email"] }));

router.get(
  "/google/callback",
  passport.authenticate("google", {
    successRedirect: CLIENT_URL,
    failureRedirect: "/login/failed",
  })
);

router.get("/github", passport.authenticate("github", { scope: ["profile"] }));

router.get(
  "/github/callback",
  passport.authenticate("github", {
    successRedirect: CLIENT_URL,
    failureRedirect: "/login/failed",
  })
);

router.get("/facebook", passport.authenticate("facebook", { scope: ["profile"] }));

router.get(
  "/facebook/callback",
  passport.authenticate("facebook", {
    successRedirect: CLIENT_URL,
    failureRedirect: "/login/failed",
  })
);

module.exports = router