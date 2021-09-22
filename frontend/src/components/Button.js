import React from 'react';
import './Button.css';
import { Link } from 'react-router-dom';

export function Button(props) {
    
    const className = `btn ${props.type}`

    return (
        <Link to={props.pagelink}>
            <button className={className}> {props.btnname} </button>
        </Link>
    );
}