from flask import Flask
from .routes.bank_statement import bank_statement_bp
from .config.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.register_blueprint(bank_statement_bp, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
