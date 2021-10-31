import React from "react";
import '../App.css';
import uoc_logo from '../images/UoC_logo.png'
import forth_logo from '../images/FORTH-ICS-logo.png';
import inspire_logo from '../images/inspire-logo.jpeg';



const Footer = () => (
  <div className="footer">
    <div className="row">
      <div style={{width: "100%", marginTop: "20px"}}>
        <a href="https://www.csd.uoc.gr/CSD/index.jsp?lang=en" target="_blank" rel="noreferrer noopener">
          <img src={uoc_logo} alt="UOC logo" style={{width:"60px", height:"60px"}}></img>
        </a>
        <a href="https://www.ics.forth.gr/" target="_blank" rel="noreferrer noopener">
          <img src={forth_logo} alt="FORTH logo" style={{width:"120px", height:"50px", marginLeft: "10px"}}></img>
        </a>
        <a href="https://www.inspire.edu.gr/" target="_blank" rel="noreferrer noopener">
          <img src={inspire_logo} alt="INSPIRE logo" style={{width:"60px", height:"60px", marginLeft: "15px", borderRadius: "3px"}}></img>
        </a>
      </div>
      <div style={{width: "100%", marginTop: "60px", textAlign: "center"}}>
        <small>Copyright &copy; {new Date().getFullYear()}, CSD UoC - INSPIRE Group (FORTH)</small>
      </div>
      <div style={{width: "100%", textAlign: "center"}}>
        <p>Developed by George Eptaminitakis</p>
        <a href="https://www.linkedin.com/in/george-eptaminitakis-5702ab1ba/" target="_blank" rel="noreferrer noopener">
          <i className="fab fa-linkedin fa-2x"></i>
        </a>
        <a href="https://github.com/georgeepta/" target="_blank" rel="noreferrer noopener">
          <i className="fab fa-github fa-2x"></i>
        </a>
      </div>
    </div>
  </div>
);

export default Footer;