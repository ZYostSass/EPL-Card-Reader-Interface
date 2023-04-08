from functools import wraps

from flask import Flask, render_template, request, redirect, Blueprint, g, url_for, session, current_app
from .models import User
from .db import db


bp = Blueprint('admin_views', __name__, url_prefix='/admin')

@current_app.before_request
def set_user_global():
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    if user_id is None:
        g.user = None
    else:
        g.user = user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/")
@login_required
def show_users():
  # Now can access the user with g.user
  users = User.query.all()
  return render_template("admin/users.html", users=users)

@bp.route("/<id>")
@login_required
def edit_users(id):
  # Now can access the currently logged in user with g.user
  user = db.get_or_404(User, id)
  return render_template("admin/update_user.html", user=user)
