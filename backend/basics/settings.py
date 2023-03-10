from app import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def get_current_user():
    user_result = None
    if 'username' in session:
        username = session['username']
        user = User.query.filter(User.username == username).first()
        user_result = user
    return user_result
