from flask import Blueprint, request, jsonify, current_app
from app.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['name', 'email', 'interests', 'location', 'travel_dates']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    user = User(
        name=data['name'],
        email=data['email'],
        interests=data['interests'],
        location=data['location'],
        travel_dates=data['travel_dates']
    )
    db = current_app.config['db']
    db.users.insert_one(user.to_dict())
    return jsonify({'message': 'User registered successfully'}), 201 