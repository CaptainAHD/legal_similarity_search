from flask import Flask,request, jsonify, Response
from flask_cors import CORS
from agent import initialise_index, output

app = Flask(__name__)
CORS(app)
initialise_index()

@app.route('/')
def home():
    return 'Api is Healthy'

@app.route('/run', methods=['POST'])
def run():
    try:
        message = request.json.get('message')
        res = output(message)
        return jsonify(res)
    except Exception as e:
        return jsonify(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)