const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const PORT = 3000; // Установите другой порт
const PHONE_NUMBER = '+79779550226'; // Номер для отправки заявок

app.use(express.static(__dirname)); // Для статики
app.use(bodyParser.json()); // Для обработки JSON

app.post('/submit-request', (req, res) => {
    const { problem, phone, address } = req.body;

    if (!problem || !phone || !address) {
        return res.status(400).send('Все поля обязательны!');
    }

    console.log(`Заявка: 
        Проблема: ${problem}
        Контактный номер: ${phone}
        Адрес проживания: ${address}`);

    // Логика отправки на номер (можно интегрировать API, например, Twilio)
    res.status(200).send('Заявка отправлена');
});

app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});
