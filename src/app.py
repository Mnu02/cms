from db import db
from flask import Flask, request, jsonify
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
    return jsonify(body), code

def failure_response(message, code=404):
    return jsonify({"error": message}), code
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
    body = request.get_json(force=True)
    if body is None:
        return failure_response("Request body must be JSON", 400)
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
        return failure_response("Course not found", 404)
    return success_response(course.serialize(), 200)


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_specific_course(course_id):
    """
    Delete a course with id `course_id`
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found", 404)
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize(), 200)


@app.route("/api/users/", methods=["POST"])
def create_a_user():
    """
    Create a user
    """
    body = request.get_json(force=True)
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
    """
    Get a specific user with id `user_id`
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 404)
    return success_response(user.serialize(), 200)


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Add a user to a course with id `course_id`
    """
    data = request.get_json(force=True)
    user_id = data.get("user_id", None)
    user_type = data.get("type", None)

    if user_id is None:
        return failure_response("User field is required", 400)
    if user_type is None or user_type not in ["student", "instructor"]:
        return failure_response("Type field not provided or invalid type", 400)
    
    course = Course.query.get(course_id)
    user = User.query.get(user_id)

    if course is None:
        return failure_response("Course not found", 404)
    if user is None:
        return failure_response("User not found", 404)
    
    if user_type == "student":
        if user not in course.students:
            course.students.append(user)
    elif user_type == "instructor":
        if user not in course.instructors:
            course.instructors.append(user)
    
    db.session.commit()
    return success_response(course.serialize(), 200)
    

@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    Create an assignment for a course with id `course_id`
    """
    data = request.get_json(force=True)
    ass_title = data.get("title", None)
    ass_due_date = data.get("due_date", None)

    if ass_title is None:
        return failure_response("title is required", 400)
    if ass_due_date is None:
        return failure_response("due date is required", 400)
    
    new_assignment = Assignment(
        title=ass_title,
        due_date=ass_due_date,
        course_id=course_id
    )

    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
