from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config['SECRET_KEY'] = 'scriptpythonic'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Setup the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.user_login'
    login_manager.init_app(app)

    from .models import User

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register the auth blueprint
    from .auth import auth as auth_blueprint
    from .views import views
    from .pay import payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(views)

    # Register other blueprints if needed
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
