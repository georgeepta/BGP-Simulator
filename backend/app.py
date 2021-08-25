from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def index():
    return {
        'message': 'George Eptaminitakis :) Successful link between React + Flask !!!'
    }

if __name__ == '__main__':
    app.run(debug=True)