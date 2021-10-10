import React, { useEffect, useState } from 'react';
import './Popup.css';
import InfectedPathsTable from './InfectedPathsTable';
import ASPath from '../components/ASPath';
import {ASInfo} from '../components/ASInfo';
import Chart from "react-google-charts";
import DataTable from 'react-data-table-component';
import ASesRovTable from './ASesRovTable';




const Popup = (props) => {
    
  const [rpki_rov_table_data, setRpki_rov_table_data] = useState();
  const [ASes_that_do_ROV, setASes_that_do_ROV] = useState();
  const [infectedASes_AfterHijack, setInfectedASes_AfterHijack] = useState();
  const [infectedASes_AfterMitigation, setInfectedASes_AfterMitigation] = useState();
  const [isRenderAvailable, setIsRenderAvailable] = useState(false);



  const columns_infectedASes_AfterHijack = [
    {
      name: 'Infected AS',
      selector: row => <ASInfo asn={row.asn.split(",")[0]} asns_details_dict={props.asns_details_dict} />,
      sortable: true,
    },
    {
      name: 'Infected AS_PATH',
      cell: (row) => <ASPath asn={row.asn.split(",")[0]} asns_details_dict={props.asns_details_dict} as_path={props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix[row.asn.split(",")[0]]}/>,
    },
  ]
  
  const columns_infectedASes_AfterMitigation = [
    {
      name: 'Infected AS',
      selector: row => <ASInfo asn={row.asn.split(",")[0]} asns_details_dict={props.asns_details_dict} />,
      sortable: true,
    },
    {
      name: 'Infected AS_PATH',
      cell: (row) => <ASPath asn={row.asn.split(",")[0]} asns_details_dict={props.asns_details_dict} as_path={props.rep_data.after_mitigation.dict_of_nodes_and_infected_paths_to_mitigation_prefix[row.asn.split(",")[0]]}/>,
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

  const ASes_ROV_table_columns = [
    {
      name: 'AS',
      cell: (row) => <ASInfo asn={row.asn.split(",")[0]} asns_details_dict={props.asns_details_dict} />,
    },
  ]


  useEffect(() => {

    /*Prepare RPKI ROV TABLE Data*/
    const rpki_rov_table_data = [];
    for (let asn in props.rep_data.rpki_rov_table) {
      for (let prefix in props.rep_data.rpki_rov_table[asn]){
        rpki_rov_table_data.push({"asn": asn, "prefix": prefix, "state": props.rep_data.rpki_rov_table[asn][prefix]})
      }
    }
    setRpki_rov_table_data(rpki_rov_table_data)

    /*Prepare the list of ASes that do ROV*/
    const ASes_that_do_ROV = [];
    for (let asn in props.rep_data.ASes_that_do_ROV){
      if (props.asns_details_dict.hasOwnProperty(asn)){
        ASes_that_do_ROV.push({"asn": asn+','+props.asns_details_dict[asn]["name"]})
      }else{
        ASes_that_do_ROV.push({"asn": asn+','})
      }
    }
    setASes_that_do_ROV(ASes_that_do_ROV)

    /*Prepare the data of the tables that depict the infected ASes and AS_PATHS*/
    const generate_infected_AS_path_data = (dict_of_nodes_and_infected_paths) => {
      const infectedASes = [];
      for (let asn in dict_of_nodes_and_infected_paths){
        if (props.asns_details_dict.hasOwnProperty(asn)){
          infectedASes.push({"asn": asn+','+props.asns_details_dict[asn]["name"]})
        }else{
          infectedASes.push({"asn": asn+','})
        }
      }
      return infectedASes
    }
    
    setInfectedASes_AfterHijack(generate_infected_AS_path_data(props.rep_data.after_hijack.dict_of_nodes_and_infected_paths_to_hijacker_prefix))
    setInfectedASes_AfterMitigation(generate_infected_AS_path_data(props.rep_data.after_mitigation.dict_of_nodes_and_infected_paths_to_mitigation_prefix))
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
                      <td>
                        {props.rep_data.anycast_ASes.map((asn, i) => <ASInfo key={i} asn={asn} asns_details_dict={props.asns_details_dict} />)}
                      </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div style={{marginLeft: "50px", marginRight: "30px"}}>
              <h1>RPKI ROV Table</h1>
              {isRenderAvailable && <DataTable 
                columns={rpki_rov_table_columns}
                data={rpki_rov_table_data}
                pagination
                paginationPerPage={5}
                paginationRowsPerPageOptions={[5, 10]}
              />}
            </div>
            <div>
              <h1>List of ASes that do ROV</h1>
              {isRenderAvailable && <ASesRovTable
                columns={ASes_ROV_table_columns}
                data={ASes_that_do_ROV}
                paginationPerPage={5}
                paginationRowsPerPageOptions={[5, 10]}
                noTableHead={true}
              />}
            </div>
          </div>
          <h1>Useful Statistics/Metrics</h1>
          <div className='row'>
            <div>
              <Chart
                chartType="ColumnChart"
                loader={<div>Loading Chart</div>}
                data={[
                  ['%', 'After Hijack', 'After Mitigation'],
                  [props.rep_data.before_hijack.nb_of_nodes_with_path_to_legitimate_prefix.toString(), 
                    props.rep_data.after_hijack.impact_estimation,
                    props.rep_data.after_mitigation.impact_estimation
                  ],
                ]}
                options={{
                  title: 'Impact Estimation',
                  chartArea: { width: '40%' },
                  colors: ['#b0120a', '#ffab91'],
                  hAxis: {
                    title: '# Route Collectors \n(Monitors)',
                    minValue: 0,
                    maxValue: 100
                  },
                  vAxis: {
                    title: '% Impact',
                  },
                  width: 500,
                  height: 300
                }}
                legendToggle
              />
            </div>
            <div style={{marginLeft: "180px"}}>
              <Chart
                chartType="Bar"
                loader={<div>Loading Chart</div>}
                data={[
                  ['', 'Before Hijack', 'After Hijack', 'After Mitigation'],
                  ['# Nodes with Hijacked Path', 
                    props.rep_data.before_hijack.nb_of_nodes_with_hijacked_path_to_legitimate_prefix, 
                    props.rep_data.after_hijack.nb_of_nodes_with_hijacked_path_to_hijacker_prefix, 
                    props.rep_data.after_mitigation.nb_of_nodes_with_hijacked_path_to_mitigation_prefix,
                  ],
                ]}
                options={{
                  // Material design options
                  chart: {
                    title: '',
                    subtitle: '',
                  },
                  width: 400,
                  height: 300
                }}
              />
            </div>
          </div>
          <div style={{marginTop: "100px"}}>
            {isRenderAvailable && <InfectedPathsTable
              title="Infected ASes and Paths After Hijack"
              columns={columns_infectedASes_AfterHijack}
              data={infectedASes_AfterHijack}
              progressPending={!isRenderAvailable}
              paginationPerPage={5}
              paginationRowsPerPageOptions={[5, 10, 15, 20, 25, 30]}
            />}
          </div>
          <div style={{marginTop: "100px"}}>
            {isRenderAvailable && <InfectedPathsTable
              title="Infected ASes and Paths After Mitigation"
              columns={columns_infectedASes_AfterMitigation}
              data={infectedASes_AfterMitigation}
              progressPending={!isRenderAvailable}
              paginationPerPage={5}
              paginationRowsPerPageOptions={[5, 10, 15, 20, 25, 30]}
            />}
          </div>
        </div>
      </div>
    );
  };

export default Popup;