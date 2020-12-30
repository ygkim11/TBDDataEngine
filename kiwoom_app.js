const amqp = require("amqplib/callback_api");
const kafka = require("kafka-node");
const dotenv = require("dotenv");

dotenv.config()

const {
  RABBITMQ_HOST,
  RABBITMQ_PORT,
  RABBITMQ_USER,
  RABBITMQ_PASSWORD
} = process.env;

const Producer = kafka.Producer;
const client = new kafka.KafkaClient({kafkaHost: 'localhost:9092'});
const producer = new Producer(client);

const rabbitUri = `amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:${RABBITMQ_PORT}//`;

producer.on('ready', function () {
  // RabbitMQ client
  amqp.connect(rabbitUri, function (err0, connection) {
    if (err0) {
      throw err0;
    }

    connection.createChannel((err1, channel) => {
      if (err1) {
          throw err1;
      }

      const kiwoomStocksTradeQueue = "kiwoom_stocks_trade_data";
      channel.assertQueue(kiwoomStocksTradeQueue, { durable: false });
      channel.consume(
        kiwoomStocksTradeQueue,
          (msg) => {
              producer.send([{
                topic: 'kiwoom_stocks',
                key: 'trade',
                messages: [msg.content],
                attributes: 1
              }], () => {});
          },
          {
            noAck: true,
          }
      );

      const kiwoomFuturesTradeQueue = "kiwoom_futures_trade_data";
      channel.assertQueue(kiwoomFuturesTradeQueue, { durable: false });
      channel.consume(
        kiwoomFuturesTradeQueue,
          (msg) => {
              producer.send([{
                topic: 'kiwoom_futures',
                key: 'trade',
                messages: [msg.content],
                attributes: 1
              }], () => {});
          },
          {
            noAck: true,
          }
      );

      const kiwoomStocksOrderbookQueue = "kiwoom_stocks_orderbook_data";
      channel.assertQueue(kiwoomStocksOrderbookQueue, { durable: false });
      channel.consume(
        kiwoomStocksOrderbookQueue,
          (msg) => {
              producer.send([{
                topic: 'kiwoom_stocks',
                key: 'orderbook',
                messages: [msg.content],
                attributes: 1
              }], () => {});
          },
          {
            noAck: true,
          }
      );

      const kiwoomFuturesOrderbookQueue = "kiwoom_futures_orderbook_data";
      channel.assertQueue(kiwoomFuturesOrderbookQueue, { durable: false });
      channel.consume(
        kiwoomFuturesOrderbookQueue,
          (msg) => {
              producer.send([{
                topic: 'kiwoom_futures',
                key: 'orderbook',
                messages: [msg.content],
                attributes: 1
              }], () => {});
          },
          {
            noAck: true,
          }
      );

    });

  });
});
