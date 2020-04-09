import React from "react";
import {
  Grid
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import Table from "./components/Table/Table";
import BigStat from "./components/BigStat/BigStat";

// Datastore
const {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore();
const query = datastore.createQuery('Delivery');
var deliveries;

export default function Dashboard(props) {
  var classes = useStyles();

  return (
    <>
      <PageTitle title="Deliveries"/>
      <Grid container spacing={4}>
        {mock.bigStat.map(stat => (
          <Grid item md={4} sm={6} xs={12} key={stat.product}>
            <BigStat {...stat} />
          </Grid>
        ))}
        <Grid item xs={12}>
          <Widget
            title="Support Requests"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableWidget}
          >
            <Table data={deliveries} />
          </Widget>
        </Grid>
      </Grid>
    </>
  );
}

async function queryDb() {
  deliveries = await datastore.runQuery(query);
}
queryDb();
