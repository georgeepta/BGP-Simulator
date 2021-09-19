import os
import sys
sys.path.insert(0, os.path.abspath(os.getcwd()))
from flask import Flask
from flask_restful import Api, Resource, reqparse
from api.SimulationRequestHandler import SimulationRequestHandler
from api.ASVulnerabilityRequestHandler import ASVulnerabilityRequestHandler

app = Flask(__name__)
api = Api(app)

@app.route('/hello', methods=['GET'])
def index():
    print("Hello - Link test")
    return {
        'message': 'George Eptaminitakis :) Successful link between React + Flask !!!'
    }

api.add_resource(SimulationRequestHandler, '/launch_simulation')
api.add_resource(ASVulnerabilityRequestHandler, '/as_vulnerability_ranking')

if __name__ == '__main__':
    app.run(debug=True)