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

      const upbitQueue = "upbit_data";
      channel.assertQueue(upbitQueue, { durable: false });
      channel.consume(
        upbitQueue,
        (msg) => {
          io.emit("upbit", { data: msg.content });
        },
        {
          noAck: true,
        }
      );

    });

  });

});

// start server
http.listen(3000, () => {
  console.log("Connected at 3000");
});
