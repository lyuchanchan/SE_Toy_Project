from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# 임시 데이터베이스 (딕셔너리 사용)
users = {}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': '모든 필드를 입력해주세요.'}), 400

    if email in users:
        return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400

    # 비밀번호 해싱
    hashed_password = generate_password_hash(password)

    # 사용자 정보 저장
    users[email] = {
        'username': username,
        'password': hashed_password
    }

    return jsonify({'message': '회원가입이 완료되었습니다.'}), 201

if __name__ == '__main__':
    app.run(debug=True)
