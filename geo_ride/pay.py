from flask import Blueprint, request, jsonify
from . import db
from .models import User ,Order
import requests
from flask_login import login_required,current_user

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    reference = data.get('reference')
    driver_id = data.get('driver_id')
    user_id = data.get('user_id')  
    pickup_location = data.get('pickup_location')
    destination = data.get('destination')
    
    # Log reference and driver_id for debugging
    print('Payment Reference:', reference)
    print('Driver ID:', driver_id)

    # Replace with your Paystack secret key
    secret_key = 'sk_test_34b0f46825a6c075b01197d5fd97d18e2e028b92'

    # Verify payment with Paystack
    verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(verify_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error verifying payment: {e}")
        return jsonify({"error": "Payment verification failed"}), 500

    response_data = response.json()
    print('Response Data:', response_data)  # Log the entire response

    if response_data.get('status') and response_data['data'].get('status') == 'success':
        driver = User.query.get(driver_id)
        user = User.query.get(user_id)

        if not driver or not user:
            return jsonify({"error": "Driver or user not found"}), 404

        # Save the order details
        order = Order(
            user_id=user_id,
            driver_id=driver_id,
            pickup_location=pickup_location,
            destination=destination,
            amount_paid=response_data['data']['amount'] / 100  # Convert kobo to naira
        )
        db.session.add(order)
        db.session.commit()

        return jsonify({"success": True, "message": "Payment verified and order saved"}), 200
    else:
        return jsonify({"error": "Payment verification failed"}), 400
    
    
@payments_bp.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    user_id = current_user.id
    user_role = current_user.role

    # Define query based on user role
    if user_role == 'driver':
        orders = Order.query.filter_by(driver_id=user_id).all()
    elif user_role == 'user':
        orders = Order.query.filter_by(user_id=user_id).all()
    else:
        return jsonify({'error': 'Invalid user role'}), 403

    # Convert orders to a list of dictionaries
    orders_list = [{
        'id': order.id,
        'pickup_location': order.pickup_location,
        'destination': order.destination,
        'amount_paid': order.amount_paid,
        'driver_name': User.query.get(order.driver_id).name if order.driver_id else 'N/A'
    } for order in orders]

    return jsonify({'orders': orders_list})

