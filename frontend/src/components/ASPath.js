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

        graph.nodes.push({id: props.asn, label: props.asn, title: props.asn})
        graph.nodes.push({id: props.as_path[0], label: props.as_path[0].toString(), title: props.as_path[0]})
        graph.edges.push({from: props.asn, to: props.as_path[0]})

        if(props.as_path.length >= 2){
            for (let index=0; index < props.as_path.length-1; index+=1){
                graph.nodes.push({id: props.as_path[index+1], label: props.as_path[index+1].toString(), title: props.as_path[index+1]});
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