"""auth route for session auth"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)


# Registration Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = generate_password_hash(password)

    # Check if the username or email already exists
    if User.query.filter_by(username=username).first():
      flash('Username already exists. Please choose a different one.')
      return redirect(url_for('auth.register'))
    if User.query.filter_by(email=email).first():
      flash('Email already exists. Please use a different email.')
      return redirect(url_for('auth.register'))

    # Create a new user and add to the database
    new_user = User(username=username,
                    email=email,
                    password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful! You can now log in.')
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html')


# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
      login_user(user)  # Log in the user
      flash('Login successful!')
      return redirect(url_for('home'))  # Redirect to home or dashboard
    else:
      flash('Invalid email or password. Please try again.')
      return redirect(url_for('auth.login'))

  return render_template('auth/login.html')


# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()  # Log out the current user
  flash('You have been logged out.')
  return redirect(url_for('auth.login'))  # Redirect to login page
