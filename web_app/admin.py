from flask import Flask, render_template, request, redirect, Blueprint, g
from .models import User
from .db import db


bp = Blueprint('admin_views', __name__, url_prefix='/admin')

@bp.route("/")
def show_users():
  # TODO: login shield
  users = User.query.all()
  return render_template("admin/users.html", users=users)

@bp.route("/<id>")
def edit_users(id):
  # TODO: login shield
  user = db.get_or_404(User, id)
  return render_template("admin/update_user.html", user=user)
