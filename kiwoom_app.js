const app = require("express")();
const http = require("http").createServer(app);
const io = require("socket.io")(http);
const amqp = require("amqplib/callback_api");
const dotenv = require("dotenv");

dotenv.config()

const {
  RABBITMQ_HOST,
  RABBITMQ_PORT,
  RABBITMQ_USER,
  RABBITMQ_PASSWORD
} = process.env;

// express default index page rendering
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

const rabbitUri = `amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}//`;

// RabbitMQ client
amqp.connect(rabbitUri, function (err0, connection) {
  if (err0) {
    throw err0;
  }

  connection.createChannel((err1, channel) => {
    if (err1) {
      throw err1;
    }

    io.on('connection', (socket) => {

      const kiwoomKospiAStocksQueue = "kiwoom_kospi_a_stocks_data";
      channel.assertQueue(kiwoomKospiAStocksQueue, { durable: false });
      channel.consume(
        kiwoomKospiAStocksQueue,
        (msg) => {
          io.emit("kiwoom_kospi_a_stocks", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

      const kiwoomKospiBStocksQueue = "kiwoom_kospi_b_stocks_data";
      channel.assertQueue(kiwoomKospiBStocksQueue, { durable: false });
      channel.consume(
        kiwoomKospiBStocksQueue,
        (msg) => {
          io.emit("kiwoom_kospi_b_stocks", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

      const kiwoomKosdaqAStocksQueue = "kiwoom_kosdaq_a_stocks_data";
      channel.assertQueue(kiwoomKosdaqAStocksQueue, { durable: false });
      channel.consume(
        kiwoomKosdaqAStocksQueue,
        (msg) => {
          io.emit("kiwoom_kosdaq_a_stocks", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

      const kiwoomKosdaqBStocksQueue = "kiwoom_kosdaq_b_stocks_data";
      channel.assertQueue(kiwoomKosdaqBStocksQueue, { durable: false });
      channel.consume(
        kiwoomKosdaqBStocksQueue,
        (msg) => {
          io.emit("kiwoom_kosdaq_b_stocks", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

      const kiwoomFuturesQueue = "kiwoom_futures_data";
      channel.assertQueue(kiwoomFuturesQueue, { durable: false });
      channel.consume(
        kiwoomFuturesQueue,
        (msg) => {
          io.emit("kiwoom_futures", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

    });

  });

});

// start server
http.listen(3001, () => {
  console.log("Connected at 3001");
});
