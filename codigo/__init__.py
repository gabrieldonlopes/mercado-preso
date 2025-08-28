import os
from dotenv import load_dotenv
from flask import Flask, render_template
from collections import defaultdict

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

from .dependencies import db, migrate
from .models import Produto

def create_app():
    app = Flask(__name__)

    # Configurações da app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "mercado_preso.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar Blueprints
    from .autenticacao import bp_auth
    app.register_blueprint(bp_auth)
    
    from .compra import bp_compra
    app.register_blueprint(bp_compra)

    @app.route("/")
    def home():
        produtos = Produto.query.all()

        # Agrupar produtos por vendedor
        produtos_por_vendedor = defaultdict(list)
        for produto in produtos:
            produtos_por_vendedor[produto.vendedor].append(produto)

        return render_template("home.html", produtos_por_vendedor=produtos_por_vendedor)

    return app