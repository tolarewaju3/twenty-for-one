import React, { Component } from 'react';
import ReactDOM from 'react-dom'
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

class Dashboard extends Component{
    constructor(props) {
      super(props);
      this.state = {deliveries: mock.table};
    }



    componentDidMount(){
      
      axios.get('https://us-central1-twenty-for-one.cloudfunctions.net/getDeliveries')
        .then(response => {
          this.setState({ deliveries: response.data });
        })
        .catch(function (error) {
          console.log(error);
        })

    }

    render(){
        return(
          <>
              <PageTitle title="Twenty for One"/>
              <Grid container spacing={4}>
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
          >
            <Table data={this.state.deliveries} />
          </Widget>
        </Grid>
      </Grid>
          </>

        )
    }


} 


export default Dashboard;



