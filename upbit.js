const WebSocket = require('ws');
const amqp = require("amqplib/callback_api");

const dotenv = require("dotenv");

dotenv.config()

const { RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD } = process.env;

// RabbitMQ client
amqp.connect(`amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:5672//`, function (err0, connection) {
  if (err0) {
    throw err0;
  }

  const kiwoom_queue = 'upbit_data';
  connection.createChannel((err1, channel) => {
      channel.assertQueue(kiwoom_queue, { durable: false });
      
      const ws = new WebSocket('wss://api.upbit.com/websocket/v1');

      ws.onopen = (event) => {
          const sendData = '[{"ticket":"test"},{"type":"trade","codes":["KRW-BTC","KRW-ETH"]}]';
          ws.send(sendData);
      };
      
      ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          channel.sendToQueue(kiwoom_queue, event.data);
      };
  });
});