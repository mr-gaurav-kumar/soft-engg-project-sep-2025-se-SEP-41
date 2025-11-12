from flask import current_app as app
from flask_restful import Api, Resource, reqparse 
# In route, we used request.get_json(), here, we are using reqparse is required to define what 
# details/ attributes we want to extract from the request body
from .models import *
from flask_security import current_user, auth_required, roles_required, roles_accepted
from .util_funcs import roles_list

api = Api()

cache = app.cache

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


#### CHAPTER end points ####
ch_parser = reqparse.RequestParser()
ch_parser.add_argument('name')
ch_parser.add_argument('description')

class ChApi(Resource):
    @auth_required('token')
    @roles_accepted('admin', 'user')
    def get(self, sub_id):
        chapters = [] # stores list of objects of class Chapter
        ch_jsons = []
        chapters = Chapter.query.filter(Chapter.subject_id == sub_id).all()
        # convering every object of class Chapter into a disctionary
        for ch in chapters:
            this_ch = {}
            this_ch["id"] = ch.id
            this_ch["name"] = ch.name
            this_ch["description"] = ch.description
            ch_jsons.append(this_ch)
        if ch_jsons:
            return ch_jsons
        else:
            return {
                "message": "No chapters found!"
            }, 404
    
    @auth_required('token')
    @roles_required('admin')
    def post(self, sub_id):
        try:
            args = ch_parser.parse_args()
            ch = Chapter(name = args["name"],
                        description = args["description"],
                        subject_id = sub_id)
            db.session.add(ch)
            db.session.commit()
            return {
                "message": "Chapter created successfully"
            }
        
        except:
            return {
                "message": "All fields are not provided"
            }, 400

    @auth_required('token')
    @roles_required('admin')
    def put(self, ch_id):
        ch_exists = Chapter.query.filter(Chapter.id == ch_id).first()
        if ch_exists:
            args = ch_parser.parse_args()
            ch_exists.name = args["name"]
            ch_exists.description = args["description"]
            db.session.commit()
            return {
                "message": "The chapter updated successfully"
            }

        else:
            return {
                "message": "The chapter does not exist"
            }, 404
        
    @auth_required('token')
    @roles_required('admin')
    def delete(self, ch_id):
        ch_exists = Chapter.query.filter(Chapter.id == ch_id).first()
        if ch_exists:
            db.session.delete(ch_exists)
            db.session.commit()
            return {
                "message": "The chapter deleted successfully"
            }

        else:
            return {    
                "message": "The chapter does not exist"
            }, 404
        
api.add_resource(ChApi, '/api/chapter/get/<int:sub_id>', '/api/chapter/create/<int:sub_id>', '/api/chapter/update/<int:ch_id>', '/api/chapter/delete/<int:ch_id>')

