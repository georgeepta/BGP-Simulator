import React from 'react';
import DataTable from 'react-data-table-component';
import FilterComponent from './FilterComponent';


function ASesRovTable(props){
    
    const [filterText, setFilterText] = React.useState('');
	const [resetPaginationToggle, setResetPaginationToggle] = React.useState(false);
	const filteredItems = props.data.filter(
		item => item.asn && item.asn.toLowerCase().includes(filterText.toLowerCase()),
	);

    const subHeaderComponentMemo = React.useMemo(() => {
		const handleClear = () => {
			if (filterText) {
				setResetPaginationToggle(!resetPaginationToggle);
				setFilterText('');
			}
		};

		return (
			<FilterComponent onFilter={e => setFilterText(e.target.value)} onClear={handleClear} filterText={filterText} />
		);
	}, [filterText, resetPaginationToggle]);
    
    return(
        <DataTable 
            columns={props.columns}
            data={filteredItems}
            pagination
            paginationPerPage={props.paginationPerPage}
            paginationRowsPerPageOptions={props.paginationRowsPerPageOptions}
            noTableHead={props.noTableHead}
            paginationResetDefaultPage={resetPaginationToggle} // optionally, a hook to reset pagination to page 1
            subHeader
            subHeaderComponent={subHeaderComponentMemo}
            highlightOnHover
        />
    );
}

export default ASesRovTable;