import React from 'react';
import { useHistory } from 'react-router';
import '../App.css';
import './SimulationDetails.css';

function SimulationDetails() {
    
    const history = useHistory();
    const simulation_uuid = history.location.state.data;
  
    return (
        <div className='simulation-details'>
            <h1>Simulation Details</h1>
            <p>{simulation_uuid}</p>
            <div className='row'>
                <table className='table-striped'>
                    <tbody>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                    </tbody>
                </table>
                <table className='table-striped'>
                    <tbody>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
  );
}

export default SimulationDetails;