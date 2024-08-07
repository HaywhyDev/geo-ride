from flask import Blueprint, render_template, redirect, url_for, flash, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user,current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.user_signup'))

        new_user = User(name=name, email=email, password_hash=generate_password_hash(password), role='user')
        db.session.add(new_user)
        db.session.commit()

        flash('User account created successfully!')
        return redirect(url_for('auth.user_login'))

    return render_template('User/register.html')

@auth.route('/driver/signup', methods=['GET', 'POST'])
def driver_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        license_number = request.form.get('license')
        phone_number = request.form.get('phone')  # Get phone number

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.driver_signup'))

        new_driver = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='driver',
            license_number=license_number,
            phone_number=phone_number  # Add phone number
        )
        db.session.add(new_driver)
        db.session.commit()

        flash('Driver account created successfully!')
        return redirect(url_for('auth.driver_login'))

    return render_template('Driver/register.html')

@auth.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, role='user').first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Login unsuccessful. Please check your email and password')
            return redirect(url_for('auth.user_login'))

        login_user(user)  # Handle login
        flash('User logged in successfully!')
        return redirect(url_for('views.home'))

    return render_template('User/login.html')

@auth.route('/driver/login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        driver = User.query.filter_by(email=email, role='driver').first()

        if not driver or not check_password_hash(driver.password_hash, password):
            flash('Login unsuccessful. Please check your email and password')
            return redirect(url_for('auth.driver_login'))

        login_user(driver)  # Handle login
        flash('Driver logged in successfully!')
        return redirect(url_for('views.driver_home'))

    return render_template('Driver/login.html')

@auth.route('/logout')
def logout():
    logout_user()  # Handle logout
    flash('You have been logged out.')
    return redirect(url_for('auth.user_login'))

@auth.route('/check-auth')
def check_auth():
    if not current_user.is_authenticated:
        return jsonify({'authenticated': False}), 401  # Not authenticated
    return jsonify({'authenticated': True}), 200  # Authenticated