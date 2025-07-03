
from flask import Flask
from fanclub.routes.auth import auth_bp
from fanclub.extensions import db




app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'  # or PostgreSQL etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




with app.app_context():
    db.drop_all()
    db.create_all()  # Create tables


if __name__ == "__main__":
    app.run(debug=True)