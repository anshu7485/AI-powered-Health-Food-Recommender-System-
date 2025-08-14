from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    # Relationship to health profile
    # health_profile = db.relationship('HealthProfile', backref='user', uselist=False)

# New table for health profile
class HealthProfile(db.Model):
    __tablename__ = 'health_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    medical_conditions = db.Column(db.Text)
    allergies = db.Column(db.Text)
    daily_calorie_goal = db.Column(db.Integer)
    sugar_limit = db.Column(db.Integer)
    sodium_limit = db.Column(db.Integer)

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    barcode = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nutrition_json = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)

class Scan(db.Model):
    __tablename__ = 'scans'
    scan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    barcode = db.Column(db.String(50), db.ForeignKey('food_items.barcode'))
    scan_time = db.Column(db.DateTime)
    recommendation = db.Column(db.Text)
    health_score = db.Column(db.Float)
