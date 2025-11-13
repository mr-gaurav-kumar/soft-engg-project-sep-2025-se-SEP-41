from flask import current_app as app
from flask_restful import Api, Resource, reqparse 
# In route, we used request.get_json(), here, we are using reqparse is required to define what 
# details/ attributes we want to extract from the request body
from .models import *
from flask_security import current_user, auth_required, roles_required, roles_accepted
from .util_funcs import roles_list

api = Api()

cache = app.cache


# Employee - verify_doc - accept/ reject, update_task
# Manager - create_task, task_details, performance_details

task_parser = reqparse.RequestParser()
task_parser.add_argument('id')
task_parser.add_argument('employee_id')
task_parser.add_argument('customer_id')
task_parser.add_argument('due_date')
task_parser.add_argument('priority')

class TaskApi(Resource):
    @auth_required('token')
    @roles_accepted('admin','manager')
    def post(self):
        try:
            args = task_parser.parse_args()
            assigned_date = datetime.strptime(args["due_date"], "%Y-%m-%d").date()
            # customer_id = Customer.query.filter(Subject.id == sub_id).first()
            task = Task(title = args["name"],
                        customer_id = args["customer_id"],
                        employee_id = args["employee_id"],
                        assigned_date = datetime.strptime(datetime.datetime(), "%Y-%m-%d").date(),
                        status = "Pending"
                        due_date = assigned_date,
                        priority = args["priority"],
                        description = args["description"])
            db.session.add(task)
            db.session.commit()
            return {
                "message": "Task created successfully"
            }
        
        except:
            return {
                "message": "All fields are not provided or the subject provided already exists"
            }, 400



    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def get(self): # get for subjects is simply retreival operation, there is no request body
        # based on who is the user - normal user or admin, we want to get all subjects or only few, we need to modify for that
        tasks = [] # stores list of objects of class Subject
        task_jsons = []
        tasks = Task.query.all()
        # convering every object of class Subject into a disctionary
        for task in tasks:
            this_task = {}
            this_task["id"] = task.id
            this_task["name"] = task.title
            this_task["category"] = task.cataegory
            this_task["customer"] = task.customer.name
            this_task["employee"] = task.employee.name
            this_task["due_date"] = task.due_date

            task_jsons.append(this_task)
        if task_jsons:
            return task_jsons
        else:
            return {
                "message": "No tasks found"
            }, 404

api.add_resource(TaskApi, '/api/task/get', '/api/task/create')














#### SUBJECT end points ####
sub_parser = reqparse.RequestParser()
sub_parser.add_argument('name')
sub_parser.add_argument('description')

class SubApi(Resource):
# in routes, we can give anything as function name under the route, but here we need to give defined names
    @auth_required('token')
    @roles_accepted('admin', 'user')
    @cache.cached(timeout = 3, key_prefix = "subjects")
    def get(self): # get for subjects is simply retreival operation, there is no request body
        # based on who is the user - normal user or admin, we want to get all subjects or only few, we need to modify for that
        subjects = [] # stores list of objects of class Subject
        sub_jsons = []
        subjects = Subject.query.all()
        # convering every object of class Subject into a disctionary
        for sub in subjects:
            this_sub = {}
            this_sub["id"] = sub.id
            this_sub["name"] = sub.name
            this_sub["description"] = sub.description
            sub_jsons.append(this_sub)
        if sub_jsons:
            return sub_jsons
        else:
            return {
                "message": "No subjects found"
            }, 404
    
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        try:
            args = sub_parser.parse_args()
            sub = Subject(name = args["name"],
                        description = args["description"])
            db.session.add(sub)
            db.session.commit()
            return {
                "message": "Subject created successfully"
            }
        
        except:
            return {
                "message": "All fields are not provided or the subject provided already exists"
            }, 400

    @auth_required('token')
    @roles_required('admin')
    def put(self, sub_id):
        sub_exists = Subject.query.filter(Subject.id == sub_id).first()
        if sub_exists:
            args = sub_parser.parse_args()
            sub_exists.name = args["name"]
            sub_exists.description = args["description"]
            db.session.commit()
            return {
                "message": "The subject updated successfully"
            }

        else:
            return {
                "message": "The subject does not exist"
            }, 404
        
    @auth_required('token')
    @roles_required('admin')
    def delete(self, sub_id):
        sub_exists = Subject.query.filter(Subject.id == sub_id).first()
        if sub_exists:
            db.session.delete(sub_exists)
            db.session.commit()
            return {
                "message": "The subject deleted successfully"
            }

        else:
            return {
                "message": "The subject does not exist"
            }, 404

api.add_resource(SubApi, '/api/subject/get', '/api/subject/create', '/api/subject/update/<int:sub_id>', '/api/subject/delete/<int:sub_id>')