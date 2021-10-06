import React, { useEffect, useState } from 'react';
import './Popup.css';
import DataTable from 'react-data-table-component';
import ASPath from '../components/ASPath';
import {ASInfo} from '../components/ASInfo';
import Chart from "react-google-charts";




const Popup = props => {
    
  const [rpki_rov_table_data, setRpki_rov_table_data] = useState();
  const [infectedASes_AfterHijack, setInfectedASes_AfterHijack] = useState();
  const [isRenderAvailable, setIsRenderAvailable] = useState(false);



  const columns_infectedASes_AfterHijack = [
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

  const rpki_rov_table_columns = [
    {
      name: 'Origin AS',
      selector: row => row.asn,
      sortable: true,
    },
    {
      name: 'Prefix',
      selector: row => row.prefix,
      sortable: true,
    },
    {
      name: 'State',
      selector: row => row.state,
      sortable: true,
    },
  ]


  useEffect(() => {

    const infectedASes_AfterHijack = [];
    const rpki_rov_table_data = [];

    for (let asn in props.rep_data.rpki_rov_table) {
      for (let prefix in props.rep_data.rpki_rov_table[asn]){
        rpki_rov_table_data.push({"asn": asn, "prefix": prefix, "state": props.rep_data.rpki_rov_table[asn][prefix]})
      }
    }
    setRpki_rov_table_data(rpki_rov_table_data)
    
    
    for (let asn in props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix){
      infectedASes_AfterHijack.push({"asn": asn})
    }
    setInfectedASes_AfterHijack(infectedASes_AfterHijack)

    
    setIsRenderAvailable(true)
    
  }, [props]);

  
  return (
      <div className="popup-box">
        <div className="box">
          <span className="close-icon" onClick={props.handleClose}>x</span>
          <div className='row'> 
            <div>
              <h1>Overview</h1>
              <table className='table-striped'>
                <tbody>
                  <tr>
                      <th>Victim AS:</th>
                      <td><ASInfo asn={props.rep_data.legitimate_AS} asns_details_dict={props.asns_details_dict} /></td>
                  </tr>
                  <tr>
                      <th>Hijacker AS:</th>
                      <td><ASInfo asn={props.rep_data.hijacker_AS} asns_details_dict={props.asns_details_dict} /></td>
                  </tr>
                  <tr>
                      <th>Helper ASes:</th>
                      <td></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div style={{marginLeft: "50px"}}>
              <h1>RPKI ROV Table</h1>
              <DataTable 
                columns={rpki_rov_table_columns}
                data={rpki_rov_table_data}
              />
            </div>
            <div style={{marginLeft: "50px"}}>
              <h1>List of ASes that do ROV</h1>
              <DataTable 
                columns={rpki_rov_table_columns}
                data={rpki_rov_table_data}
              />
            </div>
          </div>
          <h1>Useful Statistics/Metrics</h1>
          <div className='row'>
            <Chart
              width={400}
              height={300}
              chartType="ColumnChart"
              loader={<div>Loading Chart</div>}
              data={[
                ['%', 'After Hijack', 'After Mitigation'],
                ['23443', 56, 23],
              ]}
              options={{
                title: 'Impact Estimation',
                chartArea: { width: '30%' },
                colors: ['#b0120a', '#ffab91'],
                hAxis: {
                  title: '# Route Collectors \n(Monitors)',
                  minValue: 0,
                  maxValue: 100
                },
                vAxis: {
                  title: '% Impact',
                },
              }}
              legendToggle
            />
          </div>
          <DataTable 
            title="Infected ASes and Paths"
            columns={columns_infectedASes_AfterHijack}
            data={infectedASes_AfterHijack}
            progressPending={!isRenderAvailable}
            highlightOnHover
            pagination
          />
        </div>
      </div>
    );
  };

export default Popup;