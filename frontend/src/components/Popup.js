import React from "react";
import './Popup.css';

const Popup = props => {
    return (
      <div className="popup-box">
        <div className="box">
          <span className="close-icon" onClick={props.handleClose}>x</span>
          <h1>Before Hijack</h1>
          {props.rep_data.hijacker_AS}
        </div>
      </div>
    );
  };

export default Popup;