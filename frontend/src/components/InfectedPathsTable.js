import React from 'react';
import DataTable from 'react-data-table-component';
import FilterComponent from './FilterComponent';


function InfectedPathsTable(props){
    
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
            title={props.title}
            columns={props.columns}
            data={filteredItems}
            progressPending={props.progressPending}
            paginationResetDefaultPage={resetPaginationToggle} // optionally, a hook to reset pagination to page 1
            subHeader
            subHeaderComponent={subHeaderComponentMemo}
            highlightOnHover
            pagination
        />
    );
}

export default InfectedPathsTable;