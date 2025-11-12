from .database import db
from .models import User, Role
from flask import current_app as app, jsonify, request, render_template, send_from_directory
from flask_security import hash_password, auth_required, roles_required, current_user, roles_accepted, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, time
from .util_funcs import roles_list
from celery.result import AsyncResult
from .tasks import csv_report, monthly_report

cache = app.cache

# Entry point for the application FE
@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')


@app.route('/api/admin')
@auth_required('token') # Authentication - token is required to access this
@roles_required('admin')  # Authorization - RBAC
def admin_home():
    user = current_user
    return jsonify({
        "name": user.name,
        "email": user.email,
        "roles": roles_list(user.roles)
    })


@app.route('/api/home')
@auth_required('token')
@roles_required('user')
def user_home():
    user = current_user
    return jsonify({
        "name": user.name,
        "email": user.email,
        "roles": roles_list(user.roles)
    })


@app.route('/api/register', methods = ['POST'])
# or we can write - @app.post('/api/register')
def register():
    credentials = request.get_json()
    if not app.security.datastore.find_user(email = credentials["email"]):
        # dob_str = credentials.get("dob", "").strip()
        # if not dob_str:
        #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
        dob_date = datetime.strptime(credentials["dob"], "%Y-%m-%d").date()
        app.security.datastore.create_user(email = credentials["email"],
                                           name = credentials["name"],
                                           password = generate_password_hash(credentials["password"]),
                                           roles = ['user'],
                                           dob = dob_date,
                                           qualification = credentials["qualification"])
        db.session.commit()
        return jsonify({
            "message": "User created successfully"
        }), 201
    
    return jsonify({
        "message": "User already exits!"
    }), 400



# @app.route('/api/mail')
# def send_reports():
#     res = monthly_report.delay()
#     return {
#         "result": res.result
#     }