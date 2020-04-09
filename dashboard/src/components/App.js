import React from "react";
import { HashRouter, Route, Switch, Redirect } from "react-router-dom";

// components
import Layout from "./Layout";


// context


export default function App() {

  return (
    <HashRouter>
      <div>
        <Switch>
            <Route exact path="/" render={() => <Redirect to="/app/dashboard" />} />
            <Route path="/app/dashboard" component={Layout} />
        </Switch>
      </div>
    </HashRouter>
    )
 
}
