
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, HealthProfile
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(16)  # Securely generated secret key

# PostgreSQL URI placeholder (replace with your actual URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anshu906@localhost:3306/M_project_db'  # Updated to use your actual MySQL database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Table creation will be handled in the main block

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # Basic validation
        if not name or not email or not password or not confirm_password:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('signup'))
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists!', 'error')
                return redirect(url_for('signup'))
            hashed_password = generate_password_hash(password)
            user = User(name=name, email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            flash('Signup successful! Welcome.', 'success')
            return redirect(url_for('health_profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during signup. Please try again.', 'error')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/health_profile', methods=['GET', 'POST'])
def health_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    health_profile = HealthProfile.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        if not health_profile:
            health_profile = HealthProfile(user_id=user_id)
            db.session.add(health_profile)
        health_profile.medical_conditions = request.form.get('medical_conditions')
        health_profile.allergies = request.form.get('allergies')
        health_profile.daily_calorie_goal = request.form.get('daily_calorie_goal')
        health_profile.sugar_limit = request.form.get('sugar_limit')
        health_profile.sodium_limit = request.form.get('sodium_limit')
        db.session.commit()
        flash('Health profile updated!')
        return redirect(url_for('login'))
    return render_template('health_profile.html', user=user, health_profile=health_profile)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # You can update this route to use the database for authentication
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
