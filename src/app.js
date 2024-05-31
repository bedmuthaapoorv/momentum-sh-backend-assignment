import router from './routes/index.js';
import express from 'express'
import cookieParser from 'cookie-parser'
const PORT = 3000;

const app = express();

app.use(express.json())
app.use(cookieParser())
app.use(router);
app.get('/', (req, res) => {
    res.send('Hello World');
});

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});
