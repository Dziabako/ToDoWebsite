from flask import Flask
from blueprints.main import main
from blueprints.databases import db
from blueprints.users import user
from blueprints.todos import todo

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db.init_app(app)

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(todo)


if __name__ == '__main__':
    app.run(debug=True)