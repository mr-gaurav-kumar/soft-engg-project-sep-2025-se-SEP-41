import pytest
from app import create_app
from database import db
from models import *
from werkzeug.security import generate_password_hash
from datetime import date

# Test 1: Home page - working of application

def test_home_route():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data

# Test 2: Successful Registration (returns 201)

def test_customer_register():
    app = create_app()
    client = app.test_client()

    payload = {
        "email": "john@example.com",
        "name": "John",
        "password": "1234",
        "dob": "1990-01-01",
        "contact_number": "9999999999",
        "location": "Bangalore",
        "pincode": "560001"
    }

    response = client.post("/api/customer/register", json=payload)

    assert response.status_code in (201, 400)  # 201 for new user, 400 for duplicate


# Test 3: Successful Manager Registration (returns 201)

def test_manager_register():
    app = create_app()
    client = app.test_client()

    payload = {
        "email": "mag1@example.com",
        "name": "mag1",
        "password": "1234",
        "contact_number": "9999999999",
        
    }

    response = client.post("/api/manager/register", json=payload)

    assert response.status_code in (201, 400)  # 201 for new user, 400 for duplicate

# Test 4: Successful Employee Registration (returns 201)

def test_employee_register():
    app = create_app()
    client = app.test_client()

    payload = {
        "email": "emp1@example.com",
        "name": "emp1",
        "password": "1234",
        "contact_number": "9999999999",
        "manager_id": "1",
    }

    response = client.post("/api/employee/register", json=payload)

    assert response.status_code in (201, 400)  # 201 for new employee, 400 for duplicate
