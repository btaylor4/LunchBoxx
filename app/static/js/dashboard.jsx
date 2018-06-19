import NavBar from "./nav";
import React from "react";

export default class Portal extends React.Component {
  render() {
    return (
      <div>
        <NavBar />
        <div className="jumbotron vertical-center">
          <div className="container text-center">
            <a
              className="btn btn-primary btn-lg"
              href="/preferences"
              role="button"
            >
              MATCH ME
            </a>
          </div>
        </div>
      </div>
    );
  }
}
