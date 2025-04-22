from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.model):
    """
    Course Model
    """
    ___tablename___ = "courses"
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