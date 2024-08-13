var express = require('express');
var router = express.Router();
const axios = require('axios')

router.post('/register/begin', function(req, res, next) {
    const requestData = req.body 

    axios.post('http://de.yunpoc.edu.tw:5000/register/begin' , requestData)
      .then(response => {
        res.json(response.data);
      })
      .catch(error => {
        console.error("Error forward ");
        res.status(500).json({status: 'error' , error : error.message});
      })
  });

router.post('/register/complete', function(req, res, next) {
    const requestData = req.body 
   
    
    axios.post('http://de.yunpoc.edu.tw:5000/register/complete' , requestData)
      .then(response => {
        res.json(response.data);
      })
      .catch(error => {
        console.error("Error forward ");
        res.status(500).json({status: 'error' , error : error.message});
      })
      
});

router.post('/login/begin', function(req, res, next) {
  const requestData = req.body 

  axios.post('http://de.yunpoc.edu.tw:5000/login/begin' , requestData)
    .then(response => {
      res.status(200).json(response.data);
    })
    .catch(error => {
      console.error("Error forward ");
      res.status(500).json({status: 'error' , error : error.message});
    })
});

router.post('/login/complete', function(req, res, next) {
  const requestData = req.body 
  axios.post('http://de.yunpoc.edu.tw:5000/login/complete' , requestData)
    .then(response => {
      res.json(response.data);
    })
    .catch(error => {
      console.error("Error forward ");
      res.status(500).json({status: 'error' , error : error.message});
    })
    
});



module.exports = router;