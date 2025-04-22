from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Course object
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a Course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }
    
class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }
    
class Assignment(db.Model):
    """
    Assignment Model
    """
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize an Assignment object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", None)

    def serialize(self):
        """
        Serialize an Assignment object
        """
        return {
            "id": self.id, 
            "title": self.title,
            "due_date": self.due_date
        }
