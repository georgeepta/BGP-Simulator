/*import React, { useEffect, useState } from 'react';
import Graph from 'react-vis-network-graph';



function ASGraph(props) {
    
    const [isRenderAvailable, setIsRenderAvailable] = useState(false);
    const [graph, setGraph] = useState();
     
    const options = {
        
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

        for (let asn in props.as_path_dict) {
            const as_node_first = {id: asn, label: asn, title: asn};
            const as_node_second = {id: props.as_path_dict[asn][0], label: props.as_path_dict[asn][0].toString(), title: props.as_path_dict[asn][0]};
            if (!graph.nodes.some(e => e.id === as_node_first.id)) {
                graph.nodes.push(as_node_first);
            }
            if (!graph.nodes.some(e => e.id === as_node_second.id)){
                graph.nodes.push(as_node_second);
            }
            graph.edges.push({from: as_node_first, to: as_node_second});

            if(props.as_path_dict[asn].length >= 2){
                for (let index=0; index < props.as_path_dict[asn].length-1; index+=1){
                    const as_node = {id: props.as_path_dict[asn][index+1], label: props.as_path_dict[asn][index+1].toString(), title: props.as_path_dict[asn][index+1]}
                    if (!graph.nodes.some(e => e.id === as_node.id)){
                        graph.nodes.push(as_node);
                    }
                    graph.edges.push({from: props.as_path_dict[asn][index], to: props.as_path_dict[asn][index+1]});
                }
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

export default ASGraph;*/