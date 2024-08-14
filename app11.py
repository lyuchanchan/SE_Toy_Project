from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 객체 생성
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# 데이터베이스 생성
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 비밀번호 해시 처리
        hashed_password = generate_password_hash(password, method='sha256')

        # 새로운 사용자 생성
        new_user = User(username=username, email=email, password=hashed_password)

        # 데이터베이스에 사용자 추가
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('signup_success'))
        except:
            return "There was an issue adding your registration."

    return render_template('signup.html')

@app.route('/signup_success')
def signup_success():
    return "Sign Up Successful!"

if __name__ == '__main__':
    app.run(debug=True)
