from flask import redirect, render_template, flash, url_for, Blueprint
from flask_login import current_user, login_required
from databases import ToDo, AddTodoForm, db


todo = Blueprint('todo', __name__)


@login_required
@todo.route('/todos/<user_id>')
def todos(user_id):
    # Retrieve todos for the logged user from the database
    todos = ToDo.query.filter(ToDo.user_id == user_id).all()

    # Pass the todos to the template
    return render_template('todos.html', todos=todos)


@login_required
@todo.route('/add_todo', methods=["POST", "GET"])
def add_todo():
    form = AddTodoForm()

    if form.validate_on_submit():
        todo = form.todo.data

        # Add the todo to the database
        new_todo = ToDo(description=todo, status="Not Done", user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo added successfully!")
        return redirect(url_for("todo.todos", user_id=current_user.id))
