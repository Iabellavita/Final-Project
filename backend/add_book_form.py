from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class AddBookForm(FlaskForm):
    title = StringField('Title', name='title', id='title', validators=[DataRequired()])
    author = StringField('Author', name='author', id='author', validators=[DataRequired()])
    year = IntegerField('Year', name='year', id='year', validators=[DataRequired(), NumberRange()])

    submit = SubmitField('Add book', id='submit_addbook')
