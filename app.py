from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# 사용자 데이터를 임시로 저장 (간단함을 위해 메모리에 저장)
users = []

@app.route('/')
def home():
    return redirect(url_for('search'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
            
        # 사용자가 이미 존재하는지 확인
        for user in users:
            if user['email'] == email:
                return jsonify({'error': 'User already exists!'}), 400
        
        # 새로운 사용자를 목록에 추가
        users.append({
            'username': username,
            'email': email,
            'password': password  # 참고: 실제 애플리케이션에서는 항상 비밀번호를 해시 처리하세요!
        })

        return jsonify({'message': 'User registered successfully!'}), 201

    return render_template('signup.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)