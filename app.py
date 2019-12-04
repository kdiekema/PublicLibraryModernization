from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_bootstrap import Bootstrap
import pymysql
import secrets
import datetime
from datetime import date




conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY']= 'aliq!#LiNE@*;oaf098023L(U)*8cer'
app.config['SQLALCHEMY_DATABASE_URI'] = conn

db = SQLAlchemy(app)


class g3_materials(db.Model):
    ID= db.Column(db.Integer, primary_key=True)
    materialType= db.Column(db.String(255))
    callNumber= db.Column(db.String(255))
    title= db.Column(db.String(255))
    author= db.Column(db.String(255))
    publisher= db.Column(db.String(255))
    copyright = db.Column(db.String(255))
    ISBN= db.Column(db.String(255))
    description= db.Column(db.String(255))

class group3_patrons(db.Model):
    patronID= db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(255))
    last_name= db.Column(db.String(255))
    birthdate= db.Column(db.Date)
    address1= db.Column(db.String(255))
    address2= db.Column(db.String(255))
    city = db.Column(db.String(255))
    state= db.Column(db.String(2))
    zip= db.Column(db.String(5))
    phone= db.Column(db.String(20))
    phone2= db.Column(db.String(20))
    email= db.Column(db.String(255))

class g3_circulation(db.Model):
    circulationID = db.Column(db.Integer, primary_key=True)
    patronsID = db.Column(db.ForeignKey('group3_patrons.patronID'))
    materialsID = db.Column(db.ForeignKey('g3_materials.ID'))
    checkoutDate = db.Column(db.Date)
    dueDate = db.Column(db.Date)

def __repr__(self):
        return "ID: {0} | Material Type: {1} |  Call Number: {2} |  Title: {3} | Author: {4} | Publisher: {5} | Copyright: {6} | ISBN: {7} | Description: {8}".format(self.ID, self.materialType, self.callNumber, self.title, self.author, self.publisher, self.copyright, self.ISBN, self.description)

class MaterialsForm(FlaskForm):
    ID = IntegerField('ID:')
    materialType = StringField('Material Type:', validators=[DataRequired()])
    callNumber= StringField('Call Number:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    author = StringField('Author:')
    publisher = StringField('Publisher:', validators=[DataRequired()])
    copyright = StringField('Copyright:')
    ISBN = StringField('ISBN:')
    description = StringField('Description:')

class PatronsForm(FlaskForm):
    patronID = IntegerField('Patron ID:')
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name= StringField('Last Name:', validators=[DataRequired()])
    birthdate = DateField('Birthdate:', validators=[DataRequired()])
    address1 = StringField('Address 1:', validators=[DataRequired()])
    address2 = StringField('Address 2:')
    city = StringField('City:', validators=[DataRequired()])
    state = StringField('State:', validators=[DataRequired()])
    zip = StringField('Zip:', validators=[DataRequired()])
    phone = StringField('Phone 1:')
    phone2 = StringField('Phone 2:')
    email = StringField('Email:')

class CirculationForm(FlaskForm):
    circulationID = IntegerField('Circulation ID:')
    patronsID = IntegerField('Patron ID:',  validators=[DataRequired()])
    materialsID = IntegerField('Material ID:',  validators=[DataRequired()])
    checkoutDate = DateField('Checkout Date:',  validators=[DataRequired()] )
    dueDate = DateField('Due Date:',  validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', pageTitle='About')

@app.route('/patrons')
def patrons():
    all_patrons= group3_patrons.query.all()
    return render_template('patrons.html', patrons=all_patrons, pageTitle="Patrons")

@app.route('/search_patrons', methods=['GET', 'POST'])
def search_patrons():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = group3_patrons.query.filter(or_(group3_patrons.last_name.like(search), group3_patrons.email.like(search), group3_patrons.phone.like(search), group3_patrons.phone2.like(search))).all()
        return render_template('patrons.html', patrons=results, pageTitle='Patrons')
    else:
        return redirect('/patrons')

@app.route('/add_patrons', methods=['GET','POST'])
def add_patrons():
    form = PatronsForm()
    if form.validate_on_submit():
        patron = group3_patrons(first_name=form.first_name.data, last_name=form.last_name.data, birthdate= form.birthdate.data, address1=form.address1.data, address2=form.address2.data, city = form.city.data, state = form.state.data, zip = form.zip.data, phone = form.phone.data, phone2 = form.phone2.data, email = form.email.data)
        db.session.add(patron)
        db.session.commit()
        return redirect('/')

    return render_template('add_patrons.html', form=form, pageTitle='Add Patron')


@app.route('/patron/<int:patronID>', methods=['GET','POST'])
def patron(patronID):
    patron = group3_patrons.query.get_or_404(patronID)
    return render_template('patron.html', form=patron, pageTitle='Patron Details')

@app.route('/patron/<int:patronID>/update', methods=['GET','POST'])
def update_patrons(patronID):
    patron = group3_patrons.query.get_or_404(patronID)
    form = PatronsForm()
    if form.validate_on_submit():
       patron.patronID=form.patronID.data
       patron.first_name = form.first_name.data
       patron.last_name = form.last_name.data
       patron.birthdate = form.birthdate.data
       patron.address1 = form.address1.data
       patron.address2 = form.address2.data
       patron.city = form.city.data
       patron.state = form.state.data
       patron.zip = form.zip.data
       patron.phone = form.phone.data
       patron.phone2 = form.phone2.data
       patron.email = form.email.data
       db.session.commit()
       flash('Your patron has been updated.')
       return redirect(url_for('patron', patronID=patron.patronID))
    #elif request.method == 'GET':
    form.patronID.data = patron.patronID
    form.first_name.data = patron.first_name
    form.last_name.data = patron.last_name
    form.birthdate.data = patron.birthdate
    form.address1.data = patron.address1
    form.address2.data = patron.address2
    form.city.data = patron.city
    form.state.data = patron.state
    form.zip.data = patron.zip
    form.phone.data = patron.phone
    form.phone2.data = patron.phone2
    form.email.data = patron.email
    return render_template('update_patrons.html', form=form, pageTitle='Update Patrons',
                            legend="Update A Patron")

@app.route('/patron/<int:patronID>/delete', methods=['POST'])
def delete_patrons(patronID):
    if request.method == 'POST': #if it's a POST request, delete the pet from the database
        patron = group3_patrons.query.get_or_404(patronID)
        db.session.delete(patron)
        db.session.commit()
        flash('Patron was successfully deleted!')
        return redirect("/patrons")
    else: #if it's a GET request, send them to the home page
        return redirect("/patrons")






@app.route('/materials')
def materials():
    all_materials= g3_materials.query.all()
    return render_template('materials.html', materials=all_materials, pageTitle="Materials")

@app.route('/search_materials', methods=['GET', 'POST'])
def search_materials():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = g3_materials.query.filter(or_(g3_materials.title.like(search), g3_materials.materialType.like(search),g3_materials.author.like(search))).all()
        return render_template('materials.html', materials=results, pageTitle='Materials')
    else:
        return redirect('/materials')

@app.route('/add_material', methods=['GET','POST'])
def add_materials():
    form = MaterialsForm()
    if form.validate_on_submit():
        material = g3_materials(materialType=form.materialType.data, callNumber= form.callNumber.data, title=form.title.data, author=form.author.data, publisher = form.publisher.data, copyright = form.copyright.data, ISBN = form.ISBN.data, description = form.description.data)
        db.session.add(material)
        db.session.commit()
        return redirect('/materials')

    return render_template('add_materials.html', form=form, pageTitle='Add Materials')


@app.route('/material/<int:ID>', methods=['GET','POST'])
def material(ID):
    material = g3_materials.query.get_or_404(ID)
    return render_template('material.html', form=material, pageTitle='Material Details')

@app.route('/material/<int:ID>/update', methods=['GET','POST'])
def update_materials(ID):
    material = g3_materials.query.get_or_404(ID)
    form = MaterialsForm()
    if form.validate_on_submit():
        material.ID=form.ID.data
        material.materialType = form.materialType.data
        material.callNumber = form.callNumber.data
        material.title = form.title.data
        material.author = form.author.data
        material.publisher = form.publisher.data
        material.copyright = form.copyright.data
        material.ISBN = form.ISBN.data
        material.description = form.description.data
        db.session.commit()
        flash('Your material has been updated.')
        return redirect(url_for('material', ID=material.ID))
    #elif request.method == 'GET':
    form.ID.data=material.ID
    form.materialType.data = material.materialType
    form.callNumber.data = material.callNumber
    form.title.data = material.title
    form.author.data = material.author
    form.publisher.data = material.publisher
    form.copyright.data = material.copyright
    form.ISBN.data = material.ISBN
    form.description.data = material.description
    return render_template('update_materials.html', form=form, pageTitle='Update Materials',
                            legend="Update A Material")

@app.route('/material/<int:ID>/delete', methods=['POST'])
def delete_materials(ID):
    if request.method == 'POST': #if it's a POST request, delete the pet from the database
        material = g3_materials.query.get_or_404(ID)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/materials")
    else: #if it's a GET request, send them to the home page
        return redirect("/materials")

@app.route('/circulation')
def circulation():
    all_circulation= g3_circulation.query.all()
    return render_template('circulation.html', circulation=all_circulation, pageTitle="Circulation")

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    form = CirculationForm()
    if form.validate_on_submit():
        circulation = g3_circulation(patronsID=form.patronsID.data, materialsID= form.materialsID.data, checkoutDate=form.checkoutDate.data, dueDate=form.dueDate.data)
        db.session.add(circulation)
        db.session.commit()
        return redirect('/circulation')

    return render_template('checkout.html', form=form, pageTitle='Check Out')

@app.route('/checkin/<int:circulationID>', methods=['GET','POST'])
def checkin(circulationID):
    circulation = g3_circulation.query.get_or_404(circulationID)
    return render_template('checkin.html', form=circulation, pageTitle='Check In')

@app.route('/checkin/<int:circulationID>/confirm', methods=['POST'])
def confirm(circulationID):
    if request.method == 'POST':
        circulation = g3_circulation.query.get_or_404(circulationID)
        db.session.delete(circulation)
        db.session.commit()
        flash('Material was successfully checked in')
        return redirect("/circulation")
    else: #if it's a GET request, send them to the home page
        return redirect("/circulation")

@app.route('/overdue', methods=['GET', 'POST'])
def overdue():
        overdue = g3_circulation.query.filter(g3_circulation.dueDate<date.today())
        return render_template('circulation.html', circulation=overdue, pageTitle='Circulation')

@app.route('/due', methods=['GET', 'POST'])
def due():
    due = g3_circulation.query.filter(g3_circulation.dueDate==date.today())
    return render_template('circulation.html', circulation=due, pageTitle='Circulation')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    patroncount = group3_patrons.query.filter(group3_patrons.patronID).count()
    materialcount = g3_materials.query.filter(g3_materials.ID).count()
    circulationcount = g3_circulation.query.filter(g3_circulation.circulationID).count()
    return render_template('reports.html', patronspresent=patroncount, materialspresent = materialcount, circulationspresent = circulationcount, pageTitle='Report')


if __name__ == '__main__':
    app.run(debug=True)