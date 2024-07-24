var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.redirect('http://de.yunpoc.edu.tw:5000')
});

router.post('/', function(req, res, next) {
  var username = req.body.username;
  var password = req.body.password;

  res.json({ status: 'success', message: 'Received username and password successfully.' });
});

module.exports = router;
