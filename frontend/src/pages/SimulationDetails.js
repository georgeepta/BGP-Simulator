import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import '../App.css';
import './SimulationDetails.css';

function SimulationDetails() {
    
    const [data, setData] = useState();
    const [isDataAvailable, setIsDataAvailable] = useState(false);
    const history = useHistory();
    const simulation_uuid = history.location.state.data;
  
    
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/simulation_details?simulation_uuid=${encodeURIComponent(simulation_uuid)}`, {
                method: 'GET', 
            }).then(async response => {
                const isJson = response.headers.get('content-type')?.includes('application/json');
                const data = isJson && await response.json();
    
                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response status
                    console.log(data);
                    const error = data || response.status;
                    throw error;
                    /*return Promise.reject(error);*/
                }
    
                //Successful Request --> do some action
                console.log(data);
                setData(data);
                setIsDataAvailable(true);
            }).catch(error => {
              console.error('There was an error!', error.message);
            });
      }, [simulation_uuid]);

    
    return (
        <div className='simulation-details'>
            <h1>Simulation Details</h1>
            <div className='row'>
                <table className='table-striped'>
                    <tbody>
                        <tr>
                            <th>Simulation ID:</th>
                            <td>{simulation_uuid}</td>
                        </tr>
                        <tr>
                            <th>Simulation Type:</th>
                            {isDataAvailable && <td>{data.simulation_data.simulation_type}</td>}
                            {!isDataAvailable && <td>N/A</td>}
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