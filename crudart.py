import os
#from forms import  AddCat, EditCat
from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField, validators
from wtforms_sqlalchemy.fields import QuerySelectField

app = Flask(__name__)

# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

print(' ******* Sistema de Proveedores running ********* ')

############################################

        # SQL DATABASE AND MODELS
        # $env:FLASK_APP = "crudart"
##########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'provs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


  

# Database Models

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    subcats = db.relationship('Subcat', backref='cat', lazy='dynamic')
    arts = db.relationship('Art', backref='cat', lazy='dynamic')
    
    def __repr__(self):
       return f"(Cat: {self.name}, Id {self.id})"
      

    def __str__(self):
       #return f"(Cat: {self.name}, Id {self.id})"
       return self.name

    def report_subcats(self): 
        print("Subcats:")           
        for sc in self.subcats:
            print(f"(id: {sc.id}, Subcat: {sc.name})")  

    def report_arts(self): 
        print("Arts:")           
        for a in self.arts:
            print(f"(id: {a.id}, Art: {a.name})")                    


class Subcat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'))

    arts = db.relationship('Art', backref='subcat', lazy='dynamic')
    
    def __repr__(self):
       return f"(Subcat: {self.name}, Id {self.id})"

    def report_arts(self): 
        print("Arts:")           
        for art in self.arts:
            print(f"(id: {art.id}, Art: {art.name})")    

class Prov(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    arts = db.relationship('Art', backref='prov', lazy='dynamic')

    def __repr__(self):
       return f"(Prov: {self.name}, Id: {self.id})"

    def report_arts(self): 
        print("Arts:")           
        for art in self.arts:
            print(f"(id: {art.id}, Art: {art.name})")  
  

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float)

    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'))
    sc_id  = db.Column(db.Integer, db.ForeignKey('subcat.id'))
    prov_id = db.Column(db.Integer, db.ForeignKey('prov.id'))
       
    def __repr__(self):
       return f" Art: {self.name}, Price: {self.price}, {self.cat}, {self.subcat}, {self.id}"

############################################

        # FORMS

##########################################

class AddCat(FlaskForm):
    name = StringField('Categoría: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    submit = SubmitField('Agregar')

class EditCat(FlaskForm):
    name = StringField('Categoría: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    submit = SubmitField('Aceptar')

def cat_query():
    return Cat.query.order_by(Cat.name)


def get_pk(obj):
    return str(obj)  

class SelectCat(FlaskForm):
    cats = QuerySelectField(query_factory=cat_query,allow_blank=True, get_pk=get_pk)
    submit = SubmitField('Aceptar')     

class AddSubcat(FlaskForm):
    name = StringField('Subcategoría: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    cat_name = StringField('Categoría: ') 
    submit = SubmitField('Agregar')
       


############################################

        # ROUTES

##########################################


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/categorias', methods=['POST'])
def persiste_cat():
    form = AddCat()

    resCats=Cat.query.order_by(Cat.name).all()
    for cat in resCats:
        print(f"********** Id: {cat.id}, Categoria: {cat.name} ********")

    if form.validate_on_submit():
        catName= form.name.data.strip()
        print(f" **** Categoria: {catName} *****")

        existeCat=Cat.query.filter(Cat.name==catName).first()
        if existeCat:
            print(f"La categoria {catName} ya esta ingresada")
            return render_template('categorias.html',form=form,resCats=resCats,error='Ya existe categoria')   


        categoria = Cat(name=catName)
        db.session.add(categoria)
        db.session.commit()

        form.name.data = ''
        resCats=Cat.query.order_by(Cat.name).all()

        return render_template('categorias.html',form=form,resCats=resCats)    


    return render_template('categorias.html',form=form,resCats=resCats)    


@app.route('/categorias', methods=['GET'])
def categorias():
    
    resCats=Cat.query.order_by(Cat.name).all()

    return render_template('listacategorias.html',resCats=resCats)    







 
class Ocat_actual:
    def __init__(self, cat_name):
        self.cat_name = cat_name

@app.route('/subcategorias', methods=['GET','POST'])
def subcategorias():     

    cat_actual=[]
    #my_ocat_actual=Ocat_actual('Categoria')

    print("******* entra a subcategorias")

    form = SelectCat()
    form_add = AddSubcat()


    if form_add.validate_on_submit(): 
        
              
        print(f"categoria seleccionada: {cat_actual}")
        subcat_nombre=form_add.name.data      
              
        sel_cat=form.cats.data
        #if sel_cat:
        print(f"****** Agregar subcategoria: {subcat_nombre} a cat:{sel_cat} ") 
        #subcat_agregar=Subcat(name=subcat_nombre,cat=)        

        #obj_sel_cat=Cat.query.filter(Cat.name==sel_cat).first()
        # print(f"******* Categoria elegida: {sel_cat.name}, id: {sel_cat.id} ********")
        
        # if sel_cat:
        #    res_subcats=sel_cat.subcats.all()
        #    print("***** Subcaterogorias: ********")
        #    for subcat in res_subcats:
        #        print(f"***** {subcat.name}") 
        #return f"****** Agregar subcategoria: {subcat_nombre}"
        return render_template('subcategorias.html',form=form,form_add=form_add) 

    
    if form.validate_on_submit():

        print("********** vuelve de elegir categorias")

        sel_cat=form.cats.data
        if sel_cat:
            cat_actual.append(sel_cat.name)
            print(f"cat seleccionada {cat_actual}")
   
        if sel_cat:
          
            print(f"********* {sel_cat.name} ********")
            res_subcats=sel_cat.subcats.all()
            print('********* Subcategorias:  *********')
            for subcat in res_subcats:
                print(f"***** {subcat.name}")
            print("********** arma lista de subcategorias y recarga")
            return render_template('subcategorias.html',form=form,res_subcats=res_subcats,sel_cat=sel_cat.name,form_add=form_add)  


           #my_ocat_actual=Ocat_actual()

    
        
    
    return render_template('subcategorias.html',form=form,form_add=form_add)    



@app.route('/delCat/<cat_id>')
def delCat(cat_id):

    catDel=Cat.query.filter(Cat.id==cat_id).first()
    print(f"********* Eliminar Categoria: {catDel.name} *********")

    db.session.delete(catDel)
    db.session.commit()

    return redirect(url_for('categorias'))

@app.route('/editCat/', methods=['GET', 'POST'])
@app.route('/editCat/<cat_id>', methods=['GET', 'POST'])
def edit(cat_id):

    form = EditCat()

    #cat=Cat.query.filter(Cat.id==cat_id).first()

    cat = Cat.query.get(cat_id)

    print(f"********* Editar Categoria: {cat.name}, Id: {cat.id} *********")

    if request.method == 'GET':
       form.name.data = cat.name  

 
  
    if form.validate_on_submit():
        catName= form.name.data.strip()
        print(f" **** Categoria Nueva: {catName} *****")

        existeCat=Cat.query.filter(Cat.name==catName).first()
        if existeCat:
            print(f"La categoria {catName} ya esta ingresada")
            return render_template('editCat.html',form=form,error='Ya existe categoria',cat=cat,)  

        cat.name=catName      
        db.session.commit()

        form.name.data = ''
        resCats=Cat.query.order_by(Cat.name).all()

        return render_template('categorias.html',form=form,resCats=resCats)    

    return render_template('editCat.html',cat=cat,form=form)


if __name__ == '__main__':
    #app.run(host='192.168.1.51',debug=True)   
    app.run(debug=True)
