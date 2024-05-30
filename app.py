from flask import Flask
from blueprints.main import main
from blueprints.databases import db

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db.init_app(app)

app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True)