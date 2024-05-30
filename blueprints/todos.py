from flask import redirect, render_template, flash, url_for, Blueprint
from databases import ToDo


todo = Blueprint('todo', __name__)


@todo.route('/todos/<user_id>')
def todos(user_id):
    # Retrieve todos for the logged user from the database
    todos = ToDo.query.filter(ToDo.user_id == user_id).all()

    # Pass the todos to the template
    return render_template('todos.html', todos=todos)
