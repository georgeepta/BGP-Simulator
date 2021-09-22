import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import NewSimulation from './pages/NewSimulation';
import SimulationEvents from './pages/SimulationEvents';
import Home from './pages/Home';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component={Home} />
        <Route path='/new-simulation' exact component={NewSimulation} />
        <Route path='/simulation-events' exact component={SimulationEvents} />
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
