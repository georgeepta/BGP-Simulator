import React from 'react';
import '../App.css';
import { Button } from '../components/Button';


export default function NewSimulation() {
  return (
    <div className='new-simulation'>
        <div className='simulation-type'>
          <h1 className='h1'>Select Simulation Type</h1>
          <div className="line-break"></div>
          <Button 
            type="primary"
            pagelink="./custom-simulation" 
            btnname="Custom Simulation" 
          />
          <Button 
            type="primary"
            pagelink="./random-simulation" 
            btnname="Random Simulation" 
          />
        </div>
      </div>
  );
}