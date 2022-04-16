<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="frontend/src/images/BPHS_logo.png" alt="Logo" width="160" height="80">
  </a>

  <h3 align="center">BPHS</h3>

  <p align="center">
    A BGP Prefix Hijacking Simulation tool supporting RPKI filtering.
    <br />
    <a href="https://github.com/georgeepta/BGP-Simulator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/georgeepta/BGP-Simulator">View Demo</a>
    ·
    <a href="https://github.com/georgeepta/BGP-Simulator/issues">Report Bug</a>
    ·
    <a href="https://github.com/georgeepta/BGP-Simulator/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#minimum system requirements">Minimum System Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

_BPHS, is a Web-based BGP Prefix Hijacking Simulation tool that enables network operators to quickly and easily:_ 

1. _assess the vulnerability of their Autonomous Systems to BGP prefix hijacks_

2. _measure the benefits of the RPKI’s adoption in the Internet_ 

_through a user-friendly web application._

_With BPHS, the network operators can simulate all the different types of BGP hijacking attacks and obtain the simulation results through an automated and graphical way (i.e., well-designed Graphical User Interface). Also, BPHS can be offered as a Web service to the end-users, meaning that, can be publicly deployed and easily accessible by anyone in the Internet._

BPHS supports:

* user-friendly GUI for easy interaction from desktop and mobile web-browsers 

* multi-threading execution enabling end-users to retrieve quicker results per simulation 

* REST API to allow other applications to communicate with the simulator 

* realtime RPKI filtering using the most up-to-date data from the RPKI databases, for more realistic simulation results

Our simulator, models the Internet graph through the well-known AS relationship datasets from CAIDA, applies the user preferences on the generated graph (e.g., random or custom simulation, hijack type, RPKI filtering mode) and finally simulates the BGP protocol (i.e., BGP route propagation, import-export policies) along with different types of prefix hijacks.


![BPHS Screen Shot][bphs-overview]

<p align="right">(<a href="#top">back to top</a>)</p>




### Built With

BPHS is a full-stack web application that inherits all the characteristics of the MVC model. For its developement we used the following well known frameworks/libraries, databases:

* [React.js](https://reactjs.org/)
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [PostgreSQL](https://www.postgresql.org/)

![BPHS Architecture][bphs-architecture]

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Below we list the minimum system requirements and the installation steps of BPHS.

### Minimum System Requirements

* CPU: 2 cores
* RAM: 2+ GB (note that needed memory depends on the number of parralel simulations)
* HDD: 500+ MB (depends on the use case for storing the simulation data)
* OS: Ubuntu Linux 18.04+ (other Linux distributions will work too)
* Python >= 3.6

### Installation



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/georgeepta/BGP-Simulator.svg?style=for-the-badge
[contributors-url]: https://github.com/georgeepta/BGP-Simulator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/georgeepta/BGP-Simulator.svg?style=for-the-badge
[forks-url]: https://github.com/georgeepta/BGP-Simulator/network/members
[stars-shield]: https://img.shields.io/github/stars/georgeepta/BGP-Simulator.svg?style=for-the-badge
[stars-url]: https://github.com/georgeepta/BGP-Simulator/stargazers
[issues-shield]: https://img.shields.io/github/issues/georgeepta/BGP-Simulator.svg?style=for-the-badge
[issues-url]: https://github.com/georgeepta/BGP-Simulator/issues
[license-shield]: https://img.shields.io/github/license/georgeepta/BGP-Simulator.svg?style=for-the-badge
[license-url]: https://github.com/georgeepta/BGP-Simulator/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/george-eptaminitakis-5702ab1ba
[bphs-overview]: images/BPHS_overview.png
[bphs-architecture]: images/BPHS_Architecture.png
