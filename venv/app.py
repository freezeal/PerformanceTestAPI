from flask import Flask, render_template, request, jsonify
import requests

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('HelloWorld.html')

@app.route('/request_api', methods=['POST'])
def request_api():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    result = num1 + num2

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)