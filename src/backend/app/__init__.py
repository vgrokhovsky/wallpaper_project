from flask import Flask, jsonify
from flask_cors import CORS




def create_app():
    app = Flask(__name__)
    
    app.secret_key = "qwe"
    CORS(app)

    @app.route('/api/get_data/')
    def get_data():
        data = {'message': 'data from flask'}
        return jsonify(data), 200


    return app
