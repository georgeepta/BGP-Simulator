import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import '../App.css';
import './RandomSimulation.css'


function RandomSimulation() {
  

  const [HijackPrefixType, setHijackPrefixType] = useState('exact');
  const [HijackType, setHijackType] = useState(0);
  const [NumOfAnycastASes, setNumOfAnycastASes] = useState(0);
  const [RealisticROV, setRealisticROV] = useState("false");
  const [RovMode, setRovMode] = useState('all');
  const [NumOfSim, setNumOfSim] = useState(1);
  const [NumOfSimReps, setNumOfSimReps] = useState(1);
  const [isPending, setIsPending] = useState(false);
  const history = useHistory();

  const [errorMessage, setMessage] = useState(false);
  const [errorText, setErrorText] = useState('');


  const handleSubmit = (e) => {
      e.preventDefault();
      const sim_data = {
          "simulation_type": "random",
          "legitimate_AS": 0,
          "legitimate_prefix": "x.y.z.w/m",
          "hijacker_AS": 0,
          "hijacker_prefix": "x.y.z.w/m",
          "hijack_type": HijackType,
          "hijack_prefix_type": HijackPrefixType,
          "anycast_ASes": [0],
          "mitigation_prefix": "x.y.z.w/m",
          "realistic_rpki_rov": (RealisticROV === "true"),
          "rpki_rov_mode": RovMode,
          "nb_of_sims": NumOfSim,
          "nb_of_reps": NumOfSimReps,
          "caida_as_graph_dataset": "20211001",
          "caida_ixps_datasets": "202107",
          "max_nb_anycast_ASes": NumOfAnycastASes
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

          setIsPending(false);
      });

  }


  return (
      <div className='random-simulation'>
          <h2 className='h2'>Random Simulation Data</h2>
          <form onSubmit={handleSubmit}>
              <label>Hijack Prefix Type:</label>
              <select value={HijackPrefixType} onChange={(e) => setHijackPrefixType(e.target.value)}>
                  <option value="exact">Exact-Prefix Attack</option>
              </select>
              <label>Hijack Type:</label>
              <input type="number" min="0" value={HijackType} onChange={(e) => setHijackType(e.target.value)} required />
              <label>Number of Anycast ASes:</label>
              <input type="number" min="0" value={NumOfAnycastASes} onChange={(e) => setNumOfAnycastASes(e.target.value)} required />
              <label>Realistic RPKI ROV:</label>
              <select value={RealisticROV} onChange={(e) => setRealisticROV(e.target.value)}>
                  <option value="false">No</option>
              </select>
              <label>Which ASes deploy ROV?:</label>
              <select value={RovMode} onChange={(e) => setRovMode(e.target.value)}>
                  <option value="all">All</option>
                  <option value="random_20">Random 20%</option>
              </select>
              <label>Number of Random Simulations:</label>
              <input type="number" min="1" max="100" value={NumOfSim} onChange={(e) => setNumOfSim(e.target.value)} required />
              <label>Repetitions per Simulation:</label>
              <input type="number" min="1" max="100" value={NumOfSimReps} onChange={(e) => setNumOfSimReps(e.target.value)} required />
              {errorMessage && <p style={{color: "red", fontSize: "small"}}>{errorText}</p>}
              {!isPending && <button>Launch Simulation</button>}
              {isPending && <button disabled>Send Simulation Data...</button>}
          </form>
      </div>
  );


}

export default RandomSimulation;