const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

app.post('/save-location', (req, res) => {
    const { latitude, longitude } = req.body;

    // Example: Save location to the database (replace with actual DB logic)
    console.log(`Saving location: Latitude=${latitude}, Longitude=${longitude}`);
    // Add database logic here...

    res.status(200).send({ message: 'Location saved successfully.' });
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
