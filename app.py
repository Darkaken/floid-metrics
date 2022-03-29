
from flask import Flask, request
from flask_restful import Api
from src.main import main
from src.main_santander import main_santander

app = Flask(__name__)
api = Api(app)

@app.route('/get_income', methods=['POST'])
def get_income():

    return main(request.json)

@app.route('/get_income_santander', methods=['POST'])
def get_income_santander():

    return main_santander(request.json)

if __name__ == '__main__':
    app.run(debug = True)
