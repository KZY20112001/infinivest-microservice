from flask import Flask

from .routes import robo_advisor_bp
from .config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(robo_advisor_bp, url_prefix='/robo-advisor')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
