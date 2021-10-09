import React, { useEffect, useState } from 'react';
import './ASInfo.css';

export function ASInfo(props) {
    
    
    const [asn_details, setAsn_details] = useState();
    const [hasDetails, setHasDetails] = useState(false);
    
    useEffect(() => {
        if (props.asns_details_dict.hasOwnProperty(props.asn)){
            setAsn_details(props.asns_details_dict[props.asn]);
            setHasDetails(true);
        }
    }, [props]);

    return (
        <div className="asn-info">
            {hasDetails && <span className="tooltiptext">
                ASN: {props.asn}  |  
                AS Name: {asn_details["name"]} | 
                Country: {asn_details["organizationDetails"]["country"]} | 
                Organization Name: {asn_details["organizationDetails"]["name"]} | 
                Organization ID: {asn_details["organizationId"]} | 
                RIR: {asn_details["organizationDetails"]["source"]}
            </span>}
            <a href={"https://asrank.caida.org/asns?asn=" + props.asn} target="_blank" rel="noreferrer">
                {hasDetails && <span className={"flag-icon flag-icon-" + asn_details["organizationDetails"]["country"].toLowerCase()}></span>}
                {" AS" + props.asn}<br/> 
                {hasDetails && asn_details["name"]}
            </a>
        </div>
    );
}