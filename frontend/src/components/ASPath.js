import React, { useEffect, useState } from 'react';
import Graph from 'react-vis-network-graph';



function ASPath(props) {
    
    const [isRenderAvailable, setIsRenderAvailable] = useState(false);
    const [graph, setGraph] = useState();
     
    const options = {
        layout: {
            randomSeed: undefined,
            improvedLayout:true,
        },
        edges: {
            color: "#000000"
        },
        height: "300px"
    };
    

    useEffect(() => {

        const graph = {
            nodes: [],
            edges: []
        };

        const AS_info_str = (asn) => {
            return (
                "AS Name: "+props.asns_details_dict[asn]["name"]+"</br>"+
                "Country: "+props.asns_details_dict[asn]["organizationDetails"]["country"]+"</br>"+
                "Organization Name: "+props.asns_details_dict[asn]["organizationDetails"]["name"]+"</br>"+
                "Organization ID: "+props.asns_details_dict[asn]["organizationId"]+"</br>"+
                "RIR: "+props.asns_details_dict[asn]["organizationDetails"]["source"]+"</br>"
            )
        }

        graph.nodes.push({id: props.asn, label: props.asn, title: AS_info_str(props.asn)})
        graph.nodes.push({id: props.as_path[0], label: props.as_path[0].toString(), title: AS_info_str(props.as_path[0])})
        graph.edges.push({from: props.asn, to: props.as_path[0]})

        if(props.as_path.length >= 2){
            for (let index=0; index < props.as_path.length-1; index+=1){
                graph.nodes.push({id: props.as_path[index+1], label: props.as_path[index+1].toString(), title: AS_info_str(props.as_path[index+1])});
                graph.edges.push({from: props.as_path[index], to: props.as_path[index+1]});
            }
        }
        setGraph(graph)
        setIsRenderAvailable(true)
    
    }, [props]);
    


    return (
        {isRenderAvailable} && <Graph
            graph={graph}
            options={options}
        />
    );
}

export default ASPath;