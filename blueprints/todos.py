from flask import redirect, render_template, flash, url_for, Blueprint
from flask_login import current_user, login_required
from blueprints.databases import ToDo, db
from blueprints.forms import AddTodoForm


todo = Blueprint('todo', __name__)


@login_required
@todo.route('/todos/<user_id>')
def todos(user_id):
    # Retrieve todos for the logged user from the database
    todos = ToDo.query.filter(ToDo.user_id == user_id).all()
    form = AddTodoForm()

    # Pass the todos to the template
    return render_template('todos.html', todos=todos, form=form)


@login_required
@todo.route('/add_todo', methods=["POST", "GET"])
def add_todo():
    form = AddTodoForm()

    if form.validate_on_submit():
        todo = form.todo.data

        # Add the todo to the database
        new_todo = ToDo(description=todo, status=False, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo added successfully!")
        return redirect(url_for("todo.todos", user_id=current_user.id))
    

@login_required
@todo.route('/delete_todo/<todo_id>')
def delete_todo(todo_id):
    # Retrieve the todo from the database
    todo = ToDo.query.filter(ToDo.id == todo_id).first()

    # Delete the todo from the database
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully!")
    return redirect(url_for("todo.todos", user_id=current_user.id))


@login_required
@todo.route("/change_status/<todo_id>")
def change_status(todo_id):
    # Retrieve the todo from the database
    todo = ToDo.query.filter(ToDo.id == todo_id).first()

    # Change the status of the todo
    if todo.status == False:
        todo.status = True
    else:
        todo.status = False
    
    db.session.commit()
    flash("Todo status changed successfully!")
    return redirect(url_for("todo.todos", user_id=current_user.id))
