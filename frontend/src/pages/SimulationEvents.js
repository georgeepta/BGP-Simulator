import React, { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import '../App.css';
import './SimulationEvents.css'

function SimulationEvents() {
  
  const [data, setData] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
	const [toggleCleared, setToggleCleared] = useState(false);

  const columns = [
    {
      name: 'Simulation UUID',
      selector: row => row.simulation_id,
      sortable: true,
    },
    {
      name: 'Simulation Status',
      selector: row => row.simulation_status,
      sortable: true,
      conditionalCellStyles: [
        {
          when: row => row.simulation_status === 'Completed',
          style: {
            color: '#009610'
          }
        },
        {
          when: row => row.simulation_status === 'In-Progress',
          style: {
            color: '#004b96'
          }
        },
        {
          when: row => row.simulation_status === 'Failed',
          style: {
            color: '#e40101'
          }
        },
      ]
    },
    {
      name: 'Simulation Type',
      selector: row => row.simulation_data.simulation_type,
      sortable: true,
    },
    {
      name: 'Completed Simulations',
      selector: row => (row.num_of_finished_simulations).toString() + '/' + (row.num_of_simulations * row.num_of_repetitions).toString(),
      sortable: true,
    },
    {
      name: 'Start Time',
      selector: row => row.sim_start_time,
      sortable: true,
    },
    {
      name: 'End Time',
      selector: row => row.sim_end_time,
      sortable: true,
    },
  ];

  const handleRowSelected = React.useCallback(state => {
		setSelectedRows(state.selectedRows);
	}, []);

  const contextActions = React.useMemo(() => {
		const handleDelete = () => {
			
			if (window.confirm(`The following Simulations will permanently deleted from db: \n\n ${selectedRows.map(r => r.simulation_id + '\n')} \nAre you sure?`)) {
				setToggleCleared(!toggleCleared);
				setData(data.filter(x => !selectedRows.includes(x)));
        selectedRows.forEach(row => {

          fetch('http://127.0.0.1:5000/simulation_events', {
            method: 'DELETE',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({'simulation_uuid': row.simulation_id})
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

          }).catch(error => {
            console.error('There was an error!', error.message);
          });

        });
			}
		};

		return (
			<button key="delete" onClick={handleDelete} style={{ 
        backgroundColor: 'red', 
        border: 'medium none',
        color: 'white',
        padding: '8px, 32px',
        textAlign: 'center',
        textDecoration: 'none',
        display: 'inline-block',
        fontSize: '16px',
        borderRadius: '3px'
        }}>
				Delete
			</button>
		);
	}, [data, selectedRows, toggleCleared]);
  
  
  useEffect(() => {
    fetch('http://127.0.0.1:5000/simulation_events', {
            method: 'GET',
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
            setData(data);
        }).catch(error => {
          console.error('There was an error!', error.message);
        });
  }, [])
  
  return (
    <div className='simulation-events'>
      <DataTable 
        title="SIMULATION EVENTS"
        columns={columns}
        data={data}
        highlightOnHover
        pointerOnHover
        selectableRows
        contextActions={contextActions}
			  onSelectedRowsChange={handleRowSelected}
			  clearSelectedRows={toggleCleared}
        pagination
      />
    </div>
  );
}

export default SimulationEvents;