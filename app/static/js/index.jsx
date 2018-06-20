import React from "react";
import ReactDom from "react-dom";
import { BrowserRouter, browserHistory, Route, Switch } from "react-router-dom";
import Dashboard from "./dashboard";

ReactDom.render(
  <BrowserRouter>
    <Switch>
      <Route path="/user-portal" component={Dashboard}/>
    </Switch>
  </BrowserRouter>,
  document.getElementById("app")
);
