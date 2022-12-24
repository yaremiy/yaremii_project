from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required

from .. import db
from ..account.models import User
from .models import Comment, Task, Category
from .forms import CategoryCreateForm, CommentForm, TaskCreateForm, FormTaskUpdate
from . import task_bp


@task_bp.route("/user/<id>/tasks")
def tasks(id):
    user = User.query.get_or_404(id)
    return render_template('tasks.html', user=user)


@task_bp.route("/tasks/<id>", methods=['GET', 'POST'])
@login_required
def task(id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data, 
            user_id=current_user.id,
            task_id=id
        )
        try:
            db.session.add(comment)
            db.session.commit()
            flash(f"Added new comment", category='success')
        except:
            db.session.flush()
            db.session.rollback()

    task = Task.query.get_or_404(id)
    return render_template('task.html', task=task, form=form)


@task_bp.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@task_bp.route("/categories/create", methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryCreateForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        try:
            db.session.add(category)
            db.session.commit()
        except:
            db.session.flush()
            db.session.rollback()
        flash(f"New category created: {form.name.data}", category='success')
        return redirect(url_for("task.categories"))
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    return render_template('create_category.html', form=form)


@task_bp.route("/tasks/create", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskCreateForm.new()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            category_id=form.category.data,
            owner_id=current_user.id,
            deadline=form.deadline.data
        )
        try:
            task.collaborators.append(current_user)
            for collaborator in form.collaborators.data:
                task.collaborators.append(User.query.get_or_404(collaborator))
            db.session.add(task)
            db.session.commit()
            flash(f"New task created: {form.title.data}", category='success')
            return redirect(url_for("task.tasks", id=current_user.id))
        except:
           db.session.flush()
           db.session.rollback()
           flash(f"Unknown error", category='danger')
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    return render_template('create_task.html', form=form)


@task_bp.route('/categories/<id>/delete')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f"Category has been deleted", category='success')
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("task.categories"))


@task_bp.route('/tasks/<id>/delete')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f"Task has been deleted", category='success')
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("task.tasks", id=current_user.id))


@task_bp.route("/tasks/<id>/update", methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    form = FormTaskUpdate.new()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.progress = form.progress.data
        task.category_id = form.category.data
        task.deadline = form.deadline.data

        try:
            task.collaborators.clear()
            for collaborator in form.collaborators.data:
                task.collaborators.append(User.query.get_or_404(collaborator))
            db.session.commit()
            flash(
                f"Task has been updated: {form.title.data}", category='success')
            return redirect(url_for("task.tasks", id=current_user.id))
        except:
            db.session.flush()
            db.session.rollback()
            flash(f"Unknown error", category='danger')
            return render_template('update_task.html', form=form, id=id)
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    form.title.data = task.title
    form.description.data = task.description
    form.priority.data = task.priority.name
    form.progress.data = task.progress.name
    form.category.data = task.category_id
    form.collaborators.data = [
        collaborator.id for collaborator in task.collaborators]
    form.deadline.data = task.deadline
    return render_template('update_task.html', form=form, id=id)


@task_bp.route("/categories/<id>/update", methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryCreateForm()

    if form.validate_on_submit():
        category.name = form.name.data
        try:
            db.session.add(category)
            db.session.commit()
            flash(
                f"Category has been updated: {form.name.data}", category='success')
            return redirect(url_for("task.categories"))
        except:
            db.session.flush()
            db.session.rollback()
            flash(f"Unknown error", category='danger')
            return render_template('update_category.html', form=form, id=id)
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    form.name.data = category.name
    return render_template('update_category.html', form=form, id=id)