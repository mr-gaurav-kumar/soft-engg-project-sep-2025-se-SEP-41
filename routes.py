from flask_restful import Api, Resource, reqparse 
# Resource class does many backend things like how the app is connecting to  get function when we request via API, we have not called
# the get function anywhere. It is defined in the Resources
from flask import request
from models import *
from datetime import datetime

from flask import current_app as app, jsonify, request, render_template, send_from_directory
# from flask_security import hash_password, auth_required, roles_required, current_user, roles_accepted, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, time

def setup_routes(app):

    # Entry point for the application FE
    @app.route('/', methods = ['GET'])
    def home():
        return "Hello, Application Started!"


    # customer registration

    @app.route('/api/customer/register', methods = ['POST'])
    # or we can write - @app.post('/api/register')
    def customer_register():
        credentials = request.get_json()
        if not Customer.query.filter_by(email=credentials["email"]).first():
            # dob_str = credentials.get("dob", "").strip()
            # if not dob_str:
            #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
            dob_date = datetime.strptime(credentials["dob"], "%Y-%m-%d").date()
            count = Customer.query.count()
            new_customer = Customer(email = credentials["email"],
                                            name = credentials["name"],
                                            password = generate_password_hash(credentials["password"]),
                                            role = 1,
                                            dob = dob_date,
                                            contact_number = credentials["contact_number"],
                                            date_of_signup = datetime.now().date(),
                                            account_number = 1000+count+1,
                                            location = credentials["location"],
                                            pin_code = credentials["pincode"])
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({
                "message": "Customer created successfully"
            }), 201
        
        return jsonify({
            "message": "Customer already exits!"
        }), 400


# manager registration

    @app.route('/api/manager/register', methods = ['POST'])
    # or we can write - @app.post('/api/register')
    def manager_register():
        credentials = request.get_json()
        if not Bank_manager.query.filter_by(email=credentials["email"]).first():
            # dob_str = credentials.get("dob", "").strip()
            # if not dob_str:
            #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
            
            new_manager = Bank_manager(email = credentials["email"],
                                            name = credentials["name"],
                                            password = generate_password_hash(credentials["password"]),
                                            role = 3,
                                            contact_number = credentials["contact_number"],
                                            date_of_regn = datetime.now().date())
            db.session.add(new_manager)
            db.session.commit()
            return jsonify({
                "message": "Manager created successfully"
            }), 201
        
        return jsonify({
            "message": "Manager already exits!"
        }), 400


    # employee registration

    @app.route('/api/employee/register', methods = ['POST'])
    # or we can write - @app.post('/api/register')
    def employee_register():
        credentials = request.get_json()
        if not Bank_employee.query.filter_by(email=credentials["email"]).first():
            # dob_str = credentials.get("dob", "").strip()
            # if not dob_str:
            #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
            
            new_employee = Bank_employee(email = credentials["email"],
                                            name = credentials["name"],
                                            password = generate_password_hash(credentials["password"]),
                                            role = 2,
                                            contact_number = credentials["contact_number"],
                                            date_of_regn = datetime.now().date(),
                                            manager_id = credentials["manager_id"])
            db.session.add(new_employee)
            db.session.commit()
            return jsonify({
                "message": "Employee created successfully"
            }), 201
        
        return jsonify({
            "message": "Employee already exits!"
        }), 400


    