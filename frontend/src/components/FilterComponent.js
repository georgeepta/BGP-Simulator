import React from 'react';

function FilterComponent(props){

    return(
        <input type="text" style={{height: "30px", borderRadius: "8px"}} placeholder="Search by ASN, AS-Name" onChange={(event) =>props.onFilter(event)} />
    );
}

export default FilterComponent;