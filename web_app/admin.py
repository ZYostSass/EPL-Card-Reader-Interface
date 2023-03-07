from flask import Flask, render_template, request, redirect, Blueprint, g
from .models import User
from .db import db


bp = Blueprint('admin_views', __name__, url_prefix='/admin')

@bp.route("/")
def show_users():
  users = User.query.all()
  return render_template("admin/users.html", users=)
