from flask import Blueprint, request, jsonify
from extension import db
from models import Service
api_controller = Blueprint('api_controller', __name__)

@api_controller.route('/add_service', methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('base_price'):
            return jsonify({"error": "Missing required fields: name and base_price are required"}), 400
        
        new_service = Service(
            name=data['name'],
            desc=data.get('desc', ''), 
            base_price=data['base_price']
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({
            "message": "Service added successfully",
            "service_id": new_service.ser_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
