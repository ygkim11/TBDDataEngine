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

      const exchange = 'kiwoom';
      channel.assertExchange(exchange, 'topic', { durable: false });
      channel.assertQueue('', { exclusive: true }, function(err2, q) {
        if (err2) {
          throw err2;
        }
        channel.bindQueue(q.queue, exchange, '#');
        channel.consume(q.queue, msg => {
          const [asset, type] = msg.fields.routingKey.split('.');
          producer.send([{
            topic: `kiwoom_${asset}`,
            key: type,
            message: [msg.content],
            attributes: 1,
          }], () => {});
        }, { noAck: true });
      }); // channel.assertQueue

    }); //connection.createChannel

  }); // amqp.connect
}); // producer.on
