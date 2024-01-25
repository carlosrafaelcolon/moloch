from werkzeug.security import check_password_hash, generate_password_hash
from server.models import User



class UserController():
    @staticmethod
    def create_user(email, password):
        hashed_password = generate_password_hash(password)
        user = User.create(email=email, password=hashed_password)
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.find_by(email=email)
        if user and check_password_hash(user.password, password):
            return user
        else:
            return None
    
    