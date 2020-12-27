const WebSocket = require('ws');
const amqp = require("amqplib/callback_api");

const dotenv = require("dotenv");

dotenv.config()

const { RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD } = process.env;

const coinInfoObj = {
    code: null,
    date: null,
    time: null,
    my_timestamp: null,
    timestamp: null,
    trade_timestamp: null,
    trade_price: null,
    trade_volume: null,

    hoga_timestamp: null,
    total_ask_size: null,
    total_bid_size: null,

    sell_hoga15: null,
    sell_hoga14: null,
    sell_hoga13: null,
    sell_hoga12: null,
    sell_hoga11: null,
    sell_hoga10: null,
    sell_hoga9: null,
    sell_hoga8: null,
    sell_hoga7: null,
    sell_hoga6: null,
    sell_hoga5: null,
    sell_hoga4: null,
    sell_hoga3: null,
    sell_hoga2: null,
    sell_hoga1: null,

    buy_hoga1: null,
    buy_hoga2: null,
    buy_hoga3: null,
    buy_hoga4: null,
    buy_hoga5: null,
    buy_hoga6: null,
    buy_hoga7: null,
    buy_hoga8: null,
    buy_hoga9: null,
    buy_hoga10: null,
    buy_hoga11: null,
    buy_hoga12: null,
    buy_hoga13: null,
    buy_hoga14: null,
    buy_hoga15: null,

    sell_hoga15_stack: null,
    sell_hoga14_stack: null,
    sell_hoga13_stack: null,
    sell_hoga12_stack: null,
    sell_hoga11_stack: null,
    sell_hoga10_stack: null,
    sell_hoga9_stack: null,
    sell_hoga8_stack: null,
    sell_hoga7_stack: null,
    sell_hoga6_stack: null,
    sell_hoga5_stack: null,
    sell_hoga4_stack: null,
    sell_hoga3_stack: null,
    sell_hoga2_stack: null,
    sell_hoga1_stack: null,

    buy_hoga1_stack: null,
    buy_hoga2_stack: null,
    buy_hoga3_stack: null,
    buy_hoga4_stack: null,
    buy_hoga5_stack: null,
    buy_hoga6_stack: null,
    buy_hoga7_stack: null,
    buy_hoga8_stack: null,
    buy_hoga9_stack: null,
    buy_hoga10_stack: null,
    buy_hoga11_stack: null,
    buy_hoga12_stack: null,
    buy_hoga13_stack: null,
    buy_hoga14_stack: null,
    buy_hoga15_stack: null
};

const supportingCoins = [
  'BTC',
  'ETH',
  'XRP',
  'LTC',
  'BCH',
  'ADA',
  'DOT',
  'LINK',
  'XLM',
  'BSV',
  'EOS',
  'XEM',
  'TRX'
]
const supportingCoinsStr = supportingCoins.map(coin => `"KRW-${coin}"`).join(',');

const coinsInfo = {};
for (let coin of supportingCoins) {
  coinsInfo[`KRW-${coin}`] = coinInfoObj;
}

// RabbitMQ client
amqp.connect(`amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@${RABBITMQ_HOST}:12765//`, function (err0, connection) {
  if (err0) {
    throw err0;
  }

  const upbit_queue = 'upbit_data';
  connection.createChannel((err1, channel) => {
      channel.assertQueue(upbit_queue, { durable: false });
      
      const ws = new WebSocket('wss://api.upbit.com/websocket/v1');

      ws.onopen = (event) => {
          const sendData = `
          [
            {"ticket":"test"},
            {"type":"trade","codes":[${supportingCoinsStr}]},
            {"type":"orderbook","codes":[${supportingCoinsStr}]}
          ]
          `;
          ws.send(sendData);
      };
      
      ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.type == 'trade') {
            coinsInfo[data.code] = {
              ...coinsInfo[data.code],
              code: data.code,
              date: data.trade_date,
              time: data.trade_time,
              my_timestamp: Date.now(),
              timestamp: data.timestamp,
              trade_timestamp: data.trade_timestamp,
              trade_price: data.trade_price,
              trade_volume: data.trade_volume
            };
          }
          else if (data.type == 'orderbook') {
            coinsInfo[data.code] = {
              ...coinsInfo[data.code],
              my_timestamp: Date.now(),
              hoga_timestamp: data.timestamp,
              total_ask_size: data.total_ask_size,
              total_bid_size: data.total_bid_size
            };

            const orderbook = data.orderbook_units;
            for (let i = 0; i < orderbook.length; i++) {
              coinsInfo[data.code][`sell_hoga${i+1}`] = orderbook[i].ask_price;
              coinsInfo[data.code][`buy_hoga${i+1}`] = orderbook[i].bid_price;
              coinsInfo[data.code][`sell_hoga${i+1}_stack`] = orderbook[i].ask_size;
              coinsInfo[data.code][`buy_hoga${i+1}_stack`] = orderbook[i].bid_size;
            }
          }
          channel.sendToQueue(upbit_queue, Buffer.from(JSON.stringify(coinsInfo[data.code])));
      };
  });
});