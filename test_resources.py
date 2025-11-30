import pytest
from app import create_app
from database import db
from models import *
from werkzeug.security import generate_password_hash
from datetime import date

# Test 4: Task API - Create - success
# Test 5: Task API - Create - missing field

def test_task_api_create():
    app = create_app()
    client = app.test_client()

    payload = {
        "name": "Verification",
        "employee_id": "1",
        "customer_id": "1",
        "due_date": "2025-01-01",
        "priority": "high",
        "description": "KYC verification of customer id - 1"
    }

    response = client.post("/api/task/create", json=payload)

    assert response.status_code in (201, 400)  # 201 for new task, 400 for duplicate or missing field
    assert response.get_json()["message"] == "Task created successfully"


# Test 6: Task API - Get

def test_task_api_get():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/task/get")
    assert response.status_code in (201, 404)  # 201 for task, 404 for no tasks


# Test 7: Task API - Put/ Update

def test_task_api_put():
    app = create_app()
    client = app.test_client()
    response = client.put("/api/task/update/1")
    assert response.status_code in (201, 404)  # 201 for success, 404 for no task
    assert response.get_json()["message"] == "The task status updated successfully"



# Test 8: Issue API - Create - success
# Test 9: Issue API - Create - missing field

def test_issue_api_create():
    app = create_app()
    client = app.test_client()

    payload = {
        "title": "Payment Confirmation",
        "customer_id": "1",
        "description": "Did not receive confirmation on the transaction with id: 1"
    }

    response = client.post("/api/issue/create", json=payload)

    assert response.status_code in (201, 400)  # 201 for new issue, 400 for duplicate or missing field
    assert response.get_json()["message"] == "Issue created successfully"


# Test 10: Issue API - Get

def test_issue_api_get():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/issue/get")
    assert response.status_code in (201, 404)  # 201 for task, 404 for no tasks


# Test 11: Issue API - Put/ Update

def test_issue_api_put():
    app = create_app()
    client = app.test_client()
    response = client.put("/api/issue/update/1")
    assert response.status_code in (201, 404)  # 201 for success, 404 for no issue
    assert response.get_json()["message"] == "The issue status updated successfully"