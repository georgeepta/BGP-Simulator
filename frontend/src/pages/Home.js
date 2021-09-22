import React from 'react';
import '../App.css';
import { Button } from '../components/Button';
import backgroundH from "../images/bg_graph.gif";


export default function Home() {
  return (
    <div className="bk_Img"
      style={{
        backgroundImage: "url(" + backgroundH + ")",
        backgroundSize: "cover",
        height: "100vh",
      }}
    >
      <div className='home'>
        <div className='home-launch'>
          <h1 className='h1'>Launch a New Simulation now!</h1>
          <div className="line-break"></div>
          <Button 
            type="success"
            pagelink="./new-simulation" 
            btnname="Start" 
          />
        </div>
      </div>
    </div>
  );
}