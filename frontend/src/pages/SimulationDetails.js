import React from 'react';
import { useHistory } from 'react-router';
import '../App.css';

function SimulationDetails() {
    
    const history = useHistory();
    const simulation_uuid = history.location.state.data;
  
    return (
        <div className='simulation-details'>
            <h1>Simulation Details</h1>
            <p>{simulation_uuid}</p>
        </div>
  );
}

export default SimulationDetails;