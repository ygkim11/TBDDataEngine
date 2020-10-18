const app = require("express")();
const http = require("http").createServer(app);
const io = require("socket.io")(http);
const amqp = require("amqplib/callback_api");

// express default index page rendering
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

// add more queues later
const getSendData = (connection) => {
  connection.createChannel((err1, channel) => {
    if (err1) {
      throw err1;
    }

    const kiwoom_queue = "kiwoom_data";
    channel.assertQueue(kiwoom_queue, { durable: false });
    channel.consume(
      kiwoom_queue,
      (msg) => {
        io.emit("data", { data: msg.content.toString() });
      },
      {
        noAck: true,
      }
    );
  });
};

// RabbitMQ client
amqp.connect("amqp://localhost", function (err0, connection) {
  if (err0) {
    throw err0;
  }

  // Socket.IO client
  io.on("connection", (socket) => {
    console.log("socket connected");

    socket.on("ready", (msg) => {
      console.log("socket is ready");
      getSendData(connection);
    });

    socket.on("order", (msg) => {
      console.log("socket order");
      console.log(msg);
    });

    socket.on("disconnect", () => {
      console.log("socket disconnected");
    });
  });
});

// start server
http.listen(3000, () => {
  console.log("Connected at 3000");
});
