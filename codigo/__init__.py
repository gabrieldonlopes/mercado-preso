import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configurações da app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar Blueprints

    # Rotas básicas
    @app.route("/")
    def home():
        return render_template("home.html")

    return app