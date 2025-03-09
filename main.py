
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Workplace(db.Model):
    __tablename__ = 'workplace'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    workers = db.relationship('Worker', backref='workplace')

    @property
    def workers_quantity(self):
        return len(self.workers)

    def __init__(self, name, city):
        self.name = name
        self.city = city

    def __repr__(self):
        return f'{self.id} {self.name} {self.city} {self.workers_quantity}'

class Worker(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String)
    lastname = db.Column(db.String)
    position = db.Column(db.String)
    workplace_id = db.Column(db.Integer, db.ForeignKey('workplace.id'), nullable=False)


    def __init__(self, person_name, lastname, position, workplace_id):
        self.person_name = person_name
        self.lastname = lastname
        self.position = position
        self.workplace_id = workplace_id

    def __repr__(self):
        return f'{self.id} {self.person_name} {self.lastname} {self.position} {self.workplace_id}'


with app.app_context():
    db.create_all()
########
@app.route('/')
def workplace_list():
    workplaces = Workplace.query.all()
    return render_template('index.html', workplaces = workplaces)

@app.route('/workplace/<int:id>')
def workplace_view(id):
    workplace = Workplace.query.get(id)
    return render_template('workplace_card.html',workplace = workplace)

@app.route('/add-workplace', methods=['GET', 'POST'])
def add_workplace():
    if request.method == 'GET':
        return render_template('add_workplace.html')
    elif request.method == 'POST':
        name = request.form.get('nameinput')
        city = request.form.get('cityinput')
        new_workplace = Workplace(name, city)
        db.session.add(new_workplace)
        db.session.commit()
        return redirect(url_for('workplace_list'))

@app.route('/edit-workplace/<int:id>', methods=['GET', 'POST'])
def edit_workplace(id):
    workplace_row = Workplace.query.get(id)
    if not workplace_row:
        return 'Project is not in list'
    if request.method == 'GET':
        return render_template('edit_workplace.html', workplace_row = workplace_row)
    if request.method == 'POST':
        name = request.form.get('nameinput')
        city = request.form.get('cityinput')
        workplace_row.name = name
        workplace_row.city = city
        db.session.commit()

        return redirect(url_for('workplace_list'))

@app.route('/delete-workplace/<int:id>', methods=['POST'])
def delete_workplace(id):
    workplace_row = Workplace.query.get(id)
    if workplace_row.workers:
        return('Workplace has workers')
    db.session.delete(workplace_row)
    db.session.commit()
    return redirect(url_for('workplace_list'))
######
@app.route('/workers-list')
def worker_list():
    workers = Worker.query.all()
    return render_template('workers_list.html', workers=workers)

@app.route('/add-worker', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'GET':
        return render_template('add_worker.html')
    elif request.method == 'POST':
        name = request.form.get('nameinput')
        lastname = request.form.get('lastnameinput')
        position = request.form.get('positioninput')
        company_id = int(request.form.get('companyidinput'))
        new_worker = Worker(name, lastname, position, company_id)
        db.session.add(new_worker)
        db.session.commit()
        return redirect(url_for('worker_list'))

@app.route('/edit-worker/<int:id>', methods=['GET', 'POST'])
def edit_worker(id):
    worker_row = Worker.query.get(id)
    if not worker_row:
        return 'Worker is not in list'
    if request.method == 'GET':
        return render_template('edit_worker.html', worker_row = worker_row)
    if request.method == 'POST':
        name = request.form.get('nameinput')
        lastname = request.form.get('lastnameinput')
        position = request.form.get('positioninput')
        company_id = int(request.form.get('companyidinput'))
        worker_row.name = name
        worker_row.lastname = lastname
        worker_row.position = position
        worker_row.company_id = company_id
        db.session.commit()
        return redirect(url_for('worker_list'))

@app.route('/delete-worker/<int:id>', methods=['POST'])
def delete_worker(id):
    worker_row = Worker.query.get(id)
    if worker_row:
        db.session.delete(worker_row)
        db.session.commit()
    return redirect(url_for('worker_list'))

app.run()