from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField, DateField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length
from ..account.models import User
from .models import Category

class TaskCreateForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(message='Field cannot be empty!')]
    )
    description = CKEditorField(
        'Description',
        validators=[DataRequired(), Length(min=3, max=150, message='Field must be between 3 and 150 characters long!')]
    )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    category = SelectField(
        'Category',
        coerce=int
    )
    collaborators = SelectMultipleField(
        'User',
        coerce=int
    )
    deadline = DateField(
        'Deadline', 
        validators=[DataRequired()]
    )
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in Category.query.all()]
        form.collaborators.choices = [(elem.id, elem.username) for elem in User.query.all()]
        return form

    submit = SubmitField('Submit')


class FormTaskUpdate(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(message='Field cannot be empty!')]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=3, max=150, message='Field must be between 3 and 150 characters long!')]
    )
    priority = SelectField(
        'Priority',
        choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')]
    )
    category = SelectField(
        'Category',
        coerce=int
    )
    collaborators = SelectMultipleField(
        'User',
        coerce=int
    )
    progress = SelectField(
        'Progress',
        choices=[('todo', 'todo'), ('doing', 'doing'), ('done', 'done')]
    )
    deadline = DateField(
        'Deadline', 
        validators=[DataRequired()]
    )
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the agency field
        form.category.choices = [(elem.id, elem.name) for elem in Category.query.all()]
        form.collaborators.choices = [(elem.id, elem.username) for elem in User.query.all()]
        return form
    submit = SubmitField('Submit')


class CategoryCreateForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message='Field cannot be empty!')]
    )
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = CKEditorField(
        ' ', 
        [DataRequired(message='Field cannot be empty!')])
    
    submit = SubmitField('Send')