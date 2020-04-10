import React from "react";
import {
  Grid
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// axios
import axios from 'axios';

// components
import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import Table from "./components/Table/Table";
import BigStat from "./components/BigStat/BigStat";

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
            <Table data={mock.table} />
          </Widget>
        </Grid>
      </Grid>
    </>
  );
}

function getDeliveries(){
  axios.get(`https://us-central1-twenty-for-one.cloudfunctions.net/getDeliveries`)
      .then(res => {
        //const persons = res.data;
        //this.setState({ persons });
        console.log(res.data)
      })
}

getDeliveries()
