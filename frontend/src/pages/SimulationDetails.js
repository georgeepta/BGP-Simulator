import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import { useHistory } from 'react-router';
import '../App.css';
import './SimulationDetails.css';

function SimulationDetails() {
    
    const [data, setData] = useState();
    const [isDataAvailable, setIsDataAvailable] = useState(false);
    const [simResults, setSimResults] = useState();
    const history = useHistory();
    const simulation_uuid = history.location.state.data;



    const columns = [
        {
          name: 'Repetition ID',
          selector: row => row.id,
          sortable: true,
        },
        {
            name: 'Legitimate AS',
            selector: row => row.legitimate_AS,
            sortable: true,
        },
        {
            name: 'Hijacker AS',
            selector: row => row.hijacker_AS,
            sortable: true,
        },
        {
            name: 'Helper ASes',
            selector: row => row.anycast_ASes,
            sortable: true,
        },
        {
            name: 'Impact Estimation (After Hijack)',
            selector: row => row.after_hijack.impact_estimation,
            sortable: true,
        },
        {
            name: 'Impact Estimation (After Mitigation)',
            selector: row => row.after_mitigation.impact_estimation,
            sortable: true,
        },
        {
            cell:(row) => <button id={row.id} className="btn">More Details</button>,
            ignoreRowClick: true,
            allowOverflow: true,
            button: true
        },
    ]

  
    
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
                setSimResults(data.simulation_results)
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
                            <th>Simulation Status:</th>
                            {isDataAvailable && <td>{data.simulation_status}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>Completed Simulations:</th>
                            {isDataAvailable && <td>{(data.num_of_finished_simulations).toString() + '/' + (data.num_of_simulations * data.num_of_repetitions).toString()}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>Start Time:</th>
                            {isDataAvailable && <td>{data.sim_start_time}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>End Time:</th>
                            {isDataAvailable && <td>{data.sim_end_time}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                    </tbody>
                </table>
                <table className='table-striped'>
                    <tbody>
                        <tr>
                            <th>Hijack Type:</th>
                            {isDataAvailable && <td>{data.simulation_data.hijack_type}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>Hijack Prefix Type:</th>
                            {isDataAvailable && <td>{data.simulation_data.hijack_prefix_type}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>Realistic RPKI ROV:</th>
                            {isDataAvailable && <td>{data.simulation_data.realistic_rpki_rov ? "Enabled" : "Disabled"}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>RPKI ROV Mode:</th>
                            {isDataAvailable && <td>{data.simulation_data.rpki_rov_mode}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                        <tr>
                            <th>#Anycast ASes:</th>
                            {isDataAvailable && <td>{data.simulation_data.max_nb_anycast_ASes}</td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>
                    </tbody>
                </table>
            </div>

            <DataTable 
                title="Results per Repetition"
                columns={columns}
                data={simResults}
                highlightOnHover
                selectableRows
                pagination
            />

        </div>
  );
}

export default SimulationDetails;