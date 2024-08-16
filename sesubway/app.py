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
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        for user in users:
            if user['email'] == email:
                return jsonify({'error': 'User already exists!'}), 400

        users.append({
            'username': username,
            'email': email,
            'password': password
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
