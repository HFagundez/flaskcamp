from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField, validators
from wtforms_sqlalchemy.fields import QuerySelectField


class AddCat(FlaskForm):
    name = StringField('Categoría: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    submit = SubmitField('Agregar')

class EditCat(FlaskForm):
    name = StringField('Categoría: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    submit = SubmitField('Aceptar')


class Add(FlaskForm):
    name = StringField('Nombre: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    surname = StringField('Apellido: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    email = StringField('email: ', [validators.DataRequired(),validators.Length(min=2, max=50)])
    submit = SubmitField('Add Item')

class DelForm(FlaskForm):
    id = IntegerField("Id of Item to Remove: ")    
    submit = SubmitField("Remove Item")