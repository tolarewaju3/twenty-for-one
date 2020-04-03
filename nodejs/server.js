'use strict';

const express = require('express');
const {Datastore} = require('@google-cloud/datastore');

// Creates a client
const datastore = new Datastore();

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

var output = "";
const query = datastore.createQuery('Delivery');

// App
const app = express();
app.get('/', (req, res) => {
  queryDb(res)
});

async function queryDb(response) {
  const [deliveries] = await datastore.runQuery(query);
  deliveries.forEach(delivery => {
    output = output + delivery['helperName'] + " delivered for " + delivery['olderAdult']
  });

  response.send(output);
}

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);



