import NavBar from "./nav";
import React from "react";

export default class Portal extends React.Component {
  render() {
    return (
      <div>
        <NavBar />
        <div className="jumbotron vertical-center">
          <div className="container text-center">
            <button
              className="btn btn-primary btn-lg"
              href="/preferences"
              type="button"
            >
              MATCH ME
            </button>
          </div>
        </div>
      </div>
    );
  }
}
