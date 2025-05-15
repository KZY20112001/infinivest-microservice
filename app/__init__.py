from flask import Flask
from .routes import robo_advisor_bp, assets_bp, chat_bp, insights_bp
from .config import Config


blueprints = [
    (robo_advisor_bp, '/robo-advisor'),
    (assets_bp, '/assets'),
    (chat_bp, '/chat'), 
    (insights_bp, '/insights')
]
    
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
