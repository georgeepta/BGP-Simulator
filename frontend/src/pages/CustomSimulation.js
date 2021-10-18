import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
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
    const [RealisticROV, setRealisticROV] = useState("true");
    const [RovMode, setRovMode] = useState('all');
    const [NumOfSimReps, setNumOfSimReps] = useState(1);
    const [isPending, setIsPending] = useState(false);
    const history = useHistory();

    const [errorMessage, setMessage] = useState(false);
    const [errorText, setErrorText] = useState('');
    const [errorMessageVictimASN, setMessageVictimASN] = useState(false);
    const [errorTextVictimASN, setErrorTextVictimASN] = useState('');
    const [errorMessageVictimPrefix, setMessageVictimPrefix] = useState(false);
    const [errorTextVictimPrefix, setErrorTextVictimPrefix] = useState('');
    const [errorMessageHijackerASN, setMessageHijackerASN] = useState(false);
    const [errorTextHijackerASN, setErrorTextHijackerASN] = useState('');
    const [errorMessageHijackerPrefix, setMessageHijackerPrefix] = useState(false);
    const [errorTextHijackerPrefix, setErrorTextHijackerPrefix] = useState('');
    const [errorMessageAnycastASes, setMessageAnycastASes] = useState(false);
    const [errorTextAnycastASes, setErrorTextAnycastASes] = useState('');
    const [errorMessageMitigationPrefix, setMessageMitigationPrefix] = useState(false);
    const [errorTextMitigationPrefix, setErrorTextMitigationPrefix] = useState('');


    const handleSubmit = (e) => {
        e.preventDefault();
        const anycast_ASes_list = AnycastASes.split(',').map(item => parseInt(item));
        const sim_data = {
            "simulation_type": "custom",
            "legitimate_AS": parseInt(VictimASN),
            "legitimate_prefix": VictimPrefix.replace(/\s+/g,""),
            "hijacker_AS": parseInt(HijackerASN),
            "hijacker_prefix": HijackerPrefix.replace(/\s+/g,""),
            "hijack_type": HijackType,
            "hijack_prefix_type": HijackPrefixType,
            "anycast_ASes": anycast_ASes_list,
            "mitigation_prefix": MitigationPrefix.replace(/\s+/g,""),
            "realistic_rpki_rov": (RealisticROV === "true"),
            "rpki_rov_mode": RovMode,
            "nb_of_sims": NumOfSimReps,
            "nb_of_reps": 1,
            "caida_as_graph_dataset": "20211001",
            "caida_ixps_datasets": "202107",
            "max_nb_anycast_ASes": anycast_ASes_list.length
        };

        setIsPending(true);

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
                console.log(data)
                const error = data || response.status;
                throw error;
                /*return Promise.reject(error);*/
            }

            //Successful Request --> do some action
            console.log(data)
            setIsPending(false);
            history.push('/simulation-events');

        }).catch(error => {
            console.error('There was an error!', error.message);
            
            
            if (error.message){
                setMessage(true);
                setErrorText(error.message);
            }else{
                setMessage(false);
                setErrorText("");
            }

            if (error.legitimate_AS !== ""){
                setMessageVictimASN(true);
                setErrorTextVictimASN(error.legitimate_AS);
            }else{
                setMessageVictimASN(false);
                setErrorTextVictimASN("");
            }
            if (error.legitimate_prefix !== ""){
                setMessageVictimPrefix(true);
                setErrorTextVictimPrefix(error.legitimate_prefix);
            }else{
                setMessageVictimPrefix(false);
                setErrorTextVictimPrefix("");
            }

            if (error.hijacker_AS !== ""){
                setMessageHijackerASN(true);
                setErrorTextHijackerASN(error.hijacker_AS);
            }else{
                setMessageHijackerASN(false);
                setErrorTextHijackerASN("");
            }
            if (error.hijacker_prefix !== ""){
                setMessageHijackerPrefix(true);
                setErrorTextHijackerPrefix(error.hijacker_prefix);
            }else{
                setMessageHijackerPrefix(false);
                setErrorTextHijackerPrefix("");
            }

            if (error.anycast_ASes !== ""){
                setMessageAnycastASes(true);
                setErrorTextAnycastASes(error.anycast_ASes);
            }else{
                setMessageAnycastASes(false);
                setErrorTextAnycastASes("");
            }
            if (error.mitigation_prefix !== ""){
                setMessageMitigationPrefix(true);
                setErrorTextMitigationPrefix(error.mitigation_prefix);
            }else{
                setMessageMitigationPrefix(false);
                setErrorTextMitigationPrefix("");
            }

            setIsPending(false);
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
                {errorMessageVictimASN && <p style={{color: "red", fontSize: "small"}}>{errorTextVictimASN}</p>}
                <input type="number" min="0" value={VictimASN} onChange={(e) => setVictimASN(e.target.value)} required />
                <label>Victim's Prefix:</label>
                {errorMessageVictimPrefix && <p style={{color: "red", fontSize: "small"}}>{errorTextVictimPrefix}</p>}
                <input type="text" value={VictimPrefix} onChange={(e) => setVictimPrefix(e.target.value)} required />
                <label>Hijacker's ASN:</label>
                {errorMessageHijackerASN && <p style={{color: "red", fontSize: "small"}}>{errorTextHijackerASN}</p>}
                <input type="number" min="0" value={HijackerASN} onChange={(e) => setHijackerASN(e.target.value)} required />
                <label>Hijacker's Prefix:</label>
                {errorMessageHijackerPrefix && <p style={{color: "red", fontSize: "small"}}>{errorTextHijackerPrefix}</p>}
                <input type="text" value={HijackerPrefix} onChange={(e) => setHijackerPrefix(e.target.value)} required />
                <label>Anycast ASes:</label>
                {errorMessageAnycastASes && <p style={{color: "red", fontSize: "small"}}>{errorTextAnycastASes}</p>}
                <input type="text" value={AnycastASes} onChange={(e) => setAnycastASes(e.target.value)} required />
                <label>Mitigation Prefix:</label>
                {errorMessageMitigationPrefix && <p style={{color: "red", fontSize: "small"}}>{errorTextMitigationPrefix}</p>}
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
                <input type="number" min="1" max="100" value={NumOfSimReps} onChange={(e) => setNumOfSimReps(e.target.value)} required />
                {errorMessage && <p style={{color: "red", fontSize: "small"}}>{errorText}</p>}
                {!isPending && <button>Launch Simulation</button>}
                {isPending && <button disabled>Send Simulation Data...</button>}
            </form>
        </div>
    );
}

export default CustomSimulation;