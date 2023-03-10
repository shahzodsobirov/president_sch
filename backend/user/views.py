from app import *
import backend.models.basics_models
from backend.basics.settings import *
from datetime import datetime


def date():
    data = datetime.now()
    dt_string = f'{int(data.year)}'
    date_year = datetime.strptime(dt_string, "%Y")
    dt_month_string = f'{int(data.year)}/{int(data.month)}'
    date_month = datetime.strptime(dt_month_string, "%Y/%m")
    dt_day_string = f'{int(data.year)}/{int(data.month)}/{int(data.day)}'
    date_day = datetime.strptime(dt_day_string, "%Y/%m/%d")
    year = Year.query.filter(Year.date == date_year).first()
    month = Month.query.filter(Month.date == date_month).first()
    day = Day.query.filter(Day.date == date_day).first()
    # print(date_object)
    if not year:
        year = Year(date=date_year)
        db.session.add(year)
        db.session.commit()
        if not month:
            month = Month(date=date_month, year_id=year.id)
            db.session.add(month)
            db.session.commit()
            if not day:
                day = Day(date=date_day, month_id=month.id)
                db.session.add(day)
                db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def home_page():
    date()
    return render_template('home page/home page.html')


@app.route('/role', methods=['POST', 'GET'])
def role():
    if request.method == "POST":
        name = request.form.get('name')
        add = Role(name=name)
        db.session.add(add)
        db.session.commit()
    return render_template('user/role/role.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    data = datetime.now()
    year = Year.query.filter(Year.name == data.strftime("%Y")).first()
    month = Month.query.filter(Month.name == data.strftime("%m")).first()
    day = Day.query.filter(Day.name == data.strftime("%d")).first()
    print(data.strftime("%m"))
    if request.method == "POST":
        name = request.form.get('name')
        role_id = request.form.get('role')
        add = User(name=name, role_id=role_id, year_id=year.id, month_id=month.id, day_id=day.id)
        db.session.add(add)
        db.session.commit()
    roles = Role.query.all()
    return render_template('user/register/register.html', roles=roles)


@app.route('/permission', methods=['POST', 'GET'])
def permission():
    if request.method == "POST":
        name = request.form.get('name')
        add = Permission(name=name)
        db.session.add(add)
        db.session.commit()
    return render_template('user/permission/permission.html')


@app.route('/user_actions', methods=['POST', 'GET'])
def user_actions():
    users = User.query.all()

    return render_template('user/actions/actions.html', users=users)


@app.route('/add_actions/<int:user_id>', methods=['POST', 'GET'])
def add_actions(user_id):
    print(user_id)
    user = User.query.filter(User.id == user_id).first()
    permissions = Permission.query.all()
    if request.method == "POST":
        action = request.form.get('action')
        action_id = Permission.query.filter(Permission.id == action).first()
        user.user_actions.append(action_id)
        db.session.commit()
    return render_template('user/actions/add_action.html', permissions=permissions, user=user)


@app.route('/classroom', methods=['POST', 'GET'])
def classroom():
    if request.method == "POST":
        name = request.form.get('name')
        add = Class(name=name)
        db.session.add(add)
        db.session.commit()
    return render_template('user/class/add_class.html')


@app.route('/choose_classroom', methods=['POST', 'GET'])
def choose_classroom():
    users = User.query.all()
    return render_template('user/class/choose_classroom.html', users=users)


@app.route('/add_user_classroom/<int:user_id>', methods=['POST', 'GET'])
def add_user_classroom(user_id):
    user = User.query.filter(User.id == user_id).first()
    classrooms = Class.query.all()
    if request.method == "POST":
        classroom = request.form.get("class")
        class_id = Class.query.filter(Class.id == classroom).first()
        user.user_class.append(class_id)
        db.session.commit()
    return render_template('user/class/add_user.html', user=user, classrooms=classrooms)
