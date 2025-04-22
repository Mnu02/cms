from db import db
from flask import Flask, request
from db import db, Course, User, Assignment

import json

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(body, code=200):
    return json.dumps(body), code

def failure_response(message, code=404):
    return json.dumps({'error': message}), code

# your routes here

@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    Get all courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})


@app.route("/api/courses/", methods=["POST"])
def create_a_course():
    """
    Create a course
    """
    body = request.get_json()
    course_code = body.get("code", None)
    course_name = body.get("name", None)

    if course_code is None:
        return failure_response("course code is required", 400)
    if course_name is None:
        return failure_response("course name is required", 400)
    
    new_course = Course(
        code = course_code,
        name = course_name
    )
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_specific_course(course_id):
    """
    Get a specific course
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found", 400)
    return success_response(course.serialize(), 200)


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_specific_course(course_id):
    """
    Delete a course with id `course_id`
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found", 400)
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize(), 200)


@app.route("/api/users/", methods=["POST"])
def create_a_user():
    """
    Create a user
    """
    body = request.get_json()
    user_name = body.get("name", None)
    user_netid = body.get("netid", None)

    if user_name is None:
        return failure_response("User name is required", 400)
    if user_netid is None:
        return failure_response("User netid is required", 400)
    
    new_user = User(
        name = user_name,
        netid = user_netid
    )

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_specific_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 400)
    return success_response(user.serialize(), 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
