from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import sqlite3
import os
import logging

app=Flask(__name__)
app.secret_key = os.urandom(24)  # 세션 키 설정
app.logger.setLevel(logging.DEBUG)

#로그 수집을 위한 함수 추가
@app.before_request
def log_request_info():
    app.logger.debug('Request: %s', request.data)

# SQLite 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('user.db')
    conn.row_factory = sqlite3.Row
    return conn

# 사용자 테이블 생성 함수
def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 기본 사용자 추가 함수
def add_default_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', ('admin',))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', '1234'))
        conn.commit()
    conn.close()

@app.route('/login_api', methods=['POST'])
def login_api():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return jsonify({'message': 'Login successful'}), 200

    else:
        return jsonify({'error': 'Incorrect username or password'}), 401

@app.route('/logout_api', methods=['POST'])
def logout_api():
    # 세션 종료
    print(session)
    if 'username' in session:
        session.pop('username', None)
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'message': 'No active session'}), 200

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

@app.route('/delete_history', methods=['DELETE'])
def delete_history():
    try:
        # 데이터베이스 연결
        db = get_db()
        cursor = db.cursor()

        # 계산 히스토리 삭제
        cursor.execute('DELETE FROM calculation_history')
        db.commit()

        # 데이터베이스 연결 종료
        db.close()

        return jsonify({'message': 'Calculation history deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/calculator_api/<operation>', methods=['GET','POST'])
def calculator_api(operation):
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

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('HelloWorld.html') # 세션이 있는 경우 HelloWorld로 리다이렉트
    else:
        return render_template('Login.html'), 401  # 세션이 없는 경우 401 에러 코드를 함께 반환

@app.errorhandler(401)
def unauthorized(error):
    return render_template('Login.html'), 401  # 401 에러 발생 시 Login.html 페이지로 리다이렉트

@app.route('/show_image')
def show_image():
    return render_template('ShowImage.html')

@app.route('/history_view')
def History():
    return render_template('History.html')

if __name__ == '__main__':
    app.run(debug=True)
    create_user_table()
    add_default_user()