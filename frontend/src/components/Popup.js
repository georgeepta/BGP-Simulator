import React, { useEffect, useState } from 'react';
import './Popup.css';
import DataTable from 'react-data-table-component';
import ASPath from '../components/ASPath';



const Popup = props => {
    
  
  const [infectedASes, setInfectedASes] = useState();
  const [isRenderAvailable, setIsRenderAvailable] = useState(false);



  const columns = [
    {
      name: 'Infected AS',
      selector: row => row.asn,
      sortable: true,
    },
    {
      name: 'Infected AS_PATH',
      cell: (row) => <ASPath asn={row.asn} as_path={props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix[row.asn]}/>,
    },
  ]


  useEffect(() => {

    const infectedASes = [];
    for (let asn in props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix){
      infectedASes.push({"asn": asn})
    }
    setInfectedASes(infectedASes)
    setIsRenderAvailable(true)
    
  }, [props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix]);

  
  return (
      <div className="popup-box">
        <div className="box">
          <span className="close-icon" onClick={props.handleClose}>x</span>
          <h1>Before Hijack</h1>
          <p>Number of nodes with hijacked path to hijacker prefix: {props.rep_data.after_hijack.nb_of_nodes_with_hijacked_path_to_hijacker_prefix}</p>
          <DataTable 
            title="Infected ASes and Paths"
            columns={columns}
            data={infectedASes}
            progressPending={!isRenderAvailable}
            highlightOnHover
            pagination
          />
        </div>
      </div>
    );
  };

export default Popup;