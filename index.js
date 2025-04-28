const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.redirect('/books');
});

router.get('/books', (req, res) => {
  res.render('books');
});

router.get('/customers', (req, res) => {
  res.render('customers');
});

router.get('/borrowings', (req, res) => {
  res.render('borrowings');
});

module.exports = router;
