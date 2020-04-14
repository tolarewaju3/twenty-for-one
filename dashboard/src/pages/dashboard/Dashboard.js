import React, { Component } from 'react';
import {Link} from "react-router-dom";
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

import { Typography } from "../../components/Wrappers";


function withMyHook(Component) {
  return function Dashboard(props) {
    const myHookValue = useStyles();
    return <Component {...props} myHookValue={myHookValue} />;
  }
}

class Dashboard extends Component{

    constructor(props) {
      super(props);
      this.state = {deliveries: mock.table};
    }


    componentDidMount(){
      
      axios.get('https://us-central1-twenty-for-one.cloudfunctions.net/getDeliveries')
        .then(response => {
          if(response.data.length != 0){
            console.log(response.data);
            this.setState({ deliveries: response.data });
          }
        })
        .catch(function (error) {
          console.log(error);
        })

    }

    render(){
      const classes = this.props.myHookValue;
        return(
          <>
            <PageTitle title="Twenty for One"/>
          <Grid container spacing={4}>
          <Grid item xs={12}>
          <Widget
            title=""
            disableWidgetMenu
          >

          <Typography size="md" weight="medium">
                Twenty for One delivers $20 of free groceries to people at high risk of dying from COVID-19. We believe even <strong>one more death is too many</strong>. To help out, text "Hi" to 512-312-7461.
              </Typography>
            

          </Widget>
        </Grid>
        {mock.bigStat.map(stat => (
          <Grid item md={4} sm={6} xs={12} key={stat.product}>
            <BigStat {...stat} />
          </Grid>
        ))}
        <Grid item xs={12}>
          <Widget
            title="Live Stream"
            upperTitle
            noBodyPadding
            disableWidgetMenu
            bodyClass={classes.tableWidget}
          >
            <Table data={this.state.deliveries} />
          </Widget>
        </Grid>

        <Grid item xs={12}>
          <Typography weight="medium">
                <center>Contact Us @ help@twentyforone.com</center>
              </Typography>
          <Typography weight="sm">
                <center> <Link to="/privacy">Privacy Policy</Link> | <Link to="/terms">Terms of Service</Link></center>
              </Typography>
        </Grid>
      </Grid>
          </>

        )
    }


} 


export default withMyHook(Dashboard);



