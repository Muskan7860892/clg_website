from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Branch(db.Model):
    __tablename__ = 'branches'  # Ensure the table name is consistent
    id = db.Column(db.Integer, primary_key=True)
    branch_code = db.Column(db.String(10), unique=True, nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=True)  # General description
    vision = db.Column(db.Text, nullable=True)  # Vision statement
    mission = db.Column(db.Text, nullable=True)

    # Relationships
    images = db.relationship('BranchImages', backref='branch', lazy=True)
    staffs = db.relationship('Staff', backref='branch', lazy=True)
    hods = db.relationship('HOD', backref='branch', lazy=True)

class BranchImages(db.Model):
    __tablename__ = 'branch_images'
    id = db.Column(db.Integer, primary_key=True)
    branch_code = db.Column(db.String(10), db.ForeignKey('branches.branch_code'), nullable=False)  # Fixed FK reference
    image_url = db.Column(db.String(255), nullable=False)

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(100), nullable=False)
    staff_id = db.Column(db.String(20), unique=True, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)  # Changed from Integer to String (for consistency)
    qualification = db.Column(db.String(50), nullable=False)
    branch_code = db.Column(db.String(10), db.ForeignKey('branches.branch_code'), nullable=True)  # Fixed FK reference
    image_url = db.Column(db.String(255), nullable=True)

class HOD(db.Model):
    __tablename__ = 'hods'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    hod_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)  # Changed from Integer to String
    qualification = db.Column(db.String(100), nullable=False)
    branch_code = db.Column(db.String(10), db.ForeignKey('branches.branch_code'), nullable=True)  # Fixed FK reference
    image_url = db.Column(db.String(255), nullable=True)

class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    branch_code = db.Column(db.String(10), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)

class Management(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)

class Principal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)

class CellMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)  # Store image filename
    cell = db.Column(db.String(100), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    pdf_filename = db.Column(db.String(200), nullable=True)