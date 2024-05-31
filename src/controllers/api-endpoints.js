import express from 'express'
import cookieParser from 'cookie-parser'
const PORT = 3000;

const app = express();

app.use(express.json())
app.use(cookieParser())

app.get('/', (req, res) => {
    res.send('Hello World');
});

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});