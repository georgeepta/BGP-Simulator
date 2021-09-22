import React from 'react';
import '../App.css';
import './CustomSimulation.css';


function CustomSimulation() {
  return (
    <div className='custom-simulation'>
        <h2 className='h2'>Custom Simulation Data</h2>
        <form>
            <label>Hijack Prefix Type:</label>
            <select>
                <option value="exact">Exact-Prefix Attack</option>
                <option value="subprefix">Sub-Prefix Attack</option>
            </select>
            <label>Hijack Type:</label>
            <input type="number" required />
            <label>Victim's ASN:</label>
            <input type="number" required />
            <label>Victim's Prefix:</label>
            <input type="text" required />
            <label>Hijacker's ASN:</label>
            <input type="number" required />
            <label>Hijacker's Prefix:</label>
            <input type="text" required />
            <label>Anycast ASes:</label>
            <input type="text" required />
            <label>Mitigation Prefix:</label>
            <input type="text" required />
            <label>Realistic RPKI ROV:</label>
            <select>
                <option value="real-rpki-rov">Yes</option>
                <option value="hypo-rpki-rov">No</option>
            </select>
            <label>Which ASes deploy ROV?:</label>
            <select>
                <option value="rov-mode-all">All</option>
                <option value="rov-mode-20">Random 20%</option>
            </select>
            <label>Number of Simulation Repetitions:</label>
            <input type="number" required />
            <button>Launch Simulation</button>
        </form>
    </div>
  );
}

export default CustomSimulation;