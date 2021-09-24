import React, { useState } from 'react';
import '../App.css';
import './CustomSimulation.css';


function CustomSimulation() {

    const [HijackPrefixType, setHijackPrefixType] = useState('exact');
    const [HijackType, setHijackType] = useState(0);
    const [VictimASN, setVictimASN] = useState('');
    const [VictimPrefix, setVictimPrefix] = useState('');
    const [HijackerASN, setHijackerASN] = useState('');
    const [HijackerPrefix, setHijackerPrefix] = useState('');
    const [AnycastASes, setAnycastASes] = useState('');
    const [MitigationPrefix, setMitigationPrefix] = useState('');
    const [RealisticROV, setRealisticROV] = useState(true);
    const [RovMode, setRovMode] = useState('all');
    const [NumOfSimReps, setNumOfSimReps] = useState(1);

    const handleSubmit = (e) => {
        e.preventDefault();
        const anycast_ASes_list = AnycastASes.split(',').map(item => parseInt(item));
        const sim_data = {
            "simulation_type": "custom",
            "legitimate_AS": parseInt(VictimASN),
            "legitimate_prefix": VictimPrefix,
            "hijacker_AS": parseInt(HijackerASN),
            "hijacker_prefix": HijackerPrefix,
            "hijack_type": HijackType,
            "hijack_prefix_type": HijackPrefixType,
            "anycast_ASes": anycast_ASes_list,
            "mitigation_prefix": MitigationPrefix,
            "realistic_rpki_rov": RealisticROV,
            "rpki_rov_mode": RovMode,
            "nb_of_sims": NumOfSimReps,
            "nb_of_reps": 1,
            "caida_as_graph_dataset": "20210301",
            "caida_ixps_datasets": "202104",
            "max_nb_anycast_ASes": anycast_ASes_list.length
        };

        fetch('http://127.0.0.1:5000/launch_simulation', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(sim_data)
        }).then(async response => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            const data = isJson && await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.status;
                return Promise.reject(error);
            }

            //Successful Request --> do some action
            console.log(data)

        }).catch(error => {
            console.error('There was an error!', error);
        });

    }
  
  
    return (
        <div className='custom-simulation'>
            <h2 className='h2'>Custom Simulation Data</h2>
            <form onSubmit={handleSubmit}>
                <label>Hijack Prefix Type:</label>
                <select value={HijackPrefixType} onChange={(e) => setHijackPrefixType(e.target.value)}>
                    <option value="exact">Exact-Prefix Attack</option>
                    <option value="subprefix">Sub-Prefix Attack</option>
                </select>
                <label>Hijack Type:</label>
                <input type="number" min="0" value={HijackType} onChange={(e) => setHijackType(e.target.value)} required />
                <label>Victim's ASN:</label>
                <input type="number" min="0" value={VictimASN} onChange={(e) => setVictimASN(e.target.value)} required />
                <label>Victim's Prefix:</label>
                <input type="text" value={VictimPrefix} onChange={(e) => setVictimPrefix(e.target.value)} required />
                <label>Hijacker's ASN:</label>
                <input type="number" min="0" value={HijackerASN} onChange={(e) => setHijackerASN(e.target.value)} required />
                <label>Hijacker's Prefix:</label>
                <input type="text" value={HijackerPrefix} onChange={(e) => setHijackerPrefix(e.target.value)} required />
                <label>Anycast ASes:</label>
                <input type="text" value={AnycastASes} onChange={(e) => setAnycastASes(e.target.value)} required />
                <label>Mitigation Prefix:</label>
                <input type="text" value={MitigationPrefix} onChange={(e) => setMitigationPrefix(e.target.value)} required />
                <label>Realistic RPKI ROV:</label>
                <select value={RealisticROV} onChange={(e) => setRealisticROV(e.target.value)}>
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
                <label>Which ASes deploy ROV?:</label>
                <select value={RovMode} onChange={(e) => setRovMode(e.target.value)}>
                    <option value="all">All</option>
                    <option value="random_20">Random 20%</option>
                </select>
                <label>Number of Simulation Repetitions:</label>
                <input type="number" min="1" value={NumOfSimReps} onChange={(e) => setNumOfSimReps(e.target.value)} required />
                <button>Launch Simulation</button>
            </form>
        </div>
    );
}

export default CustomSimulation;