from flask import Flask, render_template, request, jsonify
import requests

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('HelloWorld.html')

@app.route('/request_api/<operation>', methods=['GET','POST'])
def request_api(operation):
    if request.method == 'GET':
        num1 = int(request.args.get('num1'))
        num2 = int(request.args.get('num2'))
    elif request.method == 'POST':
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')
    else:
        return jsonify({'error': 'Invalid request method'}), 400

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

@app.route('/show_image')
def show_image():
    return render_template('ShowImage.html')

if __name__ == '__main__':
    app.run(debug=True)