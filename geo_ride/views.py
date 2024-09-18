from flask import jsonify,Blueprint,render_template
from flask_login import login_required,current_user
from .models import User  

views=Blueprint('views',__name__)

@views.route('/')
def home():
    user = current_user
    return render_template('Page/index.html',user=user)

@views.route('/drivers')
@login_required
def drivers():
    # Query all users with the role 'driver'
    drivers = User.query.filter_by(role='driver').all()
    
    # Convert drivers to a list of dictionaries
    drivers_list = [
        {
            'id': driver.id,
            'name': driver.name,
        }
        for driver in drivers
    ]
    
    # Return the drivers list as a JSON response
    return jsonify(drivers_list)

@views.route('/driver_home')
def driver_home():
    return render_template('Page/driver.html')


@views.route('/api/driver/<int:driver_id>/email')
def get_driver_email(driver_id):
    # Fetch the driver from your database
    driver = User.query.get(driver_id)
    if driver:
        return jsonify({'email': driver.email})
    else:
        return jsonify({'error': 'Driver not found'}), 404
    
    
@views.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user  # Get the currently logged-in user
    role = "Driver" if user.role == "driver" else "User"  # Check if the user is a driver or a user
    return render_template('Page/profile.html', user=user, role=role)

