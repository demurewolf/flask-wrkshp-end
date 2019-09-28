from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from task_tracker.db import get_db

bp = Blueprint('tasks', __name__)

@bp.route('/')
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT t.id, title, body, created FROM tasks t'
        ' ORDER by priority, created DESC').fetchall()
    return render_template('tasks/index.html', tasks=tasks)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        priority = request.form['priority']

        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'Body is required'

        if not priority:
            priority = 1

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tasks (title, body, priority)'
                ' VALUES (?, ?, ?)',
                (title, body, priority)
            )
            db.commit()
            return redirect(url_for('tasks.index'))

    return render_template('tasks/create.html')

def get_task(id):
    post = get_db().execute(
        'SELECT t.id, title, body, created, priority'
        ' FROM tasks t'
        ' WHERE t.id = ?',
        (id, )
    ).fetchone()

    if post is None:
        abort(404, "Task id {0} doesn't exist.".format(id))

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        priority = request.form['priority']
        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'Body is required'

        if not priority:
            priority = 1

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE tasks SET title = ?, body = ?, priority = ?'
                ' WHERE id = ?',
                (title, body, priority, id)
            )
            db.commit()
            return redirect(url_for('tasks.index'))

    return render_template('tasks/update.html', task=task)


@bp.route('/<int:id>/delete')
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tasks.index'))