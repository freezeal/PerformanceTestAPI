from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app=Flask(__name__)

# SQLite 데이터베이스 파일 경로
DATABASE = 'example.db'

# 데이터베이스 연결 함수
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

# 계산 이력 저장 함수
def save_calculation_history(operation, num1, num2, result):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO calculation_history (operation, num1, num2, result) VALUES (?, ?, ?, ?)', (operation, num1, num2, result))
    db.commit()
    db.close()
@app.route('/history_api')
def history_api():
    # 데이터베이스 연결
    db = get_db()
    cursor = db.cursor()

    # 계산 히스토리 조회
    cursor.execute('SELECT * FROM calculation_history')
    history_data = cursor.fetchall()

    # 데이터베이스 연결 종료
    db.close()

    # 계산 히스토리를 JSON 형식으로 반환
    history_json = []
    for history in history_data:
        history_json.append({
            'id': history[0],
            'num1': history[1],
            'operation': history[2],
            'num2': history[3],
            'result': history[4]
        })

    return jsonify({'history': history_json})

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

    # 계산 이력 저장
    save_calculation_history(num1, operation, num2, result)

    return jsonify({'result': result})

@app.route('/show_image')
def show_image():
    return render_template('ShowImage.html')

@app.route('/history_view')
def History():
    return render_template('History.html')

if __name__ == '__main__':
    app.run(debug=True)