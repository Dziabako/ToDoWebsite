from flask import Flask
from blueprints.databases import db
from blueprints.main import main
from blueprints.users import user, login_manager
from blueprints.todos import todo

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(todo)


# Create the database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)