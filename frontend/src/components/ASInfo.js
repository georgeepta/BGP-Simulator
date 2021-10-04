import React from 'react';
import './ASInfo.css';

export function ASInfo(props) {
    
    
    const asn_details = props.asns_details_dict[props.asn];
    
    return (
        <div className="asn-info">
            <span className="tooltiptext">
                ASN: {props.asn}  |  
                AS Name: {asn_details["name"]} | 
                Country: {asn_details["organizationDetails"]["country"]} | 
                Organization Name: {asn_details["organizationDetails"]["name"]} | 
                Organization ID: {asn_details["organizationId"]} | 
                RIR: {asn_details["organizationDetails"]["source"]}
            </span>
            <a href={"https://asrank.caida.org/asns?asn=" + props.asn} target="_blank" rel="noreferrer">
                <span className={"flag-icon flag-icon-" + asn_details["organizationDetails"]["country"].toLowerCase()}></span>
                {" AS" + props.asn}<br/> 
                {asn_details["name"]}
            </a>
        </div>
    );
}