from flask import Flask
from .config import Config
from .extensions import db, migrate, cors, ma
from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'b5065f35e6b34d18ba2a3b86ae1d9675'  

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    ma.init_app(app) 
    # csrf.init_app(app)
    with app.app_context():
        from .security import security as security_blueprint
        from .seo import seo as seo_blueprint

        app.register_blueprint(security_blueprint, url_prefix='/api/security')
        app.register_blueprint(seo_blueprint, url_prefix='/api')

        db.create_all()

    return app