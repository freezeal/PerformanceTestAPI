from flask import Flask, render_template, request, jsonify
import requests

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('HelloWorld.html')

@app.route('/request_api/<operation>', methods=['POST'])
def request_api(operation):
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return jsonify({'error': 'Cannot divide by zero'}), 400
    else:
        return jsonify({'error': 'Invalid operation'}), 400

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)