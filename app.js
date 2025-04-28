const express = require('express');
const path = require('path');
const app = express();
const expressLayouts = require('express-ejs-layouts');  // <-- NEW
const indexRouter = require('./routes/index');

app.use(expressLayouts);  // <-- NEW

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use('/', indexRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
});
