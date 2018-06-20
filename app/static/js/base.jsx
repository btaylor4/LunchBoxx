import React from "react";

export default class Base extends React.Component {
  render() {
    return (
		<header className="bg-primary text-white ">
	      <div className="container text-center">
	        <h1>LunchBoxx</h1>
	        <p className="lead">Our Snazzy tagline for LunchBoxx</p>
	      </div>
	    </header>
    );
  }
}
