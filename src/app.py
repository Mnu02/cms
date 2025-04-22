from db import db
from flask import Flask
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
