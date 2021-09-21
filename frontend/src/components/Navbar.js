import './Navbar.css';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
/*import { Button } from './Button';
import Dropdown from './Dropdown';*/


function Navbar() {
    
    const [click, setClick] = useState(false);
    /*const [dropdown, setDropdown] = useState(false);*/
    
    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    /*const onMouseEnter = () => {
        if (window.innerWidth < 960){
            setDropdown(false);
        } else {
            setDropdown(true);
        }
    }

    const onMouseLeave = () => {
        if (window.innerWidth < 960){
            setDropdown(false);
        } else {
            setDropdown(false);
        }
    }*/
    
    return(
      <>
       <nav className='navbar'>
           <Link to='/' className='navbar-logo'>
                  BGP Hijacking Simulator
           </Link>
           <div className='menu-icon' onClick={handleClick}>
               <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
           </div>
           <ul className={click ? 'nav-menu active' : 'nav-menu'}>
               <li className='nav-item'>
                   <Link to='/' className='nav-links' onClick={closeMobileMenu}>
                     Home
                   </Link>
               </li>
               <li className='nav-item'>
                   <Link to='/new-simulation' className='nav-links' onClick={closeMobileMenu}>
                     New Simulation
                   </Link>
               </li>
               <li className='nav-item'>
                   <Link to='/simulation-events' className='nav-links' onClick={closeMobileMenu}>
                     Simulation Events
                   </Link>
               </li>
               {/*<li className='nav-item' onMouseEnter={onMouseEnter} onMouseLeave={onMouseLeave}>
                   <Link to='/services' className='nav-links' onClick={closeMobileMenu}>
                     Services <i className='fas fa-caret-down' />
                   </Link>
                   {dropdown && <Dropdown />}
               </li>
               <li className='nav-item'>
                   <Link to='/sign-up' className='nav-links-mobile' onClick={closeMobileMenu}>
                     Sign Up
                   </Link>
                </li>*/}
           </ul>
           {/*<Button />*/}
        </nav>
      </>
    );
}

export default Navbar;