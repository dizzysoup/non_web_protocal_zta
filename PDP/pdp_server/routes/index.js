import express from "express";
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.redirect('https://de.yuntech.poc.com:5443')
});

router.post('/', function(req, res, next) {
  var username = req.body.username;
  var password = req.body.password;

  res.json({ status: 'success', message: 'Received username and password successfully.' });
});

export default router
