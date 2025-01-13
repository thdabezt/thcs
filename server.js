const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const jsonDirectory = path.join(__dirname, 'json');

// Serve static files (HTML and JSON)
app.use(express.static(__dirname));

// Serve the main HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'main.html'));
});

// Endpoint to list quiz JSON files
app.get('/list-quizzes', (req, res) => {
  fs.readdir(jsonDirectory, (err, files) => {
    if (err) {
      return res.status(500).send('Error reading directory');
    }
    const jsonFiles = files.filter(file => file.endsWith('.json'));
    res.json(jsonFiles);
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
