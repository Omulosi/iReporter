"""

app.decorators
~~~~~~~~~~~~~~

Custom decorators

"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User
from app.api.v2.common.utils import raise_error

def admin_required(fn):
    """
    Checks user is admin status is True before allowing access
    to endpoint
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        USER = User()
        verify_jwt_in_request()
        user_name = get_jwt_identity()
        user = USER.filter_by('username', user_name)
        if not user.get('isadmin'):
            return raise_error(403, 'Only admins can access this endpoint')
        return fn(*args, **kwargs)
    return wrapper