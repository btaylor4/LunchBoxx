// imports
import React from "react";
import ReactDOM from "react-dom";

export default class NavBar extends React.Component {
  render() {
    const username = window.localStorage.getItem("username");
    const loggedIn = username != null && username != "" ? true : false;

    return (
      <nav className="navbar navbar-expand-sm navbar-light bg-light">
        <a className="navbar-brand" href="/">
          LunchBoxx
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              <a className="nav-link" href="/edit_profile">
                Edit Profile
              </a>
            </li>
          </ul>
        </div>
      </nav>
    );
  }
}
