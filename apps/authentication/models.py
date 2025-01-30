from werkzeug.security import generate_password_hash, check_password_hash
from apps import get_db
from flask_login import UserMixin

class UserModel(UserMixin):
    @staticmethod
    def create_user(username, email, password):
        db = get_db()
        hashed_password = generate_password_hash(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        result = db.users.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_by_username(username):
        db = get_db()
        user = db.users.find_one({"username": username})
        if user:
            return UserModel(**user)
        return None

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    def __init__(self, username, email, password, _id=None):
        self.id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        user = db.users.find_one({"_id": user_id})
        if user:
            return UserModel(**user)
        return None
