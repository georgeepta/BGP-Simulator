import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import { useHistory } from 'react-router';
import '../App.css';
import './SimulationDetails.css';
import {ASInfo} from '../components/ASInfo';
import '../components/ASInfo.css';
import Popup from '../components/Popup';


function SimulationDetails() {
    
    const [data, setData] = useState();
    const [PopUpData, setPopUpData] = useState();
    const [isDataAvailable, setIsDataAvailable] = useState(false);
    const [simResults, setSimResults] = useState();
    const history = useHistory();
    const simulation_uuid = history.location.state.data;
    const [isOpen, setIsOpen] = useState(false);

    const togglePopup = () => {
        setIsOpen(!isOpen);
    }

    const setPopup = (id) => {
        data.simulation_results.forEach(element => {
            if(element["id"] === id) {
                setPopUpData(element);
                togglePopup();
                return;
            }
        });
    }


    const columns = [
        {
          name: 'Repetition ID',
          selector: row => row.id,
          sortable: true,
        },
        {
            name: 'Legitimate AS',
            cell: (row) => <ASInfo asn={row.legitimate_AS} asns_details_dict={data.asns_details} />,
            sortable: true,
        },
        {
            name: 'Hijacker AS',
            cell: (row) => <ASInfo asn={row.hijacker_AS} asns_details_dict={data.asns_details} />,
            sortable: true,
        },
        {
            name: 'Helper ASes',
            selector: row => row.anycast_ASes,
            sortable: true,
        },
        {
            name: 'Impact Estimation (After Hijack)',
            selector: row => parseFloat(row.after_hijack.impact_estimation * 100).toFixed(4) + '%',
            sortable: true,
            center: true,
            style: {
                borderRadius: '40px',
            },
            conditionalCellStyles: [
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) < 0.01,
                    style: {
                        background: 'rgba(69,223,73,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) > 0.01 && parseFloat(row.after_hijack.impact_estimation) < 0.10,
                    style: {
                        background: 'rgba(156,223,69,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) > 0.10 && parseFloat(row.after_hijack.impact_estimation) < 0.20,
                    style: {
                        background: 'rgba(223,199,69,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) > 0.20 && parseFloat(row.after_hijack.impact_estimation) < 0.40,
                    style: {
                        background: 'rgba(223,143,69,0.5536414394859506)',
                    }
                },
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) > 0.40 && parseFloat(row.after_hijack.impact_estimation) < 0.70,
                    style: {
                        background: 'rgba(223,86,69,0.5956582462086397)',
                    }
                },
                {
                    when: row => parseFloat(row.after_hijack.impact_estimation) > 0.70,
                    style: {
                        background: 'rgba(223,69,69,0.7833333162366509)',
                    }
                },
            ]
        },
        {
            name: 'Impact Estimation (After Mitigation)',
            selector: row => parseFloat(row.after_mitigation.impact_estimation * 100).toFixed(4) + '%',
            sortable: true,
            center: true,
            style: {
                borderRadius: '40px',
            },
            conditionalCellStyles: [
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) < 0.01,
                    style: {
                        background: 'rgba(69,223,73,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) > 0.01 && parseFloat(row.after_mitigation.impact_estimation) < 0.10,
                    style: {
                        background: 'rgba(156,223,69,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) > 0.10 && parseFloat(row.after_mitigation.impact_estimation) < 0.20,
                    style: {
                        background: 'rgba(223,199,69,0.13627449270723913)',
                    }
                },
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) > 0.20 && parseFloat(row.after_mitigation.impact_estimation) < 0.40,
                    style: {
                        background: 'rgba(223,143,69,0.5536414394859506)',
                    }
                },
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) > 0.40 && parseFloat(row.after_mitigation.impact_estimation) < 0.70,
                    style: {
                        background: 'rgba(223,86,69,0.5956582462086397)',
                    }
                },
                {
                    when: row => parseFloat(row.after_mitigation.impact_estimation) > 0.70,
                    style: {
                        background: 'rgba(223,69,69,0.7833333162366509)',
                    }
                },
            ]
        },
        {
            cell:(row) => <button id={row.id} className="btn" onClick={() => setPopup(row.id)}>More Details</button>,
            ignoreRowClick: true,
            allowOverflow: true,
            button: true,
        },
    ];
  
    
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
                        {isDataAvailable && data.simulation_data.simulation_type === "custom" && <tr>
                            <th>Legitimate AS Prefix:</th>
                            {isDataAvailable && <td className="asn-info">
                                <a href={"https://stat.ripe.net/" + data.simulation_data.legitimate_prefix + "#tabId=routing"} target="_blank" rel="noreferrer">
                                    {data.simulation_data.legitimate_prefix}
                                </a>
                                </td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>}
                        {isDataAvailable && data.simulation_data.simulation_type === "custom" && <tr>
                            <th>Hijacker AS Prefix:</th>
                            {isDataAvailable && <td className="asn-info">
                                <a href={"https://stat.ripe.net/" + data.simulation_data.hijacker_prefix + "#tabId=routing"} target="_blank" rel="noreferrer">
                                    {data.simulation_data.hijacker_prefix}
                                </a>
                                </td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>}
                        {isDataAvailable && data.simulation_data.simulation_type === "custom" && <tr>
                            <th>Mitigation Prefix:</th>
                            {isDataAvailable && <td className="asn-info">
                                <a href={"https://stat.ripe.net/" + data.simulation_data.mitigation_prefix + "#tabId=routing"} target="_blank" rel="noreferrer">
                                    {data.simulation_data.mitigation_prefix}
                                </a>
                                </td>}
                            {!isDataAvailable && <td>N/A</td>}
                        </tr>}
                    </tbody>
                </table>
            </div>
            <div className="data-table">
                <DataTable 
                    title="Results per Repetition"
                    columns={columns}
                    data={simResults}
                    progressPending={!isDataAvailable}
                    highlightOnHover
                    pagination
                />
            </div>
            {isOpen && <Popup rep_data={PopUpData} asns_details_dict={data.asns_details} handleClose={togglePopup} />}
        </div>
  );
}

export default SimulationDetails;