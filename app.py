from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
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

def __repr__(self):
        return "ID: {0} | Material Type: {1} |  Call Number: {2} |  Title: {3} | Author: {4} | Publisher: {5} | Copyright: {6} | ISBN: {7} | Description: {8}".format(self.ID, self.materialType, self.callNumber, self.title, self.author, self.publisher, self.copyright, self.ISBN, self.description)

class MaterialsForm(FlaskForm):
    ID = IntegerField('ID:')
    materialType = StringField('Material Type:', validators=[DataRequired()])
    callNumber= StringField('Call Number:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    author = StringField('Title:', validators=[DataRequired()])
    publisher = StringField('Title:', validators=[DataRequired()])
    copyright = StringField('Title:', validators=[DataRequired()])
    ISBN = StringField('Title:', validators=[DataRequired()])
    description = StringField('Title:')#data can be null for the descritpion so didnt know if we had to do a validator on it?


@app.route('/') #I'm not sure what the app route would be for our database design
def index():
    all_materials = g3_materials.query.all()
    return render_template('index.html',  materials=all_materials, pageTitle='Materials')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        print(search_value)
        search = "%{}%".format(search_value)
        print(search)
        results = g3_materials.query.filter(g3_materials.ID.like(search)).all()
        #or
        return render_template('index.html', materials=results, pageTitle='Materials Search', legend='Search Results')
    else:
        return redirect('/')

@app.route('/add_materials', methods=['GET', 'POST'])
def add_materials():
    form = MaterialsForm()
    if form.validate_on_submit():
            player = g3_materials(ID=form.ID.data, materialType=form.materialType.data, callNumber=form.callNumber.data, title=form.title.data, author=form.author.data, publisher=form.publisher.data, copyright=form.copyright.data, ISBN=form.ISBN.data,
                description=form.description.data)
            db.session.add(materials)
            db.session.commit()
            return redirect('/')

    return render_template('add_materials.html', form=form, pageTitle='Add A New Material')

@app.route('/delete_materials/<int:ID>', methods=['GET','POST'])
def delete_materials(ID):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        player = g3_materials.query.get_or_404(ID)
        db.session.delete(materials)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect

@app.route('/materials/<int:materialsID>/update', methods=['GET','POST']) #materialsID comes from update materials page
def update_materials(materialsID):
    materials = g3_materials.query.get_or_404(materialsID)
    form = MaterialsForm()
    if form.validate_on_submit(): #
        materials.ID=form.ID.data
        materials.materialType = form.materialType.data
        materials.callNumber = form.callNumber.data
        materials.title = form.title.data
        materials.author = form.author.data
        materials.publisher = form.publisher.data
        materials.copyright = form.copyright.data
        materials.ISBN = form.ISBN.data
        materials.description = form.description.data
        db.session.commit()
        flash('Your materials have been updated.')
        return redirect(url_for('get_materials', materialsID=materials.ID))
    #elif request.method == 'GET':
    form.ID.data = materials.ID
    form.materialType.data = materials.materialType
    form.callNumber.data = materials.callNumber
    form.title.data = materials.title
    form.author.data = materials.author
    form.publisher.data = materials.publisher
    form.copyright.data = materials.copyright
    form.ISBN.data = materials.ISBN
    form.description.data = materials.description
    return render_template('update_materials.html', form=form, pageTitle='Update Materials',
                            legend="Update Materials")

@app.route('/materials/<int:materialsID>', methods=['GET','POST'])
def get_materials(materialsID):
    materials = g3_materials.query.get_or_404(materialsID)
    return render_template('materials.html', form=materials, pageTitle= 'Materials Details', legend='Details Page')

#form= materials could be different if Isaac uses {% if material (s)%} in index

if __name__ == '__main__':
    app.run(debug=True)
