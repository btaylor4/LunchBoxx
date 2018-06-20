import React from "react";
import Base from "./base"

export default class Dashboard extends React.Component {
  render() {
    return (
    <div className="container" >
	  	<Base />

		<div className="row">
	        <div className="col-md-6 col-sm-6">
				<div>
	            	<h3> Profile Details </h3>
					words words words
				</div>
	        </div>
	        <div className="col-md-6 col-sm-6">
				<div>
					<h3> Actions </h3>
					<a className="btn btn-primary btn-lg" href="/preferences" role="button"> MATCH ME</a>

				</div>


	        </div>
	    </div>

	</div>
    );
  }
}
