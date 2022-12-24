from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from config import config
import sqlalchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
jwt = JWTManager()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.contact import contact_bp
        from app.account import account_bp
        from app.task import task_bp
        from app.category_api import category_api_bp
        from app.task_api import task_api_bp
        from app.swagger import swagger_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(task_bp)
        app.register_blueprint(category_api_bp, url_prefix='/api')
        app.register_blueprint(task_api_bp, url_prefix='/api/v2/tasks')
        app.register_blueprint(swagger_bp, url_prefix='/swagger')

    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')
    
    return app
