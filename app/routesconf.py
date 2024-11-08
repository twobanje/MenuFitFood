from flask_login import LoginManager
from .models import Staff


staff_login_manager = LoginManager()

def setup_staff_login_manager(app):
    staff_login_manager.init_app(app)
    staff_login_manager.login_view = 'staff.slogin'

    @staff_login_manager.user_loader
    def load_user(user_id):
        return Staff.query.get(int(user_id))
