import base64
from functools import wraps
from flask import Flask, abort, g, render_template, request, redirect, escape, Blueprint, session, jsonify, make_response, flash, url_for
from database.class_models import *
from database.user_options import access_logs, add_new_user, get_user_by_psu_id, remove_user, read_all_machines, edit_machine, add_machine, remove_machine, change_user_access_level, check_user_password, get_user, read_all, add_training
from sqlalchemy.orm.exc import NoResultFound
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, RadioField
import datetime
from . import card_reader
# from wtforms.validators import DataRequired

bp = Blueprint('views', __name__)
# bp.config['SECRET_KEY'] = "asdfghjkl"


@bp.route("/")
def index():
    print(g.user)
    if g.user is None:
        next = url_for("views.dashboard")
        if request.args.get('next') is not None:
            next = request.args.get('next')
        return redirect(url_for('views.login', next=next))
    else: 
        return redirect(url_for('views.dashboard'))

@bp.errorhandler(403)
def access_denied(e):
    flash(str(e), "error")
    return render_template('access-denied.html', next=url_for(request.endpoint), no_sidebar=True, no_navbar=True), 403


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        password = request.form['password']

        # Verify password
        try:
            user = check_user_password(user_email, password)
        except Exception as e:
            flash(str(e), "error")
            user = None

        if user is None:
            return render_template("login.html")
        else:
            session["user_id"] = user.id
            redirect_arg = request.args.get('next')
            if redirect_arg is None:
                return redirect("/", code=302)
            else:
                return redirect(redirect_arg, code=302)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('views.index', next=request.args.get('next')))

admin_bp = Blueprint('admin_views', __name__, url_prefix='/admin')


def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or not g.user.has_manager():
            abort(403, description="This action is only allowed for managers or admins.")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or not g.user.has_admin():
            abort(403, description="This action is only allowed for admins.")
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/")
@admin_required
def show_users():
  # Now can access the user with g.user
  users = read_all()
  print(users)
  return render_template("admin/users.html", users=users)

@bp.route("/add-user-form/", methods=['POST', 'GET'])
@manager_required
def add_user_form():
    if request.method == "POST":
        # TODO (if time): Function call to get badge number by scanning in
        # Otherwise, proceed with getting inputs via manual entry
        user_id = request.form['id']
        user_badge = request.form['badge']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']
        try:
            # Potential TODO: Change role from Admin to Student for this form (not sure why it's Admin currently)
            add_new_user(psu_id=user_id, access=user_badge, firstname=user_fname,
                         lastname=user_lname, email=user_email, role="Student")
            flash("User Added Successfully", "success")
            return redirect(url_for('views.add_user_form'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('views.add_user_form'))

    else:
        return render_template("add_user_form.html")


@bp.route("/dashboard/")
@manager_required
def dashboard():
    # TODO: Filter these results by today
    logs = access_logs()
    return render_template("dashboard.html", logs=logs)

#TODO: Add get parameters for time range
@bp.route("/event-log-csv/")
@manager_required
def event_log_csv():
    #TODO: get time range from get parameters and pass them here
    logs = access_logs()
    response = make_response(render_template("event_log.csv", logs=logs))
    #TODO adjust file name based on time range
    file_name = "event_log.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    response.headers["Content-Type"] = "text/csv"
    return response

@bp.route("/equipOverview/")
@manager_required
def equipOverview():
    categories = all_categories()
    uncategorized = uncategorized_machines()
    return render_template("equipOverview.html", categories=categories, uncategorized=uncategorized)


@bp.route("/equipOverview/student/")
@manager_required
def equipStudent():
    return render_template("equipStudent.html")


@bp.route("/permissions/", methods=['POST', 'GET'])
@manager_required
def permissions():
    if request.method == "POST":
        try:
            user_badge = request.form['badge']
            user = get_user(user_badge)
            return redirect(url_for('views.permissionsStudent', badge=user_badge))
        except ValueError as e:
            flash(str(e), "error")
            return render_template("permissions.html")
    else:
        return render_template("permissions.html")


@bp.route("/waiver/")
@manager_required
def waiver():
    return render_template('waiver.html')


# Route for the card reader test page
@bp.route("/card_test/", methods=['GET'])
def card_test():
    return render_template('card_test.html')
# Route for checking the queue where card data gets read to
# Using flask.make_response and flask.jsonify to create an http response header.
# https://tedboy.github.io/flask/generated/flask.make_response.html
# https://tedboy.github.io/flask/generated/flask.jsonify.html
# https://api.jquery.com/ (Used in card_test.html to update page)

@bp.route("/card_data/")
def card_data():
    card_data = card_reader.get_data()
    if card_data is not None:
        card_number, facility_code = card_data
    else:
        card_number, facility_code = None, None
    return jsonify(card_number=card_number, facility_code=facility_code)

    
@bp.route("/permissions/<id>/")
@manager_required
def permissionsStudent(id):
    user = get_user_by_psu_id(id)
    categories = all_categories()
    uncategorized = uncategorized_machines()
    for category in categories:
        category.machines = list(filter(lambda machine: machine not in user.machines, category.machines))
        if category.machines == []:
            categories.remove(category)
    uncategorized = list(filter(lambda machine: machine not in user.machines, uncategorized))
    return render_template("permissionsStudent.html", user=user, categories=categories, uncategorized=uncategorized)

@bp.route("/edit_user/")
@manager_required
def edit_user():
    return render_template('edit_user.html')


@bp.route('/remove-user/', methods=['GET', 'POST'])
@manager_required
def remove_user_form():
    if request.method == "POST":
        user_badge = request.form['badge']
        try:
            remove_user(user_badge)
            flash("User Removed Successfully", "success")
            return redirect(url_for('views.remove_user_form'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('views.remove_user_form'))
    else:
        return render_template("remove_user_form.html")

# Creating a form for promoting a user


class PromoteForm(FlaskForm):
    id = StringField("Enter PSU ID", [validators.DataRequired()])
    role = RadioField('Role', choices=[('Admin','Admin'),('Manager','Manager')], validators=[validators.DataRequired()])
    password = StringField("Add a password")
    submit = SubmitField("Update")

# Create a Promote Page


@bp.route("/promote", methods=["POST", "GET"])
@admin_required
def promote_user():
    id = None
    role = None
    form = PromoteForm()
    # Validate Form
    if form.validate_on_submit():
        id = form.id.data
        role = form.role.data
        password = form.password.data
        if password == "":
            password = None
        print(role)
        if (role):
            try:
                change_user_access_level(id, role, password)
                flash("Successfully updated")
                return redirect('/promote')
            except Exception as e:
                flash(str(e), "error")
                return render_template("promote_user.html", id=id, role=role, form=form)

    return render_template("promote_user.html", id=id, role=role, form=form)


@bp.route('/manage-equipment/')
@manager_required
def manage_equipment():
    all_machine_data = read_all_machines()
    categories = all_categories()
    return render_template("manage_equipment.html", machines=all_machine_data, categories=categories)


@bp.route('/update-equipment/', methods=['POST'])
@manager_required
def update_equipment():
    equipment_id = request.form.get("equipment_id")
    equipment_name = request.form.get("equipment_name")
    equipment_link = request.form.get("epl_link")
    category_ids = request.form.getlist("categories")
    img = request.files.get("equipment_image")
    if equipment_id is None or equipment_id == "":
        flash("Malformed request, missing equipment_id", "error")
    elif equipment_name is None or equipment_name == "":
        flash("Equipment name cannot be empty", "error")
    else:
        try:
            edit_machine(int(equipment_id), equipment_name, equipment_link, category_ids, img)
            flash("Equipment Updated Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))

@bp.route('/insert-equipment/', methods=['POST'])
@manager_required
def insert_equipment():
    equipment_name = request.form['equipment_name']
    equipment_link = request.form['epl_link']
    if equipment_link == "":
        equipment_link = None
    category_ids = request.form.getlist('categories')
    img = request.files.get('equipment_image')
    if equipment_name is None or equipment_name == "":
        flash("Equipment name cannot be empty", "error")
    else:
        try:
            add_machine(equipment_name, equipment_link, category_ids, img)
            flash("Equipment Added Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))


@bp.route('/remove-equipment/<id>', methods=['GET', 'POST'])
@manager_required
def remove_equipment(id):
    try:
        remove_machine(id)
        flash("Equipment Removed Successfully", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))


@bp.route('/update_category/', methods=['POST'])
@manager_required
def update_category():
    id = request.form['category_id']
    name = request.form['category_name']
    if name is None or name == "" or id is None or id == "":
        flash("Category name or ID cannot be empty", "error")
    else:
        try:
            update_category_by_id(id, name)
            flash("Category updated Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))


@bp.route('/insert_category/', methods=['POST'])
@manager_required
def insert_category():
    name = request.form['category_name']
    if name is None or name == "":
        flash("Category name cannot be empty", "error")
    else:
        try:
            insert_category_name(name)
            flash("Category Added Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))

@bp.route('/remove-category/<id>', methods=['GET', 'POST'])
@manager_required
def remove_category(id):
    try:
        remove_category_by_id(id)
        flash("Category Removed Successfully", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))

@bp.route('/training-session/')
@manager_required
def training_session():
    all_machine_data = read_all_machines()
    return render_template('training_session.html', machines=all_machine_data)

@bp.route('/training-session/<int:machine_id>/', methods= ['GET', 'POST'])
@manager_required
def training_session_details(machine_id):
    if request.method == 'POST':
        try:
    
            user_badge = request.form['badge']
            add_training(user_badge, machine_id)
            flash(f"Training for user with Badge {user_badge} updated successfully", "success")
            return redirect(url_for('views.training_session_details', machine_id=machine_id, name=name))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('views.training_session_details', machine_id=machine_id))

    else:
        machine = get_machine(machine_id)
        return render_template('training_session_details.html', machine=machine)
