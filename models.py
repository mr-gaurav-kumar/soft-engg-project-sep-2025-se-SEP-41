# Data Models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    dob = db.Column(db.DateTime, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.Integer, default =1) # admin - 0, customer - 1, employee - 2, manager - 3
    date_of_signup = db.Column(db.DateTime, default = datetime.now) # NEED TO CONFIRM on type
    contact_number = db.Column(db.String, nullable = False)
    account_number = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    pin_code = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Pending') # Pending, Active , Flagged ,  Blocked
    # doc_name = db.Column(db.String, nullable = False) ## TO BE UPDATED
    # doc_data = db.Column(db.LargeBinary, nullable = False)
    
    # Defining backreference to enable parent to have access to all the children
    # beneficiaries = db.relationship(
    #     'Customer',               # refers to same class
    #     remote_side=[id],         # necessary for self-reference
    #     backref='beneficiaries'   # allows reverse access: customer.beneficiaries
    # )
    Beneficiaries = db.relationship('Beneficiary', cascade = 'all, delete', backref = 'customer', lazy = True)
    transactions = db.relationship(
        "Transaction",
        foreign_keys="[Transaction.from_customer]",   # specify FK here
        backref="sender",
        lazy=True
    )
    received_transactions = db.relationship(
        "Transaction",
        foreign_keys="[Transaction.to_customer]",    # specify FK here
        backref="receiver",
        lazy=True
    )
    # transactions = db.relationship('Transaction', cascade = 'all, delete', backref = 'customer', lazy = True)
    documents = db.relationship('Document', cascade = 'all, delete', backref = 'customer', lazy = True)
    tasks = db.relationship('Task', cascade = 'all, delete', backref = 'customer', lazy = True)
    # llm_interactions = tasks = db.relationship('LLM_interaction', cascade = 'all, delete', backref = 'customer', lazy = True)


class Beneficiary(db.Model):
    __tablename__ = 'beneficiary' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    beneficiary_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    name = db.Column(db.String, nullable = False)
    account_number = db.Column(db.String, nullable = False)


class Bank_employee(db.Model):
    __tablename__ = 'bank_employee' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.Integer, default =2)
    date_of_regn = db.Column(db.DateTime, default = datetime.now)
    contact_number = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Active') # Active - 1, Flagged - 2, Blocked - 3
    manager_id = db.Column(db.Integer,db.ForeignKey('bank_manager.id'), nullable = False)
    tasks = db.relationship('Task', backref = 'bank_employee', lazy = True)
    


class Bank_manager(db.Model):
    __tablename__ = 'bank_manager' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.Integer, default =2)
    date_of_regn = db.Column(db.DateTime, default = datetime.now)
    contact_number = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Active') # Active - 1, Flagged - 2, Blocked - 3
    # manager_id = db.Column(db.Integer,primary_key=True)
    employees = db.relationship('Bank_employee', backref = 'bank_manager', lazy = True)



class Task(db.Model):
    __tablename__ = 'task'
    id=db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('bank_employee.id'), nullable = False)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    # flag_sp = db.Column(db.Integer, default = 0) # Flagged - 1, not flagged - 0
    assigned_date = db.Column(db.DateTime, default = datetime.now) # NEED TO CONFIRM on type
    priority = db.Column(db.String, nullable = False)
    remarks = db.Column(db.String)
    due_date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String, default = 'Pending') # Pending, Complete


class Issue(db.Model):
    __tablename__ = 'issue'
    id=db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    assigned_date = db.Column(db.DateTime, default = datetime.now) # NEED TO CONFIRM on type
    status = db.Column(db.String, default = 'Pending') # Pending, Complete


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id=db.Column(db.Integer,primary_key=True)
    from_customer = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    to_customer = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    flag = db.Column(db.Integer, nullable = False) # Time in hours
    category = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Active') # Active - 1, Flagged - 2, Blocked - 3
    type = db.Column(db.String) 


class Document(db.Model):
    __tablename__ = 'document'
    id=db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    flag = db.Column(db.Integer, nullable = False) # Time in hours
    pan_number = db.Column(db.String, nullable = False)
    aadhar_number = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    upload_date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String) 


class Spending_category(db.Model):
    __tablename__ = 'spending_category'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    

# class LLM_interaction(db.Model):
#     __tablename__ = 'llm_interaction'
#     id=db.Column(db.Integer,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable = False)
#     ask_msg = db.Column(db.String, nullable = False)
#     response_msg = db.Column(db.String, nullable = False)
#     msg_time = db.Column(db.Float, nullable = False) # Time in hours
#     response_time = db.Column(db.Float, nullable = False) # Time in hours
    