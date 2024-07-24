var express = require('express');
var router = express.Router();

router.post('/register', function(req, res, next) {
    
    res.json({ status: 'success', message: 'register  successfully.' });
  });
  

module.exports = router;